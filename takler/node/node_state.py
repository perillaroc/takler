# coding: utf-8
from takler.base.ordered_enum import OrderedEnum


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


