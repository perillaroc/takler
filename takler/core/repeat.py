from abc import ABC, abstractmethod
from typing import Union, Optional, Dict
from datetime import datetime, date, timedelta

from .parameter import Parameter


class RepeatBase(ABC):
    def __init__(self, name: str):
        self.name = name

    @property
    @abstractmethod
    def start(self):
        ...

    @property
    @abstractmethod
    def end(self):
        ...

    @property
    @abstractmethod
    def step(self):
        ...

    @property
    @abstractmethod
    def value(self):
        ...

    @value.setter
    @abstractmethod
    def value(self, value):
        ...

    @abstractmethod
    def valid(self) -> bool:
        return True

    @abstractmethod
    def increment(self) -> bool:
        return True

    @abstractmethod
    def change(self, value):
        ...

    @abstractmethod
    def reset(self):
        ...

    @abstractmethod
    def generated_parameters(self) -> Dict[str, Parameter]:
        ...


class RepeatDate(RepeatBase):
    DATE_FORMAT = "%Y%m%d"

    def __init__(self, name: str, start_date: Union[str, int], end_date: Union[str, int], step: int = 1):
        super(RepeatDate, self).__init__(name=name)
        self.start_date: date = datetime.strptime(str(start_date), RepeatDate.DATE_FORMAT).date()
        self.end_date: date = datetime.strptime(str(end_date), RepeatDate.DATE_FORMAT).date()
        self.step_day: timedelta = timedelta(days=step)
        self._value: date = self.start_date

    @property
    def start(self) -> int:
        return int(self.start_date.strftime(RepeatDate.DATE_FORMAT))

    @property
    def end(self) -> int:
        return int(self.end_date.strftime(RepeatDate.DATE_FORMAT))

    @property
    def step(self) -> int:
        return int(self.step_day / timedelta(days=1))

    @property
    def value(self) -> int:
        return int(self._value.strftime(RepeatDate.DATE_FORMAT))

    @value.setter
    def value(self, value: Union[str, int, date]):
        if isinstance(value, int):
            value = str(value)
        if isinstance(value, str):
            value = datetime.strptime(value, RepeatDate.DATE_FORMAT).date()
        self._value = value

    def valid(self) -> bool:
        return self._value <= self.end_date

    def increment(self) -> bool:
        value = self._value + self.step_day
        if value <= self.end_date:
            self.value = value
            return True
        else:
            return False

    def change(self, value: Union[str, int, date]):
        if isinstance(value, int):
            value = str(value)
        if isinstance(value, str):
            value = datetime.strptime(value, RepeatDate.DATE_FORMAT).date()

        # check range
        if value < self.start_date or value > self.end_date:
            raise ValueError(f"value must be in range [{self.start_date}, {self.end_date}], but current is {value}")

        # check step
        diff = (value - self.start_date) / self.step_day
        if not diff.is_integer():
            raise ValueError(f"value must be in multiply step {self.step} from {self.start_date}, but current is {value}")

        self.value = value

    def reset(self):
        self._value = self.start_date

    def generated_parameters(self) -> Dict[str, Parameter]:
        return {
            self.name: Parameter(self.name, self.value)
        }


class Repeat:
    def __init__(self, r: Optional[RepeatBase] = None):
        self.r = r

    def empty(self) -> bool:
        return self.r is not None

    def clear(self):
        self.r = None

    def start(self):
        return self.r.start

    def end(self):
        return self.r.end

    def step(self):
        return self.r.step

    def value(self):
        return self.r.value

    def valid(self) -> bool:
        return self.r.valid()

    def reset(self):
        return self.r.reset()

    def increment(self):
        return self.r.increment()

    def change(self, value):
        self.r.change(value)

    def set_value(self, value):
        self.r.value = value

    def generated_parameters(self) -> Dict[str, Parameter]:
        return self.r.generated_parameters()
