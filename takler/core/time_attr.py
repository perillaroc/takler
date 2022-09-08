import datetime

from .calendar import Calendar


class TimeAttribute:
    def __init__(self, time: datetime.time):
        self.time: datetime.time = time
        self.free: bool = False

    def is_free(self, calendar: Calendar) -> bool:
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
        self.free = True

    def clear_free(self):
        self.free = False

    def calendar_changed(self, calendar: Calendar):
        if self.free:
            return
        if self.is_free(calendar):
            self.set_free()
