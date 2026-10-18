"""Live tkinter view of the sim: attitude, compass, tapes, forces, and control surfaces.

Opened by main.py (use --no-gui to skip). Call update() from the main loop; it never blocks.
"""
import math
import tkinter as tk

import config

W, H = 980, 620
SKY, GROUND, INK, PANEL, ACCENT, WARN = "#4a90d9", "#8b5a2b", "#f3f3f3", "#1e1e24", "#ffd166", "#ff4d4d"


class Display:
    def __init__(self, sim):
        self.sim = sim
        self.root = tk.Tk()
        self.root.title("AI Pilot: live physics")
        self.root.configure(bg=PANEL)
        self.root.resizable(False, False)
        self.cv = tk.Canvas(self.root, width=W, height=H, bg=PANEL, highlightthickness=0)
        self.cv.pack()
        self.closed = False
        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self.info = {"callout": "", "crashed": False, "kick": 0.0, "captain_age": None, "uno": None}

    def _close(self):
        self.closed = True
        self.root.destroy()

    # --- public -------------------------------------------------------------
    def update(self, state, **info):
        if self.closed:
            return
        self.info.update(info)
        self.cv.delete("all")
        f = self.sim.fdm
        self._horizon(state, 20, 20, 420, 420)
        self._compass(state, 20, 455, 420, 70)
        self._tape(60, "IAS kt", state["airspeed"], self.sim.target_speed, 10, 490, 20, 120, 400)
        self._tape(800, "ALT ft", state["altitude"], self.sim.target_alt, 100, 630, 20, 120, 400)
        self._forces(state, f, 770, 20, 190, 400)
        self._controls(f, 490, 440, 470, 160)
        self._banner(state)
        self.root.update_idletasks()
        self.root.update()

    # --- widgets ------------------------------------------------------------
    def _horizon(self, s, x, y, w, h):
        cv = self.cv
        cx, cy = x + w / 2, y + h / 2
        pitch, roll = s["pitch"], s["roll"]
        ppd = h / 60.0                                   # pixels per degree of pitch
        r = math.radians(-roll)
        cos, sin = math.cos(r), math.sin(r)

        def rot(px, py):                                 # rotate about centre, py down = positive
            return cx + px * cos - py * sin, cy + px * sin + py * cos

        big = w * 2
        off = pitch * ppd                                # horizon moves down when nose is up
        sky = [rot(-big, -big), rot(big, -big), rot(big, off), rot(-big, off)]
        gnd = [rot(-big, off), rot(big, off), rot(big, big), rot(-big, big)]
        cv.create_polygon(*sum(map(list, sky), []), fill=SKY, outline="")
        cv.create_polygon(*sum(map(list, gnd), []), fill=GROUND, outline="")
        cv.create_line(*rot(-big, off), *rot(big, off), fill=INK, width=2)
        for deg in range(-30, 31, 10):                  # pitch ladder
            if deg == 0:
                continue
            ly = off - deg * ppd
            half = 40 if deg % 20 == 0 else 22
            cv.create_line(*rot(-half, ly), *rot(half, ly), fill=INK, width=1)
            cv.create_text(*rot(half + 18, ly), text=str(abs(deg)), fill=INK, font=("Segoe UI", 9))
        # clip to a square frame by painting the panel colour outside it
        cv.create_rectangle(0, 0, W, y, fill=PANEL, outline="")
        cv.create_rectangle(0, y + h, W, H, fill=PANEL, outline="")
        cv.create_rectangle(0, y, x, y + h, fill=PANEL, outline="")
        cv.create_rectangle(x + w, y, W, y + h, fill=PANEL, outline="")
        # roll scale
        for deg in (-60, -45, -30, -20, -10, 0, 10, 20, 30, 45, 60):
            a = math.radians(deg - 90)
            rr = h / 2 - 8
            ln = 14 if deg % 30 == 0 else 8
            cv.create_line(cx + rr * math.cos(a), cy + rr * math.sin(a),
                           cx + (rr - ln) * math.cos(a), cy + (rr - ln) * math.sin(a), fill=INK, width=2)
        a = math.radians(-roll - 90)
        rr = h / 2 - 24
        cv.create_polygon(cx + rr * math.cos(a), cy + rr * math.sin(a),
                          cx + (rr - 14) * math.cos(a - 0.06), cy + (rr - 14) * math.sin(a - 0.06),
                          cx + (rr - 14) * math.cos(a + 0.06), cy + (rr - 14) * math.sin(a + 0.06), fill=ACCENT)
        # fixed aircraft symbol
        cv.create_line(cx - 70, cy, cx - 25, cy, fill=ACCENT, width=4)
        cv.create_line(cx + 25, cy, cx + 70, cy, fill=ACCENT, width=4)
        cv.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill=ACCENT, outline="")
        cv.create_rectangle(x, y, x + w, y + h, outline="#555", width=2)
        cv.create_text(x + 8, y + h - 8, anchor="sw", fill=INK, font=("Consolas", 11),
                       text=f"pitch {s['pitch']:+5.1f}°  roll {s['roll']:+5.1f}°")
        # flight-path vector: where the plane is actually going vs where the nose points
        gamma = math.degrees(math.atan2(self.sim.fdm["velocities/h-dot-fps"],
                                        max(self.sim.fdm["velocities/vt-fps"], 1.0)))
        fy = cy - (gamma - pitch) * ppd
        fy = max(y + 12, min(y + h - 12, fy))
        cv.create_oval(cx - 7, fy - 7, cx + 7, fy + 7, outline="#7CFC00", width=2)
        cv.create_line(cx - 16, fy, cx - 7, fy, fill="#7CFC00", width=2)
        cv.create_line(cx + 7, fy, cx + 16, fy, fill="#7CFC00", width=2)

    def _compass(self, s, x, y, w, h):
        cv = self.cv
        cv.create_rectangle(x, y, x + w, y + h, fill="#2a2a32", outline="#555")
        hdg = s["heading"]
        ppd = w / 90.0                                   # 90° visible
        cx = x + w / 2
        for d in range(int(hdg) - 50, int(hdg) + 51):
            if d % 10:
                continue
            px = cx + (d - hdg) * ppd
            if x < px < x + w:
                cv.create_line(px, y + 30, px, y + 42, fill=INK)
                label = {0: "N", 90: "E", 180: "S", 270: "W"}.get(d % 360, str(d % 360))
                cv.create_text(px, y + 20, text=label, fill=INK, font=("Consolas", 11))
        # target heading bug
        err = (self.sim.target_heading - hdg + 180) % 360 - 180
        bx = max(x + 6, min(x + w - 6, cx + err * ppd))
        cv.create_polygon(bx - 7, y + 2, bx + 7, y + 2, bx, y + 12, fill=ACCENT)
        cv.create_line(cx, y, cx, y + 44, fill=ACCENT, width=2)
        cv.create_text(x + w / 2, y + h - 6, anchor="s", fill=INK, font=("Consolas", 10),
                       text=f"HDG {hdg:5.1f}°  tgt {self.sim.target_heading:3.0f}°  err {err:+5.1f}°")

    def _tape(self, span, label, val, target, step, x, y, w, h):
        cv = self.cv
        cv.create_rectangle(x, y, x + w, y + h, fill="#2a2a32", outline="#555")
        cy = y + h / 2
        ppu = h / float(span)                            # span = units visible on the tape
        lo_v = val - span / 2
        first = int(lo_v // step) * step
        v = first
        while v < val + span / 2:
            py = cy - (v - val) * ppu
            if y + 24 < py < y + h - 24:
                cv.create_line(x + w - 14, py, x + w, py, fill=INK)
                cv.create_text(x + w - 18, py, anchor="e", text=f"{v:.0f}", fill=INK, font=("Consolas", 9))
            v += step
        ty = cy - (target - val) * ppu
        ty = max(y + 6, min(y + h - 6, ty))
        cv.create_polygon(x, ty - 7, x + 10, ty, x, ty + 7, fill=ACCENT)
        cv.create_rectangle(x + 2, cy - 14, x + w - 2, cy + 14, fill=PANEL, outline=ACCENT, width=2)
        cv.create_text(x + w / 2, cy, text=f"{val:.0f}", fill=INK, font=("Consolas", 14, "bold"))
        cv.create_text(x + w / 2, y + 12, text=label, fill="#aaa", font=("Segoe UI", 9))
        cv.create_text(x + w / 2, y + h - 10, text=f"tgt {target:.0f}", fill=ACCENT, font=("Consolas", 9))

    def _forces(self, s, f, x, y, w, h):
        """Side view of the plane with lift, weight, thrust and drag arrows scaled to the largest."""
        cv = self.cv
        cv.create_rectangle(x, y, x + w, y + h, fill="#2a2a32", outline="#555")
        cv.create_text(x + w / 2, y + 12, text="Forces (lbf)", fill="#aaa", font=("Segoe UI", 9))
        lift = f["forces/fwz-aero-lbs"]
        drag = f["forces/fwx-aero-lbs"]
        thrust = f["propulsion/engine/thrust-lbs"]
        weight = f["inertia/weight-lbs"]
        g = f["accelerations/Nz"]
        big = max(lift, drag, thrust, weight, 1.0)
        scale = 75 / big
        cx, cy = x + w / 2, y + 130
        pitch = math.radians(s["pitch"])
        cos, sin = math.cos(pitch), math.sin(pitch)

        def body(px, py):                                # plane body axes: px forward, py up
            return cx + px * cos - py * sin, cy - (px * sin + py * cos)

        # plane silhouette
        pts = [body(40, 0), body(10, 8), body(-35, 8), body(-45, 22), body(-50, 22), body(-45, 0),
               body(-35, -6), body(10, -6)]
        cv.create_polygon(*sum(map(list, pts), []), fill="#ddd", outline="#999")
        cv.create_line(*body(5, 2), *body(-20, 2), fill="#999", width=5)   # wing

        def arrow(dx, dy, color, name, val):
            if abs(val) < 1:
                return
            x1, y1 = cx, cy
            x2, y2 = cx + dx, cy + dy
            cv.create_line(x1, y1, x2, y2, fill=color, width=3, arrow=tk.LAST, arrowshape=(10, 12, 5))
            cv.create_text(x2 + (12 if dx >= 0 else -12), y2 + (12 if dy >= 0 else -12),
                           text=f"{name} {val:.0f}", fill=color, font=("Consolas", 9))

        # lift is perpendicular to the flight path, drag along it; approximate with body axes
        arrow(-sin * lift * scale, -cos * lift * scale, "#7CFC00", "L", lift)
        arrow(0, weight * scale, "#ff8c42", "W", weight)
        arrow(cos * thrust * scale, -sin * thrust * scale, "#4dd0e1", "T", thrust)
        arrow(-cos * drag * scale, sin * drag * scale, WARN, "D", drag)

        rows = [("alpha", f"{s['alpha']:5.1f}°", WARN if s["stall"] else INK),
                ("G load", f"{g:5.2f}", INK),
                ("V/S", f"{f['velocities/h-dot-fps'] * 60:+6.0f} fpm", INK),
                ("q", f"{f['aero/qbar-psf']:5.1f} psf", INK),
                ("RPM", f"{f['propulsion/engine/engine-rpm']:5.0f}", INK),
                ("L/W", f"{lift / max(weight, 1):5.2f}", INK)]
        for i, (k, v, colour) in enumerate(rows):
            yy = y + h - 20 - (len(rows) - 1 - i) * 18
            cv.create_text(x + 10, yy, anchor="w", text=k, fill="#aaa", font=("Consolas", 10))
            cv.create_text(x + w - 10, yy, anchor="e", text=v, fill=colour, font=("Consolas", 10))

    def _controls(self, f, x, y, w, h):
        cv = self.cv
        cv.create_rectangle(x, y, x + w, y + h, fill="#2a2a32", outline="#555")
        cv.create_text(x + w / 2, y + 12, text="Controls (what the autopilot is doing)", fill="#aaa", font=("Segoe UI", 9))
        bars = [("elevator", f["fcs/elevator-cmd-norm"], True),
                ("aileron", f["fcs/aileron-cmd-norm"], True),
                ("rudder", f["fcs/rudder-cmd-norm"], True),
                ("throttle", f["fcs/throttle-cmd-norm"], False)]
        bw = w - 150
        for i, (name, v, signed) in enumerate(bars):
            yy = y + 36 + i * 28
            x0 = x + 90
            cv.create_text(x + 10, yy, anchor="w", text=name, fill=INK, font=("Consolas", 10))
            cv.create_rectangle(x0, yy - 8, x0 + bw, yy + 8, outline="#666")
            if signed:
                mid = x0 + bw / 2
                cv.create_line(mid, yy - 8, mid, yy + 8, fill="#888")
                cv.create_rectangle(mid, yy - 6, mid + v * bw / 2, yy + 6, fill=ACCENT, outline="")
            else:
                cv.create_rectangle(x0, yy - 6, x0 + v * bw, yy + 6, fill="#4dd0e1", outline="")
            cv.create_text(x0 + bw + 8, yy, anchor="w", text=f"{v:+.2f}", fill=INK, font=("Consolas", 10))
        p, r, yaw = self.sim.servo_offsets()
        cv.create_text(x + 10, y + h - 12, anchor="w", fill="#aaa", font=("Consolas", 10),
                       text=f"to Uno:  P{p:+3.0f}  R{r:+3.0f}  Y{yaw:+3.0f}")

    def _banner(self, s):
        cv = self.cv
        y = 530
        cap = self.info.get("captain_age")
        uno = self.info.get("uno")
        bits = [f"t {s['time']:6.1f}s"]
        if cap is not None:
            bits.append(f"captain {cap:4.1f}s ago" + ("  STALE" if cap > config.CAPTAIN_STALE_S else ""))
        if uno is not None:
            bits.append("uno OK" if uno else "uno DOWN")
        cv.create_text(20, y, anchor="nw", text="   ".join(bits), fill="#aaa", font=("Consolas", 10))
        callout = self.info.get("callout") or ""
        if callout:
            cv.create_text(20, y + 22, anchor="nw", text=f"Captain: “{callout}”", fill=ACCENT,
                           font=("Segoe UI", 12, "italic"), width=440)
        flags = []
        if s["stall"]:
            flags.append("STALL")
        if self.info.get("crashed"):
            flags.append("CRASHED")
        if self.info.get("kick", 0) > s["time"]:
            flags.append("RUDDER KICK")
        if flags:
            cv.create_text(W - 20, y + 10, anchor="ne", text="   ".join(flags), fill=WARN,
                           font=("Segoe UI", 16, "bold"))
