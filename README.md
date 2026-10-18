# HT6HackDay2026 - AI Pilot

Project made for Hack the 6ix's Hack Day, October 18th 2026. Developers: Abhiram Vadali, Dhyanesh Sivaram, Shubh Patel.

An AI captain (Gemma) flies a Cessna 172 in JSBSim. A PID autopilot tracks the captain's targets, and an Arduino Uno
mirrors the sim's attitude on a physical plane (yaw stepper, pitch servo, roll servo).

## Layout

| File | Role |
|---|---|
| `main.py` | Starts sim, captain thread and bridge. Prints a status line every second. Ctrl+C stops and writes a summary. |
| `sim.py` | JSBSim `c172x` at 50 Hz, PID autopilot (alt→pitch, heading→roll, speed→throttle), attitude→servo mapping, stall flag. |
| `captain.py` | Gemma on a worker thread, every 4 s. Validates the JSON reply, keeps the last good target, logs to `notes/attempts.md`. |
| `bridge.py` | Owns the COM port. Sends `Y`/`P`/`R` at ≤20 Hz, only on a ≥1° change. Reconnects every second. |
| `gui.py` | Manual test: three sliders, `Centre all`, `Save PRY` → `pry.csv`. Never run alongside `main.py`. |
| `config.py` | COM port, captain backend, PID gains, stall alpha, yaw scale. |
| `firmware/pilot_slider/pilot_slider.ino` | Uno firmware. Stepper on 8/10/9/11, pitch servo 5, roll servo 6. Prints `READY`. |

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install jsbsim pyserial requests
```

Flash the firmware (needs AccelStepper from the Library Manager). Set `COM_PORT` in `config.py`.

Captain backend (`config.py`):
- `ollama`: `ollama pull gemma3:4b`, then `ollama serve`. The first call loads the model (~13 s); `main.py` warms it up before the sim starts.
- `api`: set `CAPTAIN_API_KEY` in the environment (and optionally `CAPTAIN_API_URL` / `CAPTAIN_API_MODEL`, OpenAI-compatible chat endpoint).

## Run

```powershell
python gui.py                # motors + logging test
python captain.py            # captain-alone test: prints JSON and response time
python main.py --sim-only    # sim + captain, no hardware
python main.py               # full run
python main.py --no-captain  # sim holds the start targets (autopilot test)
```

Measured on the laptop: `gemma3:4b` on CPU answers in ~9 s alone and ~17 s while the sim runs. For a snappier demo use
`OLLAMA_MODEL = "gemma3:1b"` or the `api` backend. `CAPTAIN_TIMEOUT_S` and `CAPTAIN_STALE_S` are set for the 4b model.

## Crash buzzer

The sim counts a crash when the plane is under 10 ft above ground (`CRASH_AGL_FT`). `main.py` then prints `CRASH`,
centres the plane, sends `C` to the Uno once, and resets the sim after 5 s (`CRASH_RESET_S`, 0 = stay crashed).

On `C` the firmware drives pin 12 HIGH for two 150 ms beeps with a 150 ms gap. It does not block, so the stepper keeps running.

- Wiring: buzzer `+` to pin 12, `-` to GND. An active buzzer works as is.
- Passive buzzer: set `BUZZER_PASSIVE = true` in the sketch so it uses `tone()`.
- Test: the `Test buzzer` button in `gui.py`, or `python main.py --crash-test` (dives into the ground in about 40 s).

## Rudder-kick button

A push button between pin 2 and GND (internal pull-up, no resistor needed). Each press makes the Uno send `K` to the
laptop. `main.py` then applies full rudder (`RUDDER_KICK`) for one second (`RUDDER_KICK_S`), alternating sides each press,
so the sim plane yaws about 10° and the yaw stepper swings with it. Console prints `RUDDER KICK`.

## Weather

Always on, set in `config.py`: an 18 kt wind from 030, MIL-STD-1797 turbulence at severity 4, and random 3 s gusts of up to
15 kt every 6 to 14 s. The captain sees `wind_kts` and `gust` in its state, and the window shows the wind in the status row.
