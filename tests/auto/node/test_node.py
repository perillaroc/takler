# coding: utf-8
import os
import json
import pathlib

import pytest

from takler.node.variable import VariableName, Variable
from takler.node.node import Node
from takler.node.node_state import NodeState
from takler.visitor import SimplePrintVisitor, pre_order_travel


class TestNode(object):
    def setup_method(self):
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
        self.suite1 = Node("suite1")
        self.suite1.set_variable(VariableName.SUITE_HOME.name, os.path.dirname(__file__))
        self.suite1.set_variable(VariableName.TAKLER_RUN_HOME.name, os.path.join(os.path.dirname(__file__), "run"))

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

        self.suite_dict = {
            'name': 'suite1',
            'state': 'unknown',
            'var_map': {
                'SUITE_HOME': {
                    'name': 'SUITE_HOME',
                    'value': os.path.dirname(__file__)
                },
                'TAKLER_RUN_HOME': {
                    'name': 'TAKLER_RUN_HOME',
                    'value': os.path.join(os.path.dirname(__file__), "run")
                }
            },
            'children': [
                {
                    'name': 'family1',
                    'state': 'unknown',
                    'var_map': {

                    },
                    'children': [
                        {
                            'name': 'task1',
                            'state': 'unknown',
                            'var_map': {},
                            'children': []
                        },
                        {
                            'name': 'task2',
                            'state': 'unknown',
                            'trigger': {
                                'expr': 'task1 == complete'
                            },
                            'var_map': {},
                            'children': []
                        }
                    ]
                },
                {
                    'name': 'family2',
                    'state': 'unknown',
                    'trigger': {
                        'expr': 'family1 == complete'
                    },
                    'var_map': {},
                    'children': [
                        {
                            'name': 'task3',
                            'state': 'unknown',
                            'var_map': {},
                            'children': []
                        },
                        {
                            'name': 'family3',
                            'state': 'unknown',
                            'trigger': {
                                'expr': 'task3 == complete'
                            },
                            'var_map': {},
                            'children': [
                                {
                                    'name': 'task4',
                                    'state': 'unknown',
                                    'var_map': {},
                                    'children': []
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    def teardown_method(self):
        self.suite1 = None

    def test_to_dict(self):
        suite_dict = self.suite1.to_dict()
        assert suite_dict == self.suite_dict

    def test_create_from_dict(self):
        suite = Node.create_from_dict(self.suite_dict)
        assert suite.name == self.suite1.name
        assert suite.state == self.suite1.state

    def test_to_json(self):
        suite_json = self.suite1.to_json()
        assert suite_json == json.dumps(self.suite_dict)

    def test_create_from_json(self):
        pass

    def test_append_child(self):
        suite = Node('suite')
        task = Node('task')
        suite.append_child(task)
        assert suite.children[0] == task
        assert task.parent == suite

        suite = Node('suite')
        task1 = suite.append_child('task1')
        task2 = suite.append_child('task2')
        assert suite.children[0] == task1
        assert suite.children[1] == task2
        assert task1.parent == suite
        assert task2.parent == suite

        with pytest.raises(TypeError):
            suite.append_child(1)

    def test_find_child_index(self):
        assert self.family1.find_child_index(self.task1) == 0
        assert self.family1.find_child_index(self.task1.name) == 0

        assert self.family1.find_child_index(self.task3) == -1
        assert self.family1.find_child_index(self.task3.name) == -1

        with pytest.raises(TypeError):
            self.family1.find_child_index(1)

    def test_update_child(self):
        new_task1 = Node("new_task1")
        old_task1 = self.family1.update_child('task1', new_task1)
        assert old_task1 == self.task1
        assert self.family1.children[self.family1.find_child_index('new_task1')] == new_task1

        with pytest.raises(Exception):
            self.family1.update_child('task_no', new_task1)

    def test_delete_child(self):
        self.family2.delete_child(self.family3)
        assert len(self.family2.children) == 1
        assert len(self.family3.children) == 0

    def test_delete_children(self):
        self.family1.delete_children()
        assert len(self.family1.children) == 0
        assert self.task1.parent is None
        assert self.task1.var_map == dict()
        assert self.task1.trigger is None
        assert len(self.task1.children) == 0

    def test_set_variable(self):
        assert len(self.task1.var_map) == 0
        self.task1.set_variable("MODEL_DT", 30)
        assert len(self.task1.var_map) == 1
        assert "MODEL_DT" in self.task1.var_map
        assert self.task1.var_map["MODEL_DT"].name == "MODEL_DT"
        assert self.task1.var_map["MODEL_DT"].value == 30

    def test_swim_state_change(self):
        self.task1.state = NodeState.active
        self.task2.state = NodeState.queued
        self.task1.swim_state_change()
        assert self.family1.state == NodeState.active
        assert self.suite1.state == NodeState.active

        self.task1.state = NodeState.complete
        self.task2.state = NodeState.aborted
        self.task2.swim_state_change()
        assert self.family1.state == NodeState.aborted
        assert self.suite1.state == NodeState.aborted

    def test_sink_state_change(self):
        self.family2.sink_state_change(NodeState.queued)

        assert self.task3.state == NodeState.queued
        assert self.family3.state == NodeState.queued
        assert self.task4.state == NodeState.queued

    def test_set_state(self, monkeypatch):
        self.suite1.sink_state_change(NodeState.queued)

        def mock_run(x):
            def mock_run_inner():
                x.state = NodeState.active
            # print("run", x)
            return mock_run_inner

        monkeypatch.setattr(self.suite1, "run", mock_run(self.suite1))
        monkeypatch.setattr(self.family1, "run", mock_run(self.family1))
        monkeypatch.setattr(self.task1, "run", mock_run(self.task1))
        monkeypatch.setattr(self.task2, "run", mock_run(self.task2))
        monkeypatch.setattr(self.family2, "run", mock_run(self.family2))
        monkeypatch.setattr(self.task3, "run", mock_run(self.task3))
        monkeypatch.setattr(self.family3, "run", mock_run(self.family3))
        monkeypatch.setattr(self.task4, "run", mock_run(self.task4))

        self.family1.set_state(NodeState.queued)

        assert self.task1.state == NodeState.active

    def test_add_trigger(self):
        trigger = self.task2.trigger
        assert trigger.exp_str == "task1 == complete"
        assert trigger.parent_node == self.task2

    def test_evaluate_trigger(self):
        assert self.task4.evaluate_trigger()
        self.task1.state = NodeState.queued
        assert not self.task2.evaluate_trigger()
        self.task1.state = NodeState.complete
        assert self.task2.evaluate_trigger()

    def test_is_leaf_node(self):
        assert self.task1.is_leaf_node()
        assert not self.family1.is_leaf_node()
        assert not self.suite1.is_leaf_node()

    def test_get_node_path(self):
        assert self.suite1.get_node_path() == "/suite1"
        assert self.family1.get_node_path() == "/suite1/family1"
        assert self.task1.get_node_path() == "/suite1/family1/task1"
        assert self.task4.get_node_path() == "/suite1/family2/family3/task4"

    def test_find_node(self):
        assert self.task1.find_node("task2") == self.task2
        assert self.task2.find_node("task1") == self.task1
        assert self.family1.find_node("family2") == self.family2
        assert self.family2.find_node("family1") == self.family1
        assert self.task3.find_node("family3") == self.family3
        assert self.family1.find_node("family2/task3") == self.task3

        assert self.task1.find_node("../family2") == self.family2
        assert self.task1.find_node("../family2/task3") == self.task3

        assert self.task1.find_node("/suite1") == self.suite1
        assert self.task1.find_node("/suite1/family2/task3") == self.task3

        assert self.task1.find_node("/suite1/family3") is None
        assert self.task1.find_node("task3") is None
        assert self.task4.find_node("../family1/task1") is None

    def test_get_root(self):
        assert self.task1.get_root() == self.suite1
        assert self.family1.get_root() == self.suite1
        assert self.suite1.get_root() == self.suite1

    def test_find_variable(self):
        var_command = Variable('command', 'this is a command var value.')
        self.task1.var_map['command'] = var_command

        assert self.task1.find_variable('command') == var_command

    def test_find_generate_variable(self):
        assert self.task1.find_generate_variable(VariableName.NODE_PATH.name).value == "/suite1/family1/task1"

    def test_find_parent_variable(self):
        test_string = 'test_string'
        self.suite1.set_variable('test_string', test_string)
        assert self.task1.find_parent_variable("test_string").value == test_string
        assert self.task1.find_parent_variable("null_string") is None
        assert (self.task1.find_parent_variable(VariableName.NODE_PATH.name).value == "/suite1/family1/task1")
        assert (self.family1.find_parent_variable(VariableName.NODE_PATH.name).value == "/suite1/family1")
        assert (self.suite1.find_parent_variable(VariableName.NODE_PATH.name).value == "/suite1")

    def test_substitute_variable(self):
        assert (self.task1.substitute_variable("python $SCRIPT_PATH$")
                == "python {script_path}".format(script_path=self.task1.get_script_path()))
        assert (self.task1.substitute_variable("$SCRIPT_PATH$ hello $NODE_PATH$") ==
                "{script_path} hello {node_path}".format(
                    script_path=self.task1.get_script_path(),
                    node_path=self.task1.get_node_path()
                ))

    def test_get_script_path(self):
        assert (pathlib.Path(self.task1.get_script_path()) ==
                pathlib.Path(os.path.dirname(__file__), "suite1/family1/task1.takler"))
        assert (pathlib.Path(self.task4.get_script_path()) ==
                pathlib.Path(os.path.dirname(__file__), "suite1/family2/family3/task4.takler"))

    def test_get_job_path(self):
        assert (pathlib.Path(self.task1.get_job_path()) ==
                pathlib.Path(os.path.dirname(__file__), "run/suite1/family1/task1.takler.job"))
        assert (pathlib.Path(self.task4.get_job_path()) ==
                pathlib.Path(os.path.dirname(__file__), "run/suite1/family2/family3/task4.takler.job"))

    def test_get_job_output_path(self):
        assert (pathlib.Path(self.task1.get_job_output_path()) ==
                pathlib.Path(os.path.dirname(__file__), "run/suite1/family1/task1.takler.out"))
        assert (pathlib.Path(self.task4.get_job_output_path()) ==
                pathlib.Path(os.path.dirname(__file__), "run/suite1/family2/family3/task4.takler.out"))

    def test_get_job_output_error_path(self):
        assert (pathlib.Path(self.task1.get_job_output_error_path()) ==
                pathlib.Path(os.path.dirname(__file__), "run/suite1/family1/task1.takler.out.err"))
        assert (pathlib.Path(self.task4.get_job_output_error_path()) ==
                pathlib.Path(os.path.dirname(__file__), "run/suite1/family2/family3/task4.takler.out.err"))
