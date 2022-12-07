from typing import Dict

from .util import SerializationType


class Meter:
    def __init__(self, name: str, min_value: int, max_value: int):
        self.name: str = name
        self.min_value: int = min_value
        self.max_value: int = max_value
        self._value: int = self.min_value

    def __repr__(self):
        return f"Meter({self.name}, [{self.min_value}, {self.max_value}], {self.value})"

    def __eq__(self, other: "Meter") -> bool:
        return (
            self.name == other.name
            and self.min_value == other.min_value
            and self.max_value == other.max_value
            and self.value == other.value
        )

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int):
        if self.is_valid(value):
            raise ValueError(f"value must be in [{self.min_value}, {self.max_value}]")
        self._value = value

    def reset(self):
        self.value = self.min_value

    def is_valid(self, value: int) -> bool:
        return value < self.min_value or value > self.max_value

    # -----------------------------------------------------------

    def to_dict(self) -> Dict:
        result = dict(
            name=self.name,
            min_value=self.min_value,
            max_value=self.max_value,
            value=self.value
        )
        return result

    @classmethod
    def from_dict(cls, d: Dict, method: SerializationType = SerializationType.Status) -> "Meter":
        name = d["name"]
        min_value = d["min_value"]
        max_value = d["max_value"]
        meter = Meter(
            name=name,
            min_value=min_value,
            max_value=max_value,
        )
        if method == SerializationType.Status:
            value = d["value"]
            meter.value = value
        return meter
