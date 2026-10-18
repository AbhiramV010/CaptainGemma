"""Project settings. Edit these before a run."""
import os

# --- Hardware ---
COM_PORT = "COM4"          # the Uno's port, e.g. "COM5"
BAUD = 9600
BRIDGE_HZ = 20             # max serial update rate
LIMIT_DEG = 20             # every axis is clamped to ±20°

# --- Captain backend ---
CAPTAIN_BACKEND = "ollama"             # "ollama" or "api"
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma3:4b"
OLLAMA_KEEP_ALIVE = "30m"               # keep the model loaded between calls
CAPTAIN_WARMUP_S = 60.0                # timeout for the one-off model load at start
# Hosted endpoint (OpenAI-compatible chat completions). Key comes from the env var, never from code.
API_URL = os.environ.get("CAPTAIN_API_URL", "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions")
API_MODEL = os.environ.get("CAPTAIN_API_MODEL", "gemma-3-27b-it")
API_KEY_ENV = "CAPTAIN_API_KEY"
CAPTAIN_PERIOD_S = 4.0                 # seconds between captain calls
CAPTAIN_TIMEOUT_S = 20.0               # HTTP timeout per call (gemma3:4b on CPU takes ~9 s; gemma3:1b ~3 s)
CAPTAIN_STALE_S = 15.0                 # print CAPTAIN STALE after this long without a valid reply
CAPTAIN_MAX_TOKENS = 80                # cap the reply length so a rambling model cannot stall the loop

# --- Sim ---
SIM_HZ = 50
AIRCRAFT = "c172x"
START_ALT_FT = 3000
START_HEADING_DEG = 90
START_SPEED_KTS = 100
RUDDER_KICK = 0.8          # rudder command (0-1) applied on a kick
RUDDER_KICK_S = 1.0        # how long the kick lasts
MIN_SPEED_KTS = 70         # below this the autopilot limits nose-up pitch
CRASH_AGL_FT = 10.0        # below this height above ground the plane counts as crashed
CRASH_RESET_S = 5.0        # reset the sim this long after a crash (0 = stay crashed)
STALL_ALPHA_DEG = 15.0     # c172x lift curve flattens past ~0.26 rad (15°); verify before demo
YAW_SCALE = 1.0            # Y = heading error × YAW_SCALE, clamped ±20

# --- Autopilot (PID) gains ---
ALT_PID   = dict(kp=0.03, ki=0.0001, kd=0.01, out=(-20.0, 20.0))     # ft error -> target pitch deg
PITCH_PID = dict(kp=0.08, ki=0.02, kd=0.01, out=(-1.0, 1.0))          # pitch deg error -> elevator
HDG_PID   = dict(kp=1.5, ki=0.0, kd=0.3, out=(-20.0, 20.0))           # heading deg error -> target roll deg
ROLL_PID  = dict(kp=0.02, ki=0.002, kd=0.005, out=(-0.5, 0.5))        # roll deg error -> aileron
SPEED_PID = dict(kp=0.02, ki=0.004, kd=0.0, out=(0.0, 1.0))           # kts error -> throttle

# --- Files ---
ROOT = os.path.dirname(os.path.abspath(__file__))
PRY_CSV = os.path.join(ROOT, "pry.csv")
ATTEMPTS_MD = os.path.join(ROOT, "notes", "attempts.md")
