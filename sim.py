"""JSBSim c172x at 50 Hz with a PID autopilot and attitude-to-servo mapping."""
import math
import random

import jsbsim

import config

KT2FPS = 1.6878


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def wrap180(deg):
    return (deg + 180.0) % 360.0 - 180.0


class PID:
    def __init__(self, kp, ki, kd, out):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.lo, self.hi = out
        self.i = 0.0
        self.prev = None

    def step(self, err, dt):
        if self.ki:
            self.i = clamp(self.i + err * dt, self.lo / self.ki, self.hi / self.ki)   # anti-windup
        d = 0.0 if self.prev is None else (err - self.prev) / dt
        self.prev = err
        return clamp(self.kp * err + self.ki * self.i + self.kd * d, self.lo, self.hi)


class Sim:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dt = 1.0 / config.SIM_HZ
        self.fdm = jsbsim.FGFDMExec(None)
        self.fdm.set_debug_level(0)
        self.fdm.load_model(config.AIRCRAFT)
        f = self.fdm
        f["ic/h-sl-ft"] = config.START_ALT_FT
        f["ic/vc-kts"] = config.START_SPEED_KTS
        f["ic/psi-true-deg"] = config.START_HEADING_DEG
        f["ic/gamma-deg"] = 0
        f["fcs/throttle-cmd-norm"] = 0.7
        f["fcs/mixture-cmd-norm"] = 0.87
        f["propulsion/magneto_cmd"] = 3
        f["propulsion/set-running"] = -1       # start engines before run_ic, else trim fails
        f.set_dt(self.dt)
        f.run_ic()
        f.run()
        try:
            f["simulation/do_simple_trim"] = 1
        except Exception as e:                 # fly untrimmed; the PIDs will take over
            print(f"SIM: trim failed ({e})")
        self.trim_pitch = f["attitude/theta-deg"]
        self.trim_throttle = f["fcs/throttle-cmd-norm"]

        self.target_alt = float(config.START_ALT_FT)
        self.target_heading = float(config.START_HEADING_DEG)
        self.target_speed = float(config.START_SPEED_KTS)

        self.alt_pid = PID(**config.ALT_PID)
        self.pitch_pid = PID(**config.PITCH_PID)
        self.hdg_pid = PID(**config.HDG_PID)
        self.roll_pid = PID(**config.ROLL_PID)
        self.speed_pid = PID(**config.SPEED_PID)
        if self.speed_pid.ki:
            self.speed_pid.i = self.trim_throttle / self.speed_pid.ki   # start at trim throttle
        self.kick_until = -1.0
        self.kick_sign = 1.0
        self._weather_on()
        self.state = self.read()

    # --- weather ------------------------------------------------------------
    def _weather_on(self):
        """Steady wind plus MIL-STD turbulence, always on. Gusts are added in step()."""
        f = self.fdm
        rad = math.radians(config.WIND_FROM_DEG)
        v = config.WIND_KTS * KT2FPS
        f["atmosphere/wind-north-fps"] = -v * math.cos(rad)      # wind FROM north blows south
        f["atmosphere/wind-east-fps"] = -v * math.sin(rad)
        f["atmosphere/turb-type"] = 3                             # 3 = MIL-STD-1797 model
        f["atmosphere/turbulence/milspec/windspeed_at_20ft_AGL-fps"] = config.TURB_WIND_20FT_FPS
        f["atmosphere/turbulence/milspec/severity"] = config.TURB_SEVERITY
        self.next_gust = random.uniform(*config.GUST_EVERY_S)
        self.gust_end = -1.0
        self.gust_vec = (0.0, 0.0, 0.0)

    def _gusts(self, t):
        f = self.fdm
        if t >= self.next_gust:
            g = config.GUST_KTS * KT2FPS * random.uniform(0.5, 1.0)
            a = random.uniform(0, 2 * math.pi)
            self.gust_vec = (g * math.cos(a), g * math.sin(a), random.uniform(-0.6, 0.6) * g)
            self.gust_end = t + config.GUST_LEN_S
            self.next_gust = t + random.uniform(*config.GUST_EVERY_S)
        if t < self.gust_end:
            k = math.sin(math.pi * (self.gust_end - t) / config.GUST_LEN_S)   # smooth ramp up and down
            f["atmosphere/gust-north-fps"] = self.gust_vec[0] * k
            f["atmosphere/gust-east-fps"] = self.gust_vec[1] * k
            f["atmosphere/gust-down-fps"] = self.gust_vec[2] * k
        else:
            f["atmosphere/gust-north-fps"] = 0.0
            f["atmosphere/gust-east-fps"] = 0.0
            f["atmosphere/gust-down-fps"] = 0.0

    def kick_rudder(self):
        """Pretend the pilot kicked the rudder: full deflection for RUDDER_KICK_S, alternating sides."""
        self.kick_sign = -self.kick_sign
        self.kick_until = self.state["time"] + config.RUDDER_KICK_S

    def set_targets(self, alt_ft=None, heading_deg=None, speed_kts=None):
        if alt_ft is not None:
            self.target_alt = float(alt_ft)
        if heading_deg is not None:
            self.target_heading = float(heading_deg) % 360.0
        if speed_kts is not None:
            self.target_speed = float(speed_kts)

    def read(self):
        f = self.fdm
        return {
            "pitch": f["attitude/theta-deg"],
            "roll": f["attitude/phi-deg"],
            "heading": f["attitude/psi-deg"] % 360.0,
            "airspeed": f["velocities/vc-kts"],
            "altitude": f["position/h-sl-ft"],
            "alpha": f["aero/alpha-deg"],
            "stall": f["aero/alpha-deg"] > config.STALL_ALPHA_DEG,
            "agl": f["position/h-agl-ft"],
            "gust": abs(f["atmosphere/gust-north-fps"]) + abs(f["atmosphere/gust-east-fps"]) > 1.0,
            "wind_kts": math.hypot(f["atmosphere/total-wind-north-fps"], f["atmosphere/total-wind-east-fps"]) / KT2FPS,
            "crashed": f["position/h-agl-ft"] < config.CRASH_AGL_FT,
            "time": f["simulation/sim-time-sec"],
        }

    def step(self):
        """One 50 Hz physics step with the autopilot. Returns the new state."""
        s = self.state
        f = self.fdm
        dt = self.dt

        # altitude -> pitch -> elevator
        pitch_cmd = self.trim_pitch + self.alt_pid.step(self.target_alt - s["altitude"], dt)
        if s["airspeed"] < config.MIN_SPEED_KTS:                    # protect airspeed on steep climbs
            pitch_cmd = min(pitch_cmd, self.trim_pitch + (s["airspeed"] - config.MIN_SPEED_KTS + 10.0))
        if s["stall"]:
            pitch_cmd = min(pitch_cmd, self.trim_pitch - 3.0)      # nose down to recover
        f["fcs/elevator-cmd-norm"] = -self.pitch_pid.step(pitch_cmd - s["pitch"], dt)

        # heading -> roll -> aileron
        roll_cmd = self.hdg_pid.step(wrap180(self.target_heading - s["heading"]), dt)
        f["fcs/aileron-cmd-norm"] = self.roll_pid.step(roll_cmd - s["roll"], dt)
        f["fcs/rudder-cmd-norm"] = self.kick_sign * config.RUDDER_KICK if s["time"] < self.kick_until else 0.0

        # speed -> throttle
        f["fcs/throttle-cmd-norm"] = self.speed_pid.step(self.target_speed - s["airspeed"], dt)

        self._gusts(s["time"])
        f.run()
        self.state = self.read()
        return self.state

    def servo_offsets(self):
        """Map attitude to (P, R, Y) degrees for the Uno."""
        s = self.state
        lim = config.LIMIT_DEG
        p = clamp(s["pitch"] - self.trim_pitch, -lim, lim)
        r = clamp(s["roll"], -lim, lim)
        y = clamp(wrap180(self.target_heading - s["heading"]) * config.YAW_SCALE, -lim, lim)
        return p, r, y
