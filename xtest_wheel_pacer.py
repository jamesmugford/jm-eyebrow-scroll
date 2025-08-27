# ---- add these imports at the top of your file (Linux path) ----
import threading
import os

# ---- buffered scroller for X11 (python-xlib, no subprocesses) ----
class XTestWheelPacer:
    """
    Convert a continuous 'amount' signal into paced wheel ticks without
    spawning subprocesses. X11 only (display must be available).
    """
    def __init__(self,
                 min_rate=4.0,            # ticks/sec just over threshold
                 max_rate=40.0,           # ticks/sec at strong motion
                 ease_power=2.2,          # curve shaping (>1 = gentler near zero)
                 hysteresis=0.02,         # deadzone to avoid jitter
                 max_ticks_per_flush=6,   # cap per flush to avoid bursts
                 flush_hz=50,             # how often we flush (20ms)
                 max_input=1.0):          # value that maps to max_rate
        from Xlib import X, display
        self._X = X
        self._d = display.Display()
        self._root = self._d.screen().root

        self.min_rate = float(min_rate)
        self.max_rate = float(max_rate)
        self.ease_power = float(ease_power)
        self.hysteresis = float(hysteresis)
        self.max_ticks_per_flush = int(max_ticks_per_flush)
        self.flush_dt = 1.0 / float(flush_hz)
        self.max_input = float(max_input)

        self._amount = 0.0        # latest signed amount (thread-safe via lock)
        self._accum = 0.0         # fractional ticks
        self._dir = 0             # last sign
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def set_amount(self, amount: float):
        with self._lock:
            self._amount = float(amount)

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=1.0)

    # --- internals ---
    def _emit_ticks(self, sign: int, n: int):
        btn = 4 if sign > 0 else 5  # 4=up, 5=down
        for _ in range(n):
            self._root.fake_input(self._X.ButtonPress, btn)
            self._root.fake_input(self._X.ButtonRelease, btn)
        # one sync for the batch
        self._d.sync()

    def _rate_for_amount(self, a: float) -> float:
        if abs(a) < self.hysteresis:
            return 0.0
        mag = min(1.0, abs(a) / self.max_input)
        eased = mag ** self.ease_power
        return self.min_rate + (self.max_rate - self.min_rate) * eased

    def _loop(self):
        import time
        last = time.monotonic()
        while not self._stop.is_set():
            now = time.monotonic()
            dt = now - last
            if dt < self.flush_dt:
                # sleep the remaining slice to hit ~flush_hz
                time.sleep(self.flush_dt - dt)
                continue
            last = now

            with self._lock:
                a = self._amount

            # compute desired rate & direction
            rate = self._rate_for_amount(a)
            if rate <= 0.0:
                self._accum = 0.0
                self._dir = 0
                continue

            sign = 1 if a > 0 else -1
            if sign != self._dir:
                self._accum = 0.0  # avoid dumping ticks in wrong dir
                self._dir = sign

            # accumulate ticks and emit an integer portion, capped per flush
            self._accum += rate * self.flush_dt
            ticks = int(self._accum)
            if ticks > 0:
                if ticks > self.max_ticks_per_flush:
                    ticks = self.max_ticks_per_flush
                    # keep leftover in the accumulator
                    self._accum -= ticks
                else:
                    self._accum -= ticks
                self._emit_ticks(sign, ticks)
