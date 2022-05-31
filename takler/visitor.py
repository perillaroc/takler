from typing import IO
from abc import ABC, abstractmethod

from takler.core.node import Node


class NodeVisitor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def visit(self, node: Node):
        pass

    def before_visit_child(self):
        pass

    def after_visit_child(self):
        pass


class SimplePrintVisitor(NodeVisitor):
    def __init__(self):
        NodeVisitor.__init__(self)
        self.level = 0

    def visit(self, node: Node):
        place_holder = "  " * self.level
        node_name = node.name
        node_state = node.state.node_status.name
        print(f"{place_holder}|- {node_name} [{node_state}]")

    def before_visit_child(self):
        self.level += 1

    def after_visit_child(self):
        self.level -= 1


class PrintVisitor(NodeVisitor):
    def __init__(self, stream: IO, show_trigger: bool = False):
        NodeVisitor.__init__(self)
        self.level: int = 0
        self.stream: IO = stream

        self.show_trigger = show_trigger

    def visit(self, node: Node):
        place_holder = "  " * self.level
        node_name = node.name
        node_state = node.state.node_status.name
        if node.is_suspended():
            node_state = f"suspend ({node_state})"
        self.stream.write(f"{place_holder}|- {node_name} [{node_state}]\n")
        pre_spaces = " " * len(f"{place_holder}|- ")

        if self.show_trigger and node.trigger_expression is not None:
            self.stream.write(f"{pre_spaces} trigger {node.trigger_expression.expression_str}\n")

        if len(node.limits) > 0:
            for limit in node.limits:
                self.stream.write(f"{pre_spaces} limit {limit.name} [{limit.value}/{limit.limit}]\n")
        if len(node.events) > 0:
            for event in node.events:
                v = "set" if event.value else "unset"
                self.stream.write(f"{pre_spaces} event {event.name} [{v}]\n")
        if len(node.meters) > 0:
            for meter in node.meters:
                self.stream.write(f"{pre_spaces} meter {meter.name} {meter.min_value} {meter.max_value} [{meter.value}]\n")

    def before_visit_child(self):
        self.level += 1

    def after_visit_child(self):
        self.level -= 1


def pre_order_travel(root_node: Node, visitor: NodeVisitor):
    visitor.visit(root_node)
    for child_node in root_node.children:
        visitor.before_visit_child()
        pre_order_travel(child_node, visitor)
        visitor.after_visit_child()
