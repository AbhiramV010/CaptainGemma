"""Gemma captain. Runs on a worker thread; the physics loop never waits on it."""
import json
import os
import re
import sys
import threading
import time

import requests

import config

SYSTEM_PROMPT = (
    "You are the captain of a Cessna 172 flying in a simulator. Every few seconds you receive the "
    "aircraft state as JSON. Reply with ONLY one JSON object, no prose, no markdown, of the form "
    '{"target_alt_ft": int, "target_heading_deg": int, "target_speed_kts": int, "callout": str}. '
    "Keep altitude between 1500 and 6000 ft, speed between 70 and 120 kts, heading 0-359. "
    "Change targets gradually (at most 500 ft, 30 degrees, 10 kts per reply). If stall is true, "
    "lower the target altitude and raise the target speed. Expect strong wind, gusts and turbulence; "
    "keep speed at or above 90 kts in rough air. The callout is one short sentence."
)

KEYS = ("target_alt_ft", "target_heading_deg", "target_speed_kts")


def append_attempt(line):
    os.makedirs(os.path.dirname(config.ATTEMPTS_MD), exist_ok=True)
    new = not os.path.exists(config.ATTEMPTS_MD)
    with open(config.ATTEMPTS_MD, "a", encoding="utf-8") as fh:
        if new:
            fh.write("# Captain attempts\n\nOne line per call: what failed and what to change.\n\n")
        fh.write(f"- {time.strftime('%Y-%m-%d %H:%M:%S')} {line}\n")


def parse_reply(text):
    """Return a validated target dict or raise ValueError."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("no JSON object in reply")
    data = json.loads(m.group(0))
    out = {}
    for k in KEYS:
        if k not in data:
            raise ValueError(f"missing {k}")
        out[k] = int(round(float(data[k])))
    out["target_alt_ft"] = max(500, min(10000, out["target_alt_ft"]))
    out["target_heading_deg"] = out["target_heading_deg"] % 360
    out["target_speed_kts"] = max(60, min(140, out["target_speed_kts"]))
    out["callout"] = str(data.get("callout", ""))[:200]
    return out


class Captain:
    def __init__(self, backend=config.CAPTAIN_BACKEND):
        self.backend = backend
        self.target = None            # last valid target
        self.last_ok = None           # wall time of last valid reply
        self.last_call = None
        self.last_rt = None           # response time of the last call
        self.notes = []               # last three callouts
        self.failures = 0
        self.calls = 0
        self._state = None
        self._started = time.time()
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._started = time.time()
        self._thread.start()

    def warm_up(self):
        """Load the model before the sim starts; cold load can take >10 s on Ollama."""
        if self.backend != "ollama":
            return
        try:
            t0 = time.time()
            requests.post(config.OLLAMA_URL, timeout=config.CAPTAIN_WARMUP_S, json={
                "model": config.OLLAMA_MODEL, "messages": [], "keep_alive": config.OLLAMA_KEEP_ALIVE})
            print(f"CAPTAIN model loaded in {time.time() - t0:.1f}s")
        except Exception as e:
            print(f"CAPTAIN warm-up failed: {e.__class__.__name__}: {str(e)[:100]}")

    def stop(self):
        self._stop.set()

    def update_state(self, s):
        with self._lock:
            self._state = {
                "altitude_ft": int(s["altitude"]),
                "heading_deg": int(s["heading"]),
                "airspeed_kts": int(s["airspeed"]),
                "pitch_deg": round(s["pitch"], 1),
                "roll_deg": round(s["roll"], 1),
                "stall": bool(s["stall"]),
                "wind_kts": int(s.get("wind_kts", 0)),
                "gust": bool(s.get("gust", False)),
            }

    def stale(self):
        ref = self.last_ok if self.last_ok else self._started
        return time.time() - ref > config.CAPTAIN_STALE_S

    # --- worker -------------------------------------------------------------
    def _run(self):
        while not self._stop.is_set():
            with self._lock:
                state = dict(self._state) if self._state else None
            if state is not None:
                self.call_once(state)
            self._stop.wait(config.CAPTAIN_PERIOD_S)

    def call_once(self, state):
        """One request/response cycle. Safe to call from a test."""
        payload = dict(state, notes=self.notes[-3:])
        self.calls += 1
        t0 = time.time()
        self.last_call = t0
        try:
            text = self._ask(json.dumps(payload))
            self.last_rt = time.time() - t0
            target = parse_reply(text)
        except Exception as e:
            self.last_rt = time.time() - t0
            self.failures += 1
            msg = f"FAIL ({self.backend}, {self.last_rt:.1f}s): {e.__class__.__name__}: {str(e)[:120]}"
            print(f"CAPTAIN {msg}")
            append_attempt(msg + " | change: " + self._hint(e))
            return None
        self.target = target
        self.last_ok = time.time()
        if target["callout"]:
            self.notes.append(target["callout"])
            self.notes = self.notes[-3:]
        append_attempt(f"OK ({self.backend}, {self.last_rt:.1f}s): {json.dumps(target)}")
        return target

    @staticmethod
    def _hint(e):
        if isinstance(e, requests.exceptions.ConnectionError):
            return "backend not reachable; run `ollama serve` or set CAPTAIN_BACKEND='api'"
        if isinstance(e, requests.exceptions.Timeout):
            return "raise CAPTAIN_TIMEOUT_S or use a smaller model"
        if isinstance(e, (ValueError, KeyError)):
            return "model returned bad JSON; tighten SYSTEM_PROMPT or lower temperature"
        return "see error text"

    def _ask(self, user_msg):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_msg}]
        if self.backend == "ollama":
            r = requests.post(config.OLLAMA_URL, timeout=config.CAPTAIN_TIMEOUT_S, json={
                "model": config.OLLAMA_MODEL, "messages": messages, "stream": False,
                "format": "json", "options": {"temperature": 0.2, "num_predict": config.CAPTAIN_MAX_TOKENS}, "keep_alive": config.OLLAMA_KEEP_ALIVE,
            })
            r.raise_for_status()
            return r.json()["message"]["content"]
        if self.backend == "api":
            key = os.environ.get(config.API_KEY_ENV)
            if not key:
                raise RuntimeError(f"{config.API_KEY_ENV} not set in the environment")
            r = requests.post(config.API_URL, timeout=config.CAPTAIN_TIMEOUT_S,
                              headers={"Authorization": f"Bearer {key}"},
                              json={"model": config.API_MODEL, "messages": messages, "temperature": 0.2,
                                    "max_tokens": config.CAPTAIN_MAX_TOKENS})
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        raise RuntimeError(f"unknown backend {self.backend!r}")


if __name__ == "__main__":
    # Captain-alone test (step 5): one call, print the JSON and the response time.
    backend = sys.argv[1] if len(sys.argv) > 1 else config.CAPTAIN_BACKEND
    c = Captain(backend)
    c.warm_up()
    demo = {"altitude_ft": 3000, "heading_deg": 90, "airspeed_kts": 100,
            "pitch_deg": 0.8, "roll_deg": 0.0, "stall": False}
    t = c.call_once(demo)
    print(f"backend={backend} response_time={c.last_rt:.2f}s")
    print(json.dumps(t, indent=2) if t else "NO VALID REPLY")
    if t and (c.last_rt or 0) > 4.0:
        print("WARN: slower than the 4 s goal; try OLLAMA_MODEL = 'gemma3:1b' or the api backend")
    sys.exit(0 if t else 1)
