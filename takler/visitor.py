import os
from takler.node_state import NodeState


class NodeVisitor(object):
    def __init__(self):
        pass

    def visit(self, node):
        pass

    def before_visit_child(self):
        pass

    def after_visit_child(self):
        pass


class SimplePrintVisitor(NodeVisitor):
    def __init__(self):
        NodeVisitor.__init__(self)
        self.level = 0

    def visit(self, node):
        if node.state == NodeState.Unknown:
            state = "Unknown"
        elif node.state == NodeState.Queued:
            state = "Queued"
        elif node.state == NodeState.Submitted:
            state = "Submitted"
        elif node.state == NodeState.Active:
            state = "Active"
        elif node.state == NodeState.Complete:
            state = "Complete"
        elif node.state == NodeState.Aborted:
            state = "Aborted"
        else:
            state = "Invalid"

        print "{place_holder}|- {node_name} [{node_state}] {trigger}".format(
            place_holder="  " * self.level,
            node_name=node.name,
            node_state=state,
            trigger=("Trigger: [" + node.trigger.exp_str + "] " if node.trigger is not None else "Trigger: ") +
                    str(node.evaluate_trigger()))

    def before_visit_child(self):
        self.level += 1

    def after_visit_child(self):
        self.level -= 1


class MakeDirectoryVisitor(NodeVisitor):
    def __init__(self):
        NodeVisitor.__init__(self)
        pass

    def visit(self, node):
        base_name = os.path.dirname(node.get_script_path())
        if not os.path.isdir(base_name):
            os.makedirs(base_name)


def pre_order_travel(root_node, visitor):
    visitor.visit(root_node)
    for child_node in root_node.children:
        visitor.before_visit_child()
        pre_order_travel(child_node, visitor)
        visitor.after_visit_child()
