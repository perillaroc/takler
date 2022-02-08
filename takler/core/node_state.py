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

    @staticmethod
    def compute_node_state(node) -> NodeStatus:
        if len(node.children) == 0:
            return node.state
        state = NodeStatus.unknown
        for a_child in node.children:
            child_node_state = NodeStatus.compute_node_state(a_child)
            if child_node_state > state:
                state = child_node_state
        return state


class NodeState(object):
    def __init__(self, status: Optional[NodeStatus] = None):
        if status is None:
            status = NodeStatus.unknown
        self.status = status
