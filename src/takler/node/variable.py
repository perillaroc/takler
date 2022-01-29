# coding: utf-8
from enum import Enum


class VariableName(Enum):
    NODE_PATH = "NODE_PATH"
    SCRIPT_PATH = "SCRIPT_PATH"
    TASK_ID = "TASK_ID"
    RUN_COMMAND = "RUN_COMMAND"
    KILL_COMMAND = "KILL_COMMAND"
    TAKLER_MACRO = "TAKLER_MACRO"
    TAKLER_JOB_PATH = "TAKLER_JOB_PATH"
    TAKLER_JOB_OUTPUT = "TAKLER_JOB_OUTPUT"
    TAKLER_JOB_OUTPUT_ERROR = "TAKLER_JOB_OUTPUT_ERROR"
    SUITE_HOME = "SUITE_HOME"
    TAKLER_RUN_HOME = "TAKLER_RUN_HOME"


class Variable(object):
    def __init__(self, name='', value=''):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.value
        }

    @classmethod
    def create_from_dict(cls, var_dict):
        var = Variable(var_dict['name'], var_dict['value'])
        return var
