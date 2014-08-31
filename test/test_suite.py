import unittest
import os
import shutil

from takler.suite import Suite
from takler.visitor import pre_order_travel, NodeVisitor


class MakeDirectoryVisitor(NodeVisitor):
    def __init__(self):
        NodeVisitor.__init__(self)
        pass

    def visit(self, node):
        base_name = os.path.dirname(node.get_script_path())
        if not os.path.isdir(base_name):
            os.makedirs(base_name)


class TestSuite(unittest.TestCase):
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
        self.old_cwd = os.getcwd()
        test_temp_dir = os.sep.join(['..', '..', 'takler-monitor-test-temp-dir', 'test_suite'])
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

        pre_order_travel(self.suite1, MakeDirectoryVisitor())

        task1_content = """print "this is task1"
print "task1 begin"
print "task1 init"
print "task1 end"
"""
        with open(self.task1.get_script_path(), 'w') as f:
            f.write(task1_content)

        task2_content = """print "this is task2"
print "task2 begin"
print "task2 init"
print "task2 end"
"""
        with open(self.task2.get_script_path(), 'w') as f:
            f.write(task2_content)

        task3_content = """print "this is task1"
print "task3 begin"
print "task3 init"
print "task3 end"
"""
        with open(self.task3.get_script_path(), 'w') as f:
            f.write(task3_content)

        task4_content = """print "this is task4"
print "task4 begin"
print "task4 init"
print "task4 end"
"""
        with open(self.task4.get_script_path(), 'w') as f:
            f.write(task4_content)

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

if __name__ == "__main__":
    unittest.main()