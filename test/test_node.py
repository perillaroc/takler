import os
from takler.node import Node
from takler.node_state import NodeState
from takler.visitor import SimplePrintVisitor, pre_order_travel
from takler.variable import VariableName

import unittest


class TestNode(unittest.TestCase):
    def setUp(self):
        """Build a node tree for test:

        |- suite1 [Unknown] Trigger: True
            |- family1 [Unknown] Trigger: True
                |- task1 [Unknown] Trigger: True
                |- task2 [Unknown] Trigger: [task1 == complete] False
            |- family2 [Unknown] Trigger: [family1 == complete] False
                |- task3 [Unknown] Trigger: True
                |- family3 [Unknown] Trigger: [task3 == complete] False
                    |- task4 [Unknown] Trigger: True
        """
        self.suite1 = Node("suite1")
        self.suite1.var_map[VariableName.SUITE_HOME] = os.path.dirname(__file__)

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

    def test_get_node_path(self):
        self.assertEqual(self.suite1.get_node_path(), "/suite1")
        self.assertEqual(self.family1.get_node_path(), "/suite1/family1")
        self.assertEqual(self.task1.get_node_path(), "/suite1/family1/task1")
        self.assertEqual(self.task4.get_node_path(), "/suite1/family2/family3/task4")

    def test_find_node(self):
        self.assertEqual(self.task1.find_node("task2"), self.task2)
        self.assertEqual(self.task2.find_node("task1"), self.task1)
        self.assertEqual(self.family1.find_node("family2"), self.family2)
        self.assertEqual(self.family2.find_node("family1"), self.family1)
        self.assertEqual(self.task3.find_node("family3"), self.family3)
        self.assertEqual(self.family1.find_node("family2/task3"), self.task3)

        self.assertEqual(self.task1.find_node("../family2"), self.family2)
        self.assertEqual(self.task1.find_node("../family2/task3"), self.task3)

        self.assertEqual(self.task1.find_node("/suite1"), self.suite1)
        self.assertEqual(self.task1.find_node("/suite1/family2/task3"), self.task3)

        self.assertIsNone(self.task1.find_node("/suite1/family3"))
        self.assertIsNone(self.task1.find_node("task3"))
        self.assertIsNone(self.task4.find_node("../family1/task1"))

    def test_to_dict(self):
        suite_dict = self.suite1.to_dict()
        print suite_dict
        suite2 = Node.create_from_dict(suite_dict)
        pre_order_travel(suite2, SimplePrintVisitor())

    def test_to_json(self):
        suite_json = self.suite1.to_json()
        print suite_json
        suite2 = Node.create_from_json(suite_json)
        pre_order_travel(suite2, SimplePrintVisitor())

    def test_node_append(self):
        print "[test_node_append] start"
        new_node = Node("task2-1")
        self.family2.append_child_node(new_node)
        self.family2.append_child("task2-2")
        self.assertIsNotNone(self.suite1.find_node("/suite1/family2/task2-1"))
        self.assertIsNotNone(self.suite1.find_node("/suite1/family2/task2-2"))
        print "[test_node_append] end"

    def test_node_deletion(self):
        print "before node delete"
        pre_order_travel(self.suite1, SimplePrintVisitor())
        self.family1.delete_children()
        print "after node delete"
        self.assertEqual(self.family1.children, list())
        pre_order_travel(self.suite1, SimplePrintVisitor())

    def test_find_parent_variable(self):
        test_string = 'test_string'
        self.suite1.var_map['test_string'] = test_string
        self.assertEqual(self.task1.find_parent_variable("test_string"), test_string)
        self.assertIsNone(self.task1.find_parent_variable("null_string"))
        self.assertEqual(self.task1.find_parent_variable(VariableName.NODE_PATH), "/suite1/family1/task1")
        self.assertEqual(self.family1.find_parent_variable(VariableName.NODE_PATH), "/suite1/family1")
        self.assertEqual(self.suite1.find_parent_variable(VariableName.NODE_PATH), "/suite1")

    def test_substitute_variable(self):
        self.assertEqual(self.task1.substitute_variable("python $script_path$"),
                         "python {script_path}".format(script_path=self.task1.get_script_path()))
        self.assertEqual(self.task1.substitute_variable("$script_path$ hello $node_path$"),
                         "{script_path} hello {node_path}".format(
                             script_path=self.task1.get_script_path(),
                             node_path=self.task1.get_node_path()
                         ))


if __name__ == "__main__":
    unittest.main()