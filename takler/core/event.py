from typing import Dict


class Event:
    def __init__(self, name: str, initial_value: bool = False):
        self.name: str = name
        self.initial_value: bool = initial_value
        self._value: bool = self.initial_value

    def __eq__(self, other: "Event") -> bool:
        return(
                self.name == other.name
                and self.value == other.value
                and self.initial_value == other.initial_value
        )

    def __repr__(self):
        if self.value:
            return f"Event({self.name}, set)"
        else:
            return f"Event({self.name}, unset)"

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, value: bool):
        self._value = value

    def reset(self):
        self.value = self.initial_value

    def to_dict(self) -> Dict:
        result = dict(
            name=self.name,
            initial_value=self.initial_value,
            value=self.value,
        )
        return result
