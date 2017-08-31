# coding: utf-8
import os
import json

import pytest

from takler.node.variable import VariableName
from takler.node.node import Node
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
        pass

    def test_delete_children(self):
        pass

    def test_set_variable(self):
        pass

    def test_set_state(self):
        pass

    def test_swim_state_change(self):
        pass

    def test_sink_state_change(self):
        pass

    def test_add_trigger(self):
        pass

    def test_evaluate_trigger(self):
        pass

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

    def test_node_deletion(self):
        print("before node delete")
        pre_order_travel(self.suite1, SimplePrintVisitor())
        self.family1.delete_children()
        print("after node delete")
        assert self.family1.children == list()
        pre_order_travel(self.suite1, SimplePrintVisitor())

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

