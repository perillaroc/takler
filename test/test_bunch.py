import unittest
from takler.bunch import Bunch
from takler.visitor import pre_order_travel, NodeVisitor


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

    def test_create(self):
        self.suite1.print_suite()

    def test_find_suite_by_name(self):
        self.assertEqual(self.bunch.find_suite_by_name("suite1"), self.suite1)

    def test_find_node_by_absolute_path(self):
        self.assertEqual(self.bunch.find_node_by_absolute_path("/suite1/family1"), self.family1)
        self.assertEqual(self.bunch.find_node_by_absolute_path("/suite1/family1/task1"), self.task1)
        self.assertEqual(self.bunch.find_node_by_absolute_path("/suite1/family2"), self.family2)


if __name__ == '__main__':
    unittest.main()
