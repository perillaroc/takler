from takler.node import Node
from takler.node_state import NodeState
import unittest


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


def pre_order_travel(root_node, visitor):
    visitor.visit(root_node)
    for child_node in root_node.children:
        visitor.before_visit_child()
        pre_order_travel(child_node, visitor)
        visitor.after_visit_child()


class TestNode(unittest.TestCase):
    def setUp(self):
        self.suite1 = Node("suite1")

        self.family1 = self.suite1.append_child("family1")
        self.task1 = self.family1.append_child("task1")
        self.task2 = self.family1.append_child("task2")
        self.task2.add_trigger("task1 == complete")

        self.family2 = self.suite1.append_child("family2")
        self.family2.add_trigger("family1 == complete")

        self.task3 = self.family2.append_child("task3")

        self.family3 = self.family2.append_child("family3")
        self.family3.add_trigger("task3 == complete")
        self.task4 = self.family3.append_child("task4")

    def test_create_node_tree(self):
        pre_order_travel(self.suite1, SimplePrintVisitor())

    def test_find_node(self):
        self.assertEqual(self.task1.find_node("task2"), self.task2)
        self.assertEqual(self.task2.find_node("task1"), self.task1)

        self.assertEqual(self.family1.find_node("family2"), self.family2)
        self.assertEqual(self.family2.find_node("family1"), self.family1)

        self.assertEqual(self.task3.find_node("family3"), self.family3)

        self.assertEqual(self.task1.find_node("../family2"), self.family2)
        self.assertEqual(self.family1.find_node("family2/task3"), self.task3)
        self.assertEqual(self.task1.find_node("../family2/task3"), self.task3)

        self.assertEqual(self.task1.find_node("/suite1/family2/task3"), self.task3)

        self.assertIsNone(self.task1.find_node("/suite1/family3"))
        self.assertIsNone(self.task1.find_node("task3"))

    def test_node_operation(self):
        self.suite1.queue()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.task1.init()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.task1.complete()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.task2.init()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.task2.complete()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.task3.init()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.task3.complete()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.task4.init()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.task4.complete()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.task2.run()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.family2.queue()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.family1.queue()
        pre_order_travel(self.suite1, SimplePrintVisitor())

        self.task1.abort()
        pre_order_travel(self.suite1, SimplePrintVisitor())

if __name__ == "__main__":
    unittest.main()