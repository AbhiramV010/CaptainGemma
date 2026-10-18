"""Serial link to the Uno. The only module that writes to the COM port."""
import threading
import time

import serial

import config


class Bridge:
    def __init__(self, port=config.COM_PORT, baud=config.BAUD):
        self.port = port
        self.baud = baud
        self.ser = None
        self.target = {"Y": 0, "P": 0, "R": 0}
        self.sent = {}
        self._crash_pending = False
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._last_retry = 0.0
        self._thread = threading.Thread(target=self._run, daemon=True)

    # --- public -------------------------------------------------------------
    def start(self):
        self._connect()
        self._thread.start()

    def set(self, pitch, roll, yaw):
        lim = config.LIMIT_DEG
        with self._lock:
            self.target = {
                "P": int(round(max(-lim, min(lim, pitch)))),
                "R": int(round(max(-lim, min(lim, roll)))),
                "Y": int(round(max(-lim, min(lim, yaw)))),
            }

    def crash(self):
        """Ask the Uno to beep twice. Sent once, as soon as the port is up."""
        self._crash_pending = True

    @property
    def connected(self):
        return self.ser is not None and self.ser.is_open

    def close(self):
        self._stop.set()
        self._thread.join(timeout=1.0)
        if self.ser:
            try:
                for axis in "YPR":
                    self.ser.write(f"{axis}0\n".encode())
                self.ser.close()
            except serial.SerialException:
                pass
            self.ser = None

    # --- internals ----------------------------------------------------------
    def _connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=0.1)
            time.sleep(2.0)             # the Uno resets when the port opens
            self.ser.reset_input_buffer()
            self.sent = {}              # resend everything after a reset
            print(f"UNO CONNECTED on {self.port}")
            return True
        except serial.SerialException as e:
            self.ser = None
            print(f"UNO DISCONNECTED ({e.__class__.__name__}: {e})")
            return False

    def _run(self):
        period = 1.0 / config.BRIDGE_HZ
        while not self._stop.is_set():
            t0 = time.monotonic()
            if not self.connected:
                if t0 - self._last_retry >= 1.0:
                    self._last_retry = t0
                    self._connect()
            else:
                if self._crash_pending:
                    try:
                        self.ser.write(b"C\n")
                        self._crash_pending = False
                    except serial.SerialException:
                        pass                     # the write below will detect the drop
                with self._lock:
                    target = dict(self.target)
                for axis in "YPR":
                    v = target[axis]
                    if self.sent.get(axis) != v:         # only send on a change of >= 1°
                        try:
                            self.ser.write(f"{axis}{v}\n".encode())
                            self.sent[axis] = v
                        except serial.SerialException:
                            print("UNO DISCONNECTED")
                            try:
                                self.ser.close()
                            except Exception:
                                pass
                            self.ser = None
                            break
            dt = time.monotonic() - t0
            if dt < period:
                time.sleep(period - dt)
