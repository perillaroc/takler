import unittest
import os
import shutil

from takler.suite import Suite
from takler.visitor import pre_order_travel, NodeVisitor, MakeDirectoryVisitor


class TestSuite(unittest.TestCase):
    def setUp(self):
        """Build a node tree for tests:

        |- suite1 [Unknown] Trigger: True
            |- family1 [Unknown] Trigger: True
                |- task1 [Unknown] Trigger: True
                |- task2 [Unknown] Trigger: [task1 == complete] False
            |- family2 [Unknown] Trigger: [family1 == complete] False
                |- task3 [Unknown] Trigger: True
                |- family3 [Unknown] Trigger: [task3 == complete] False
                    |- task4 [Unknown] Trigger: True
        """
        self.old_cwd = os.getcwd()
        test_temp_dir = os.sep.join([os.path.dirname(__file__), '..', '..', 'takler-monitor-tests', 'test_suite'])
        #test_temp_dir = "/vagrant_data/takler-monitor-tests/test_suite"
        if not os.path.exists(test_temp_dir):
            os.makedirs(test_temp_dir)
        print test_temp_dir
        os.chdir(test_temp_dir)
        self.suite_home = os.getcwd()
        self.suite1 = Suite("suite1")

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
        os.chdir(self.old_cwd)
        shutil.rmtree(self.suite_home)

    def test_suite_create(self):
        self.assertEqual(self.suite1.suite_home, os.getcwd())
        self.suite1.print_suite()

    def test_task_script_path(self):
        def check_task_script_path(path_mapper):
            for a_task_node in path_mapper:
                self.assertEqual(a_task_node.get_script_path(), path_mapper[a_task_node])

        task_script_path_mapper = {
            self.task1: self.suite_home+"/suite1/family1/task1.takler",
            self.task2: self.suite_home+"/suite1/family1/task2.takler",
            self.task3: self.suite_home+"/suite1/family2/task3.takler",
            self.task4: self.suite_home+"/suite1/family2/family3/task4.takler"
        }
        check_task_script_path(task_script_path_mapper)

    def test_to_json(self):
        print self.suite1.to_json()

if __name__ == "__main__":
    unittest.main()