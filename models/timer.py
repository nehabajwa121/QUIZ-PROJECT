"""
models/timer.py

A simple countdown timer built on top of Tkinter's `after` scheduling.
Decoupled from any specific widget so it can be reused or tested.
"""

from typing import Callable, Optional


class Timer:
    """Countdown timer that ticks once per second using a Tk root's event loop."""

    def __init__(
        self,
        tk_root,
        duration: int,
        on_tick: Callable[[int], None],
        on_timeout: Callable[[], None],
    ):
        """
        tk_root: any Tkinter widget/root with an `.after()` method
        duration: starting number of seconds
        on_tick: callback invoked every second with remaining seconds
        on_timeout: callback invoked once when the timer reaches zero
        """
        self._root = tk_root
        self._duration = duration
        self._remaining = duration
        self._on_tick = on_tick
        self._on_timeout = on_timeout
        self._job: Optional[str] = None
        self._paused = False
        self._running = False

    def start(self) -> None:
        self._remaining = self._duration
        self._running = True
        self._paused = False
        self._on_tick(self._remaining)
        self._schedule_next()

    def _schedule_next(self) -> None:
        if self._running and not self._paused:
            self._job = self._root.after(1000, self._tick)

    def _tick(self) -> None:
        if not self._running or self._paused:
            return
        self._remaining -= 1
        self._on_tick(self._remaining)
        if self._remaining <= 0:
            self._running = False
            self._on_timeout()
        else:
            self._schedule_next()

    def pause(self) -> None:
        self._paused = True
        self._cancel_job()

    def resume(self) -> None:
        if self._running and self._paused:
            self._paused = False
            self._schedule_next()

    def stop(self) -> None:
        self._running = False
        self._paused = False
        self._cancel_job()

    def _cancel_job(self) -> None:
        if self._job is not None:
            try:
                self._root.after_cancel(self._job)
            except Exception:
                pass
            self._job = None

    @property
    def remaining(self) -> int:
        return self._remaining

    @property
    def is_paused(self) -> bool:
        return self._paused
