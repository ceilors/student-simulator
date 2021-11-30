from typing import Callable, Optional

import signal
import threading


class Timer:
    def __init__(self, interval: int, handler: Callable):
        """
        Initiate timer instance.

        If `SIGALRM` and `setitimer` are present in `signal` module, then they'll be used,
        otherwise `threading.Timer` will be used.

        ### Parameters
        - `interval` : int
            - timeout in seconds for a `handler` function to be called
        - `handler` : callable
            - function that'll be called after `interval` seconds have passed
        """
        self.interval = interval
        self.handler = handler
        self.running = False

        self.use_signals = hasattr(signal, "setitimer") and hasattr(signal, "SIGALRM")
        if self.use_signals:
            signal.signal(signal.SIGALRM, self.handler)

    def alter_timer(self, interval: Optional[int] = None, handler: Optional[Callable] = None):
        """
        Modify timer instance parameters. If arg is None, correspondent timer parameter won't be changed.

        If `signal` is in use, `setitimer` is modified here as well.

        ### Parameters
        - `*interval` : int, (default `None`)
            - timeout in seconds for a `handler` function to be called
        - `*handler` : callable, (default `None`)
            - function that'll be called after `interval` seconds have passed
        """
        if interval:
            self.interval = interval
        if handler:
            self.handler = handler

        if self.use_signals:
            signal.setitimer(signal.ITIMER_REAL, self.interval, self.interval)

    def step(self):
        """
        Function to be called if `threading` is in use.
        Executes `handler` once and calls `start` to re-launch thread.
        """
        self.running = False
        self.start()
        if self.handler:
            self.handler()

    def start(self):
        """
        Starts timer.
        If `threading` is in use, then initiates new `threading.Timer`.
        Otherwise, calls `signal.setitimer` and exits.

        Won't run if timer is already started.
        """
        if not self.running:
            self.running = True

            if self.use_signals:
                return signal.setitimer(signal.ITIMER_REAL, self.interval, self.interval)

            self.timer = threading.Timer(self.interval, self.step)
            self.timer.start()

    def stop(self):
        """
        Stops timer.
        If `threading` is in use, `cancel`s current timer thread.
        Otherwise, calls `signal.setitimer` with 0 passed as `seconds` argument.

        Does nothing if timer is already stopped.
        """
        if self.use_signals:
            return signal.setitimer(signal.ITIMER_REAL, 0)

        if self.timer:
            self.timer.cancel()
            self.timer = None
        self.running = False
