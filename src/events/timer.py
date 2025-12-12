# Imports.
# Local imports.
# External imports.
from attrs import define, field
from typing import Callable, Optional


@define
class Timer:
    """
    A simple day-based countdown timer.

    :param id: Identifier for the timer.
    :type id: str
    :param duration: Total duration of the timer in days.
    :type duration: int
    :param remaining: Days remaining until the timer finishes.
                      If ``None`` is provided, it defaults to ``duration``.
    :type remaining: int or None
    :param on_finish: Optional callback executed once when the timer reaches zero.
                      The callback takes no parameters.
    :type on_finish: Callable[[], None] or None
    """

    id: str = field(default=None)
    duration: int = field(default=0)
    remaining: int = field(default=None)
    on_finish: Optional[Callable[[dict], None]] = field(default=None)
    day: int = field(default=None)
    month: int = field(default=None)
    year: int = field(default=None)

    # Internal flag to avoid calling the callback more than once
    _callback_triggered: bool = field(default=False, init=False)

    def __attrs_post_init__(self):
        """
        Post-initialization hook.

        Ensures that ``remaining`` is properly set and validates the values.
        """
        if self.remaining is None:
            self.remaining = self.duration

        if self.duration < 0:
            raise ValueError("Timer duration must be a non-negative integer.")
        if self.remaining < 0:
            raise ValueError("Timer remaining time must be a non-negative integer.")

    @property
    def date(self) -> tuple[int, int, int]:
        return self.year, self.month,  self.day,

    def tick(self, days: int = 1, **kwargs):
        """
        Advance the timer by a given number of days.

        :param days: Number of days to advance the timer. Must be non-negative.
        :type days: int

        :raises ValueError: If ``days`` is negative.
        """
        if days < 0:
            raise ValueError("tick() cannot advance negative days.")

        if self.is_finished():
            return

        self.day += days
        self.remaining = max(0, self.remaining - days)

        if self.remaining == 0 and not self._callback_triggered:
            self._trigger_finish_callback(**kwargs)

    def reset(self):
        """
        Reset the timer back to its original duration.

        This also resets the internal callback state.
        """
        self.remaining = self.duration
        self._callback_triggered = False

    def is_finished(self) -> bool:
        """
        Check whether the timer has reached zero.

        :return: ``True`` if the timer is finished, otherwise ``False``.
        :rtype: bool
        """
        return self.remaining == 0

    def get_total_duration(self) -> int:
        """
        Get the total duration of the timer.

        :return: Total duration in days.
        :rtype: int
        """
        return self.duration

    def get_remaining(self) -> int:
        """
        Get the number of remaining days.

        :return: Remaining duration in days.
        :rtype: int
        """
        return self.remaining

    def get_elapsed(self) -> int:
        """
        Get how many days have passed since the timer started.

        :return: Elapsed days.
        :rtype: int
        """
        return self.duration - self.remaining

    def progress(self) -> float:
        """
        Get the progress of the timer as a value between 0.0 and 1.0.

        :return: Progress ratio, where ``1.0`` means the timer is complete.
        :rtype: float
        """
        if self.duration == 0:
            return 1.0
        return (self.duration - self.remaining) / self.duration

    def _trigger_finish_callback(self, **kwargs):
        """
        Internal method to safely trigger the ``on_finish`` callback once.

        Exceptions raised by the callback are caught and printed.
        """
        if self.on_finish is not None:
            try:
                self.on_finish(**kwargs)
            except Exception as e:
                print(f"Timer '{self.id}' finish callback raised an exception: {e}")
                input()

        self._callback_triggered = True
