class NodeState(object):
    Unknown = 1
    Queued = 2
    Submitted = 3
    Active = 4
    Complete = 5
    Aborted = 6

    state_mapper = {
        "unknown": Unknown,
        "queued":  Queued,
        "submitted": Submitted,
        "active": Active,
        "complete": Complete,
        "aborted": Aborted
    }

    def __init__(self):
        self.node_state = self.Unknown

    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

    @staticmethod
    def to_state(state_str):
        return NodeState.state_mapper[state_str.lower()]


class NodeTrigger(object):

    def __init__(self, trigger_str, parent):
        self.exp_str = trigger_str
        self.node = None
        self.state = None
        self.operator = None
        self._parent_node = parent
        self.parse()

    @property
    def parent_node(self):
        return self._parent_node

    @parent_node.setter
    def parent_node(self, value):
        self._parent_node = value

    def parse(self):
        tokens = self.exp_str.split()
        if len(tokens) == 3:
            left_part = tokens[0]
            trigger_operator = tokens[1]
            right_part = tokens[2]

            self.node = self.parent_node.find_node(left_part)
            if self.node is None:
                raise Exception("trigger %s is not supported" % self.exp_str)
            self.operator = trigger_operator
            self.state = NodeState.to_state(right_part)
        else:
            raise Exception("trigger %s is not supported" % self.exp_str)

    def evaluate(self):
        if self.operator == "==":
            return self.node.state == self.state


class Node(object):
    def __init__(self, node_name=""):
        self.parent = None
        self.children = list()

        self.state = NodeState.Unknown
        self.name = node_name
        self.rid = ""
        self.path = ""

        self.trigger = None

    def __str__(self):
        return "[Node] {node_name}".format(node_name=self.name)

    def append_child(self, child_name):
        child_node = Node(child_name)
        child_node.parent = self
        self.children.append(child_node)
        return child_node

    def add_trigger(self, trigger_str):
        self.trigger = NodeTrigger(trigger_str, self)

    def evaluate_trigger(self):
        if self.trigger is None:
            return True
        return self.trigger.evaluate()

    def resolve_dependency(self):
        pass

    def find_node(self, node_str):
        # Currently, we just use a node name
        result_node = None
        if self.parent is None:
            return None
        if len(self.parent.children) == 0:
            return result_node
        for a_node in self.parent.children:
            if a_node.name == node_str:
                result_node = a_node
                break
        return result_node


def pre_order_travel(root_node, visitor):
    visitor.visit(root_node)
    for child_node in root_node.children:
        visitor.before_visit_child()
        pre_order_travel(child_node, visitor)
        visitor.after_visit_child()

if __name__ == "__main__":
    root = Node("suite")

    family1 = root.append_child("family1")
    task1 = family1.append_child("task1")
    family1.append_child("task2").add_trigger("task1 == complete")

    family2 = root.append_child("family2")
    family2.add_trigger("family1 == complete")

    family2.append_child("task3")

    family3 = family2.append_child("family3")
    family3.add_trigger("task3 == complete")
    family3.append_child("task4")

    level = 0

    class SimplePrintVisitor(object):
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

            print "{place_holder}|- {node_name} [{node_state}] {trigger}".format(
                place_holder="  "*self.level,
                node_name=node.name,
                node_state=state,
                trigger=("[" + node.trigger.exp_str+"] " if node.trigger is not None else "") +
                        str(node.evaluate_trigger()))

        def before_visit_child(self):
            self.level += 1

        def after_visit_child(self):
            self.level -= 1

    pre_order_travel(root, SimplePrintVisitor())