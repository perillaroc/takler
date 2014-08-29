from node_state import NodeState
from node_trigger import NodeTrigger


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

    def set_state(self, some_state):
        """Set node state to some state, and handle the state change.
        """
        self.state = some_state
        # swim stats
        self.swim_state_change()
        # resolve dependency from root.
        self.get_root().resolve_dependency()

    def swim_state_change(self):
        """Apply current node's state to all its ancestors without doing anything.

        Swim current state up. This method can only be called in set_state and itself.
        """
        node_state = NodeState.compute_node_state(self)

        if node_state is not self.state:
            self.state = node_state

        if self.parent is not None:
            self.parent.swim_state_change()
        return

    def sink_state_change(self, state):
        """Apply the state change to all its descendants without doing anything.

        Sink current state down. This method can only be called in set_state and itself.
        """
        self.state = state
        for a_node in self.children:
            a_node.sink_state_change(state)

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
        """Resolve node dependency for this node and all its children. Submit those satisfy conditions.
        """
        if not self.__resolve_node_dependency():
            return False
        for a_child in self.children:
            a_child.resolve_dependency()
        return True

    def __resolve_node_dependency(self):
        """Resolve dependency of this node only and submit it when true.
        """
        if self.state == NodeState.Complete or self.state >= NodeState.Submitted:
            return False

        if not self.evaluate_trigger():
            return False

        if len(self.children) == 0:
            self.run()

        return True

    def queue(self):
        """Re-queue this node and all its children nodes.

        Change stats of this nodes to Queued, and resolve dependency once.
        """
        print "{node} queue".format(node=self)
        self.sink_state_change(NodeState.Queued)
        self.set_state(NodeState.Submitted)

    def run(self):
        """Execute the script of the node. Change state to Submitted.

        This method is usually called by resolve_dependency.
        """
        print "{node} submitted".format(node=self)
        self.set_state(NodeState.Submitted)

    def init(self):
        """Change state to Active. This is usually called form running script via a client command.
        """
        print "{node} init".format(node=self)
        self.set_state(NodeState.Active)

    def complete(self):
        print "{node} complete".format(node=self)
        self.set_state(NodeState.Complete)

    def abort(self):
        print "{node} abort".format(node=self)
        self.set_state(NodeState.Aborted)

    def kill(self):
        print "{node} kill".format(node=self)

    # node access methods
    def is_leaf_node(self):
        if len(self.children) == 0:
            return True
        else:
            return False

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

    def get_root(self):
        root = self
        while root.parent is not None:
            root = root.parent
        return root


def pre_order_travel(root_node, visitor):
    visitor.visit(root_node)
    for child_node in root_node.children:
        visitor.before_visit_child()
        pre_order_travel(child_node, visitor)
        visitor.after_visit_child()


if __name__ == "__main__":
    suite1 = Node("suite1")

    family1 = suite1.append_child("family1")
    task1 = family1.append_child("task1")
    task2 = family1.append_child("task2")
    task2.add_trigger("task1 == complete")

    family2 = suite1.append_child("family2")
    family2.add_trigger("family1 == complete")

    task3 = family2.append_child("task3")

    family3 = family2.append_child("family3")
    family3.add_trigger("task3 == complete")
    task4 = family3.append_child("task4")

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
                place_holder="  " * self.level,
                node_name=node.name,
                node_state=state,
                trigger=("Trigger: [" + node.trigger.exp_str + "] " if node.trigger is not None else "Trigger: ") +
                        str(node.evaluate_trigger()))

        def before_visit_child(self):
            self.level += 1

        def after_visit_child(self):
            self.level -= 1

    pre_order_travel(suite1, SimplePrintVisitor())

    suite1.queue()
    pre_order_travel(suite1, SimplePrintVisitor())

    task1.init()
    pre_order_travel(suite1, SimplePrintVisitor())

    task1.complete()
    pre_order_travel(suite1, SimplePrintVisitor())

    task2.init()
    pre_order_travel(suite1, SimplePrintVisitor())

    task2.complete()
    pre_order_travel(suite1, SimplePrintVisitor())

    task3.init()
    pre_order_travel(suite1, SimplePrintVisitor())

    task3.complete()
    pre_order_travel(suite1, SimplePrintVisitor())

    task4.init()
    pre_order_travel(suite1, SimplePrintVisitor())

    task4.complete()
    pre_order_travel(suite1, SimplePrintVisitor())

    task2.run()
    pre_order_travel(suite1, SimplePrintVisitor())

    family2.queue()
    pre_order_travel(suite1, SimplePrintVisitor())

    family1.queue()
    pre_order_travel(suite1, SimplePrintVisitor())

    task1.abort()
    pre_order_travel(suite1, SimplePrintVisitor())
