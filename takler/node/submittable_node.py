# coding=utf-8
import os
import sys

from .node import Node
from .variable import VariableName, Variable
from .node_state import NodeState

from takler.core import constant
from takler.takler_script_file import TaklerScriptFile


class SubmittableNode(Node):
    def __init__(self, name):
        Node.__init__(self, name)
        self.task_id = ''

    def to_dict(self):
        node_dict = Node.to_dict(self)
        if self.task_id is not None and len(self.task_id) > 0:
            node_dict['task_id'] = self.task_id
        return node_dict

    #######################
    #   node operation
    #######################

    def init(self, task_id):
        """
        Change state to Active. This is usually called form running script via a client command.
        """
        self.task_id = task_id
        print("[Node]{node} init with {task_id}".format(node=self.get_node_path(), task_id=task_id))
        self.set_state(NodeState.active)

    def abort(self):
        print("[Node]{node} abort".format(node=self.get_node_path()))
        self.set_state(NodeState.aborted)

    def run(self):
        """
        Execute the script of the node. Change state to Submitted.

        This method is usually called by resolve_dependency.
        """
        node_path = self.get_node_path()
        script_path = self.get_script_path()
        job_file = self.get_job_path()
        print("[Node]{node} submitted. script is {script_path}".format(
            node=node_path, script_path=script_path))

        script_file = TaklerScriptFile(self, self.get_script_path())
        script_file.create_job_script_file()
        command = self.find_parent_variable("run_command")
        self.run_command(command)
        self.set_state(NodeState.submitted)
        return

    def complete(self):
        print("[Node]{node} complete with task_id {task_id}".format(
            node=self.get_node_path(),
            task_id=self.task_id))
        self.set_state(NodeState.complete)

    def kill(self):
        print("[Node]{node} kill".format(node=self.get_node_path()))
        command = self.substitute_variable(self.find_parent_variable("kill_command"))
        self.run_command(command)
        self.set_state(NodeState.aborted)

    def run_command(self, command):
        substituted_command = self.substitute_variable(command)
        child_pid = os.fork()
        if child_pid == 0:
            child_pid = os.fork()
            if child_pid == 0:
                os.execl("/bin/sh", "sh", "-c", substituted_command)
                os._exit(127)
            elif child_pid == -1:
                print("[Node]{node} run command failed for {command}:  can't fork.".format(
                    node=self.get_node_path(),
                    command=substituted_command
                ))
                sys.exit()
            else:
                sys.exit()
        elif child_pid == -1:
            print("[Node]{node} run command failed for {command}:  can't fork.".format(
                node=self.get_node_path(),
                command=substituted_command
            ))
            return
        else:
            os.waitpid(child_pid, 0)
            return

    ######################
    #   script and job
    ######################

    def get_script_path(self):
        root = self.get_root()
        if VariableName.SUITE_HOME.name in root.var_map:
            return (root.var_map[VariableName.SUITE_HOME.name].value
                    + self.get_node_path() + '.'
                    + constant.SCRIPT_EXTENSION)
        else:
            return None

    def get_job_path(self):
        root = self.get_root()
        if VariableName.TAKLER_RUN_HOME.name in root.var_map:
            path = root.var_map[VariableName.TAKLER_RUN_HOME.name].value + self.get_node_path() + '.' + \
                   constant.JOB_SCRIPT_EXTENSION
            return path
        else:
            return None

    def get_job_output_path(self):
        root = self.get_root()
        if VariableName.TAKLER_RUN_HOME.name in root.var_map:
            return root.var_map[VariableName.TAKLER_RUN_HOME.name].value + self.get_node_path() + '.' + \
                   constant.JOB_OUTPUT_EXTENSION
        else:
            return None

    def get_job_output_error_path(self):
        root = self.get_root()
        if VariableName.TAKLER_RUN_HOME.name in root.var_map:
            return root.var_map[VariableName.TAKLER_RUN_HOME.name].value + self.get_node_path() + '.' + \
                   constant.JOB_OUTPUT_ERROR_EXTENSION
        else:
            return None
