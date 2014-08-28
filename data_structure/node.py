class NodeState(object):
    Unknown = 1
    Queued = 2
    Submitted = 3
    Active = 4
    Complete = 5
    Aborted = 6

    def __init__(self):
        self.node_state = self.Unknown

    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


class Node(object):
    def __init__(self):
        self.parent = None
        self.children = list()

        self.state = NodeState.Unknown
        self.name = ""
        self.rid = ""
        self.path = ""

    def __str__(self):
        return "[Node] {node_name}".format(node_name=self.name)

    def append_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)


def pre_order_travel(root_node, visitor):
    visitor.visit(root_node)
    for child_node in root_node.children:
        visitor.before_visit_child()
        pre_order_travel(child_node, visitor)
        visitor.after_visit_child()

if __name__ == "__main__":
    root = Node()
    root.name = "suite"

    family_1_node = Node()
    family_1_node.name = "family1"

    task_1_node = Node()
    task_1_node.name = "task1"

    task_2_node = Node()
    task_2_node.name = "task2"

    family_1_node.append_child(task_1_node)
    family_1_node.append_child(task_2_node)

    family_2_node = Node()
    family_2_node.name = "family2"

    task_3_node = Node()
    task_3_node.name = "task3"

    family_2_node.append_child(task_3_node)

    family_3_node = Node()
    family_3_node.name = "family3"

    task_4_node = Node()
    task_4_node.name = "task4"

    family_3_node.append_child(task_4_node)

    family_2_node.append_child(family_3_node)

    root.append_child(family_1_node)
    root.append_child(family_2_node)

    level = 0

    class Visitor:
        def __init__(self):
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

            print "{place_holder}|- {node_name} [{node_state}] ".format(
                place_holder=" "*self.level,
                node_name=node.name,
                node_state=state)

        def before_visit_child(self):
            self.level += 1

        def after_visit_child(self):
            self.level -= 1

    pre_order_travel(root, Visitor())