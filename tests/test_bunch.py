import json
import unittest
from takler.node.bunch import Bunch, Suite, Node
from takler.visitor import pre_order_travel, SimplePrintVisitor


class TestBunchCase(unittest.TestCase):
    def setUp(self):
        self.bunch = Bunch()

        self.suite1 = self.bunch.add_suite("suite1")
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

    def tearDown(self):
        pass

    def test_add_suite(self):
        self.suite1.print_suite()

    def test_add_node(self):
        new_node = Node("task1-1")
        self.bunch.add_node("/suite1/family1", new_node)
        self.assertIsNotNone(self.bunch.find_node("/suite1/family1/task1-1"))
        self.assertIsNotNone(self.bunch.find_node("/suite1/family1/task1"))

    def test_find_suite_by_name(self):
        self.assertEqual(self.bunch.find_suite("suite1"), self.suite1)

    def test_find_node_by_absolute_path(self):
        self.assertEqual(self.bunch.find_node("/suite1/family1"), self.family1)
        self.assertEqual(self.bunch.find_node("/suite1/family1/task1"), self.task1)
        self.assertEqual(self.bunch.find_node("/suite1/family2"), self.family2)

    def test_to_json(self):
        print(self.bunch.to_json())

    def test_delete_suite(self):
        suite2 = self.bunch.add_suite("suite2")
        suite2.append_child("task1")
        suite2.append_child("task2")
        self.assertEqual(len(self.bunch.suites), 2)
        print(json.dumps(self.bunch.to_dict(),
                         indent=4, separators=(',', ';')))
        self.bunch.delete_suite(suite2)
        self.assertEqual(len(self.bunch.suites), 1)
        print(json.dumps(self.bunch.to_dict(),
                         indent=4, separators=(',', ';')))

    def test_delete_node(self):
        suite2 = self.bunch.add_suite("suite2")
        suite2.append_child("task1")
        suite2.append_child("task2")
        suite2.append_child("family1").append_child("task1")
        #pre_order_travel(suite2, SimplePrintVisitor())
        self.bunch.delete_node("/suite2/family1")
        self.assertIsNone(self.bunch.find_node("/suite2/family1"))
        self.assertIsNone(self.bunch.find_node("/suite2/family1/task1"))
        #pre_order_travel(suite2, SimplePrintVisitor())

    def test_update_suite(self):
        print("[test_update_suite] begin")
        suite2 = self.bunch.add_suite("suite2")
        suite2.append_child("task1")
        suite2.append_child("task2")
        #pre_order_travel(self.bunch.find_suite("suite2"), SimplePrintVisitor())
        suite3 = Suite("suite2")
        suite3.append_child("task2-1")
        suite3.append_child("task2-2")
        self.bunch.update_suite(suite3)
        self.assertIsNotNone(self.bunch.find_node("/suite2"))
        self.assertIsNotNone(self.bunch.find_node("/suite2/task2-1"))
        self.assertIsNotNone(self.bunch.find_node("/suite2/task2-2"))
        #pre_order_travel(self.bunch.find_suite("suite2"), SimplePrintVisitor())
        print("[test_update_suite] end")

    def test_update_node(self):
        print("[test_update_node] begin")
        suite2 = self.bunch.add_suite("suite2")
        family1 = suite2.append_child("family1")
        family1.append_child("task1")
        family1.append_child("task2")
        suite2.append_child("task3")
        pre_order_travel(self.bunch.find_suite("suite2"), SimplePrintVisitor())
        new_family1 = Node("family1")
        new_family1.append_child("task1-1")
        new_family1.append_child("task2-1")
        self.bunch.update_node("/suite2/family1", new_family1)
        self.assertIsNotNone(self.bunch.find_node("/suite2"))
        self.assertIsNotNone(self.bunch.find_node("/suite2/family1"))
        self.assertIsNotNone(self.bunch.find_node("/suite2/family1/task1-1"))
        self.assertIsNotNone(self.bunch.find_node("/suite2/family1/task2-1"))
        pre_order_travel(self.bunch.find_suite("suite2"), SimplePrintVisitor())
        print("[test_update_node] end")


if __name__ == '__main__':
    unittest.main()
