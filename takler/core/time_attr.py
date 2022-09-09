import datetime

from .calendar import Calendar


class TimeAttribute:
    def __init__(self, time: datetime.time):
        self.time: datetime.time = time
        self.free: bool = False

    def is_free(self, calendar: Calendar) -> bool:
        """
        Check TimeAttribute is satisfied.

        Parameters
        ----------
        calendar

        Returns
        -------
        bool
        """
        if self.free:
            return True

        flow_time = calendar.flow_time
        hour = flow_time.hour
        minute = flow_time.minute
        if hour == self.time.hour and minute == self.time.minute:
            return True
        else:
            return False

    def reset(self):
        self.clear_free()

    def set_free(self):
        """
        Mark TimeAttribute's free flag.
        """
        self.free = True

    def clear_free(self):
        """
        Clear TimeAttribute's free flag.
        """
        self.free = False

    def calendar_changed(self, calendar: Calendar):
        """
        When calendar equals TimeAttribute's time, the TimeAttribute is satisfied.
        After this time, TimeAttribute should always be satisfied until Node is requeue.
        So when calendar changed, TimeAttributes should be checked.
        If it is free, it should be set free to prevent future time check.

        Parameters
        ----------
        calendar
            The calendar of a Flow
        """
        if self.free:
            return
        if self.is_free(calendar):
            self.set_free()
