# coding: utf-8
from enum import Enum


class VariableName(Enum):
    NODE_PATH = "node_path"
    SCRIPT_PATH = "script_path"
    TASK_ID = "task_id"
    RUN_COMMAND = "run_command"
    KILL_COMMAND = "kill_command"
    TAKLER_MACRO = "takler_macro"
    TAKLER_JOB_PATH = "takler_job_path"
    TAKLER_JOB_OUTPUT = "takler_job_output"
    TAKLER_JOB_OUTPUT_ERROR = "takler_job_output_error"
    SUITE_HOME = "suite_home"
    TAKLER_RUN_HOME = "takler_run_home"


class Variable(object):
    def __init__(self, name='', value=''):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.value
        }
