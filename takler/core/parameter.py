from typing import Union, Optional

# Bunch level
TAKLER_HOST = "TAKLER_HOST"
TAKLER_PORT = "TAKLER_PORT"
TAKLER_HOME = "TAKLER_HOME"

# Flow level
FLOW = "FLOW"
TAKLER_DATE = "TAKLER_DATE"
TAKLER_TIME = "TAKLER_TIME"

TIME = "TIME"
DATE = "DATE"

# Task level
TASK = "TASK"
TAKLER_NAME = "TAKLER_NAME"
TAKLER_RID = "TAKLER_RID"
TAKLER_TRY_NO = "TAKLER_TRY_NO"

TAKLER_TRIES = "TAKLER_TRIES"


class Parameter(object):
    def __init__(self, name: str, value: Optional[Union[str, int, float, bool]] = None):
        self.name: str = name
        self._value: Optional[Union[str, int, float, bool]] = value

    def __repr__(self):
        return f"Parameter<{self.name}, {self.value}>"

    def __eq__(self, other):
        return type(other) == type(self) and other.name == self.name and other.value == self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v: Optional[Union[str, int, float, bool]]):
        self._value = v
