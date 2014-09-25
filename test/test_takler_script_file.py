import os
import unittest
import takler.suite
from takler.takler_script_file import TaklerScriptFile


class TaklerScriptFileTestCase(unittest.TestCase):
    def setUp(self):
        import os

        self.empty_suite = takler.suite.Suite("empty_suite")
        self.empty_suite.var_map["suite_home"] = os.path.join(os.path.dirname(__file__), 'test_data/py')
        self.empty_suite.var_map["takler_run_home"] = os.path.join(os.path.dirname(__file__),
                                                                   'test_data/takler-run-dir')
        self.family1 = self.empty_suite.append_child("family1")
        self.task1 = self.family1.append_child("task1")
        self.task2 = self.family1.append_child("task2")
        self.task2.add_trigger("task1 == complete")

        self.family2 = self.empty_suite.append_child("family2")
        self.family2.add_trigger("family1 == complete")

        self.task3 = self.family2.append_child("task3")

        self.family3 = self.family2.append_child("family3")
        self.family3.add_trigger("task3 == complete")
        self.task4 = self.family3.append_child("task4")

    def tearDown(self):
        pass

    def test_create_job_script_file(self):
        script_file = TaklerScriptFile(self.task1, self.task1.get_script_path())
        script_file.create_job_script_file()


if __name__ == '__main__':
    unittest.main()
