from __future__ import annotations

from enum import Enum
from typing import Optional


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class NodeStatus(OrderedEnum):
    unknown = 1
    complete = 2
    queued = 3
    submitted = 4
    active = 5
    aborted = 6


class State(object):
    def __init__(self, node_status: Optional[NodeStatus] = None):
        if node_status is None:
            node_status = NodeStatus.unknown
        self.node_status: NodeStatus = node_status
        self.suspended: bool = False
