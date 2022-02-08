from typing import Union, Optional


class Parameter(object):
    def __init__(self, name: str, value: Optional[Union[str, int, float]] = None):
        self.name = name
        self.value = value
