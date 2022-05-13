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
    def __init__(self, stream: IO):
        NodeVisitor.__init__(self)
        self.level: int = 0
        self.stream: IO = stream

    def visit(self, node: Node):
        place_holder = "  " * self.level
        node_name = node.name
        node_state = node.state.node_status.name
        self.stream.write(f"{place_holder}|- {node_name} [{node_state}]\n")
        pre_spaces = " " * len(f"{place_holder}|- ")
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
