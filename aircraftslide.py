import time
import tkinter as tk
import serial

PORT = "COM5"          # change to your Uno's port
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=0.1)
time.sleep(2)          # the Uno resets when the port opens

root = tk.Tk()
root.title("Pilot Control")

def send(axis, value):
    ser.write(f"{axis}{int(float(value))}\n".encode())

def reset():
    for s in sliders.values():
        s.set(0)
    for axis in "YPR":
        send(axis, 0)

sliders = {}
for name, axis in [("Yaw", "Y"), ("Pitch", "P"), ("Roll", "R")]:
    s = tk.Scale(root, from_=-20, to=20, orient="horizontal", length=400,
                 label=f"{name} (°)", resolution=1,
                 command=lambda v, a=axis: send(a, v))
    s.set(0)
    s.pack(padx=10, pady=5)
    sliders[axis] = s

tk.Button(root, text="Centre all", command=reset).pack(pady=10)

def on_close():
    ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()