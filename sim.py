"""JSBSim c172x at 50 Hz with a PID autopilot and attitude-to-servo mapping."""
import jsbsim

import config


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
        self.state = self.read()

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
        f["fcs/rudder-cmd-norm"] = 0.0

        # speed -> throttle
        f["fcs/throttle-cmd-norm"] = self.speed_pid.step(self.target_speed - s["airspeed"], dt)

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
