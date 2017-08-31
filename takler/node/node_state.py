# coding: utf-8

from enum import Enum


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


class NodeState(OrderedEnum):
    unknown = 1
    complete = 2
    queued = 3
    submitted = 4
    active = 5
    aborted = 6

    @staticmethod
    def compute_node_state(node):
        if len(node.children) == 0:
            return node.state
        state = NodeState.unknown
        for a_child in node.children:
            child_node_state = NodeState.compute_node_state(a_child)
            if child_node_state > state:
                state = child_node_state
        return state


