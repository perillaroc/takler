from typing import Union, Optional

# Bunch level
TAKLER_HOST = "TAKLER_HOST"
TAKLER_PORT = "TAKLER_PORT"
TAKLER_HOME = "TAKLER_HOME"

# Flow level
FLOW = "FLOW"
TAKLER_DATE = "TAKLER_DATE"
TAKLER_TIME = "TAKLER_TIME"

# Task level
TASK = "TASK"
TAKLER_NAME = "TAKLER_NAME"


class Parameter(object):
    def __init__(self, name: str, value: Optional[Union[str, int, float, bool]] = None):
        self.name = name  # type: str
        self.value = value  # type: Optional[Union[str, int, float, bool]]

    def __eq__(self, other):
        return type(other) == type(self) and other.name == self.name and other.value == self.value
