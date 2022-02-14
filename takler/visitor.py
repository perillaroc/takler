from takler.core.node import Node


class NodeVisitor(object):
    def __init__(self):
        pass

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


def pre_order_travel(root_node, visitor):
    visitor.visit(root_node)
    for child_node in root_node.children:
        visitor.before_visit_child()
        pre_order_travel(child_node, visitor)
        visitor.after_visit_child()
