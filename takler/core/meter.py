

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
