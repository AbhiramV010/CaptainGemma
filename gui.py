import csv
import os
import time
import tkinter as tk
import serial

import config

# Manual test mode only. Do not run at the same time as main.py.
PORT = config.COM_PORT
BAUD = config.BAUD
RANGE = config.LIMIT_DEG
CSV_PATH = config.PRY_CSV

ser = serial.Serial(PORT, BAUD, timeout=0.1)
time.sleep(2)          # the Uno resets when the port opens

root = tk.Tk()
root.title("Pilot Control: PRY")

def send(axis, value):
    ser.write(f"{axis}{int(float(value))}\n".encode())

def reset():
    for s in sliders.values():
        s.set(0)
    for axis in "YPR":
        send(axis, 0)
    status.config(text="Centred")

def test_buzzer():
    ser.write(b"C\n")
    status.config(text="Buzzer test sent")

def save_pry():
    is_new = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["timestamp", "pitch_deg", "roll_deg", "yaw_deg"])
        w.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            int(sliders["P"].get()),
            int(sliders["R"].get()),
            int(sliders["Y"].get()),
        ])
    status.config(text=f"Saved to {CSV_PATH}")

sliders = {}
for name, axis in [("Pitch", "P"), ("Roll", "R"), ("Yaw", "Y")]:
    s = tk.Scale(root, from_=-RANGE, to=RANGE, orient="horizontal", length=500,
                 label=f"{name} (°)", resolution=1,
                 command=lambda v, a=axis: send(a, v))
    s.set(0)
    s.pack(padx=10, pady=5)
    sliders[axis] = s

btns = tk.Frame(root)
btns.pack(pady=10)
tk.Button(btns, text="Centre all", command=reset).pack(side="left", padx=5)
tk.Button(btns, text="Save PRY", command=save_pry).pack(side="left", padx=5)
tk.Button(btns, text="Test buzzer", command=test_buzzer).pack(side="left", padx=5)

status = tk.Label(root, text=f"CSV: {CSV_PATH}")
status.pack(pady=5)

def on_close():
    ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()