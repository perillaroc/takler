# coding=utf-8
import pathlib

import pytest

from takler.node.variable import VariableName
from takler.node.submittable_node import SubmittableNode
from takler.node.node import Node


class TestSubmittableNode(object):
    def setup_method(self):
        self.suite_home = "/tmp/suite_home"
        self.takler_run_home = "/tmp/taker_run_home"

        self.suite1 = Node("suite1")
        self.suite1.set_variable(VariableName.SUITE_HOME.name, self.suite_home)
        self.suite1.set_variable(VariableName.TAKLER_RUN_HOME.name, self.takler_run_home)

        self.submiited_node1 = SubmittableNode("task1")
        self.suite1.append_child(self.submiited_node1)

        self.suite1_dict = {
            'name': 'suite1',
            'state': 'unknown',
            'var_map': {
                'SUITE_HOME': {
                    'name': 'SUITE_HOME',
                    'value': self.suite_home
                },
                'TAKLER_RUN_HOME': {
                    'name': 'TAKLER_RUN_HOME',
                    'value': self.takler_run_home
                }
            },
            'children': [
                {
                    'name': 'task1',
                    'state': 'unknown',
                    'var_map': {},
                    'children': []
                }
            ]
        }

    def teardown_method(self):
        pass

    def test_to_dict(self):
        suite1_dict = self.suite1.to_dict()
        assert (suite1_dict == self.suite1_dict)

    def test_get_script_path(self):
        assert (pathlib.Path(self.submiited_node1.get_script_path()) ==
                pathlib.Path(self.suite_home, "suite1/task1.takler"))

    def test_get_job_path(self):
        assert (pathlib.Path(self.submiited_node1.get_job_path()) ==
                pathlib.Path(self.takler_run_home, "suite1/task1.takler.job"))

    def test_get_job_output_path(self):
        assert (pathlib.Path(self.submiited_node1.get_job_output_path()) ==
                pathlib.Path(self.takler_run_home, "suite1/task1.takler.out"))

    def test_get_job_output_error_path(self):
        assert (pathlib.Path(self.submiited_node1.get_job_output_error_path()) ==
                pathlib.Path(self.takler_run_home, "suite1/task1.takler.out.err"))

