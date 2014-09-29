import json
import os
import sys
import takler.constant
from takler.node_state import NodeState
from takler.node_trigger import NodeTrigger
from takler.takler_script_file import TaklerScriptFile
from takler.variable import VariableName


class Node(object):
    def __init__(self, node_name=""):
        self.name = node_name
        self.state = NodeState.Unknown

        self.parent = None
        self.children = list()

        self.task_id = ""
        self.path = ""

        self.trigger = None

        self.var_map = dict()

    def __str__(self):
        return "[{class_name}] {node_name}".format(class_name=self.__class__.__name__,
                                                   node_name=self.name)

    def __del__(self):
        self.parent = None
        for a_child in self.children:
            del a_child
        del self.children
        del self.trigger
        del self.var_map

    def to_dict(self):
        ret = dict()
        ret['name'] = self.name
        ret['state'] = self.state
        if self.task_id is not None and len(self.task_id) > 0:
            ret['task_id'] = self.task_id
        if self.path is not None and len(self.path) > 0:
            ret['path'] = self.path
        if self.trigger is not None:
            ret['trigger'] = self.trigger.to_str()
        ret['var_map'] = self.var_map
        ret['children'] = list()
        for a_child in self.children:
            ret['children'].append(a_child.to_dict())
        return ret

    @staticmethod
    def create_from_dict(node_dict, parent=None):
        # use parent is evil.
        node = Node()
        node.parent = parent
        node.name = node_dict['name']
        node.state = node_dict['state']
        if 'task_id' in node_dict:
            node.task_id = node_dict['task_id']
        if 'path' in node_dict:
            node.path = node_dict['path']
        if 'trigger' in node_dict:
            node.trigger = NodeTrigger(node_dict['trigger'], parent=node)
        node.var_map = node_dict['var_map']
        for a_child_item in node_dict['children']:
            a_child_node = Node.create_from_dict(a_child_item, parent=node)
            node.children.append(a_child_node)
        return node

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def create_from_json(node_json, parent=None):
        node_dict = json.loads(node_json)
        return Node.create_from_dict(node_dict, parent)

    def append_child(self, child_name):
        child_node = Node(child_name)
        return self.append_child_node(child_node)

    def append_child_node(self, child_node):
        child_node.parent = self
        self.children.append(child_node)
        return child_node

    def find_child_index(self, child):
        if isinstance(child, Node):
            child_name = child.name
        elif isinstance(child, basestring):
            child_name = child
        else:
            raise Exception("child must be a Node or a string.")
        for child_index in range(0, len(self.children)):
            if self.children[child_index].name == child_name:
                return child_index
        return -1

    def update_child(self, child_name, child_node):
        child_index = self.find_child_index(child_name)
        if child_index == -1:
            raise Exception("child {child_name} is not found".format(child_name=child_name))
        old_child = self.children[child_index]
        child_node.parent = self
        self.children[child_index] = child_node
        return old_child

    def delete_child(self, child):
        if child in self.children:
            child.delete_children()
            return self.children.pop(self.children.index(child))
        else:
            raise Exception("{child} does not exist".format(child=child))

    def delete_children(self):
        while len(self.children)>0:
            self.children[0].delete_children()
            self.children[0].parent = None
            self.children[0].trigger = None
            self.children[0].var_map = dict()
            self.children.remove(self.children[0])
        self.children = list()

    def set_value(self, value_name, value):
        self.var_map[value_name] = value

    def set_state(self, some_state):
        """Set node state to some state, and handle the state change.
        """
        self.state = some_state
        # swim stats
        self.swim_state_change()
        # resolve dependency from root.
        self.get_root().resolve_dependency()

    def swim_state_change(self):
        """Apply current node's state to all its ancestors without doing anything.

        Swim current state up. This method can only be called in set_state and itself.
        """
        node_state = NodeState.compute_node_state(self)

        if node_state != self.state:
            self.state = node_state

        if self.parent is not None:
            self.parent.swim_state_change()
        return

    def sink_state_change(self, state):
        """Apply the state change to all its descendants without doing anything.

        Sink current state down. This method can only be called in set_state and itself.
        """
        self.state = state
        for a_node in self.children:
            a_node.sink_state_change(state)

    def add_trigger(self, trigger_str):
        self.trigger = NodeTrigger(trigger_str, self)

    def evaluate_trigger(self):
        if self.trigger is None:
            return True
        return self.trigger.evaluate()

    def resolve_dependency(self):
        """Resolve node dependency for this node and all its children. Submit those satisfy conditions.
        """
        if not self.__resolve_node_dependency():
            return False
        for a_child in self.children:
            a_child.resolve_dependency()
        return True

    def __resolve_node_dependency(self):
        """Resolve dependency of this node only and submit it when true.
        """
        if self.state == NodeState.Complete or self.state >= NodeState.Submitted:
            return False

        if not self.evaluate_trigger():
            return False

        if self.is_leaf_node():
            self.run()

        return True

    def queue(self):
        """Re-queue this node and all its children nodes.

        Change stats of this nodes to Queued, and resolve dependency once.
        """
        print "[Node]{node} queue".format(node=self.get_node_path())
        self.sink_state_change(NodeState.Queued)
        self.set_state(NodeState.Queued)

    def run(self):
        """Execute the script of the node. Change state to Submitted.

        This method is usually called by resolve_dependency.
        """
        node_path = self.get_node_path()
        script_path = self.get_script_path()
        job_file = self.get_job_path()
        print "[Node]{node} submitted. script is {script_path}".format(node=node_path, script_path=script_path)

        script_file = TaklerScriptFile(self, self.get_script_path())
        script_file.create_job_script_file()
        command = self.find_parent_variable("run_command")
        substituted_command = self.substitute_variable(command)

        self.run_command(substituted_command)
        self.set_state(NodeState.Submitted)
        return

    def init(self, task_id):
        """Change state to Active. This is usually called form running script via a client command.
        """
        self.task_id = task_id
        print "[Node]{node} init with {task_id}".format(node=self.get_node_path(), task_id=task_id)
        self.set_state(NodeState.Active)

    def complete(self):
        print "[Node]{node} complete with task_id {task_id}".format(node=self.get_node_path(),
                                                                    task_id=self.task_id)
        self.set_state(NodeState.Complete)

    def abort(self):
        print "[Node]{node} abort".format(node=self.get_node_path())
        self.set_state(NodeState.Aborted)

    def kill(self):
        print "[Node]{node} kill".format(node=self.get_node_path())
        command = self.substitute_variable(self.find_parent_variable("kill_command"))
        substituted_command = self.substitute_variable(command)
        self.run_command(substituted_command)
        self.set_state(NodeState.Aborted)

    def run_command(self, command):
        child_pid = os.fork()
        if child_pid == 0:
            child_pid = os.fork()
            if child_pid == 0:
                os.execl("/bin/sh", "sh", "-c", command)
                os._exit(127)
            elif child_pid == -1:
                print "[Node]{node} run command failed for {command}:  can't fork.".format(
                    node=self.get_node_path(),
                    command=command
                )
                sys.exit()
            else:
                sys.exit()
        elif child_pid == -1:
            print "[Node]{node} run command failed for {command}:  can't fork.".format(
                node=self.get_node_path(),
                command=command
            )
            return
        else:
            os.waitpid(child_pid, 0)
            return
    ##############################
    # section for node accessing
    ##############################

    def is_leaf_node(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def get_node_path(self):
        cur_node = self
        node_list = []
        while cur_node is not None:
            node_list.insert(0, cur_node.name)
            cur_node = cur_node.parent
        node_list.insert(0, "")
        return "/".join(node_list)

    def find_node(self, a_node_path):
        """use node path to find a node.

        Type of node path:
            1. node1    relative to currently directory
            2. ../node1/node2
            3. /node1/node2
        """
        cur_node = self
        node_path = a_node_path
        root = cur_node.get_root()
        if node_path.startswith("/"):
            node_path = node_path[1:]

        # TODO: support multi roots, affect bunch.find_node_by_absolute_path
        if node_path.startswith(root.name):
            node_path = node_path[len(root.name)+1:]
            cur_node = root
        else:
            cur_node = self.parent

        if len(node_path) == 0:
            return cur_node

        tokens = node_path.split("/")
        for a_token in tokens:
            if a_token == "..":
                cur_node = cur_node.parent
            else:
                t_node = None
                for a_child in cur_node.children:
                    if a_child.name == a_token:
                        t_node = a_child
                        break
                if t_node is None:
                    return None
                cur_node = t_node

        return cur_node

    def get_root(self):
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    ###########################
    # section for variable map
    ###########################
    def find_variable(self, name):
        if name in self.var_map:
            return self.var_map[name]
        return None

    def find_generate_variable(self, name):
        if name == VariableName.NODE_PATH:
            return self.get_node_path()
        elif name == VariableName.SCRIPT_PATH:
            return self.get_script_path()
        elif name == VariableName.TASK_ID:
            return self.task_id
        elif name == VariableName.RUN_COMMAND:
            return "python $takler_job_path$ > $takler_job_output$ 2>&1 &"
            #return "python $takler_job_path$ &"
        elif name == VariableName.KILL_COMMAND:
            return "kill $task_id$"
        elif name == VariableName.TAKLER_MACRO:
            # marco char for pre process including variable substitute
            # currently, we only use $ for python script.
            return "$"
        elif name == VariableName.TAKLER_JOB_PATH:
            return self.get_job_path()
        elif name == VariableName.TAKLER_JOB_OUTPUT:
            return self.get_job_output_path()
        elif name == VariableName.TAKLER_JOB_OUTPUT_ERROR:
            return self.get_job_output_error_path()
        return None

    def find_parent_variable(self, name):
        value = self.find_variable(name)
        if value is not None:
            return value
        value = self.find_generate_variable(name)
        if value is not None:
            return value
        parent_node = self.parent
        while parent_node is not None:
            value = parent_node.find_variable(name)
            if value is not None:
                return value
            value = self.find_generate_variable(name)
            if value is not None:
                return value
            parent_node = parent_node.parent

        return value

    def substitute_variable(self, line, micro="$"):
        pos = 0
        result_line = line

        while True:
            start_pos = result_line.find(micro, pos)
            if start_pos == -1:
                return result_line

            end_pos = result_line.find(micro, start_pos+1)
            if end_pos == -1:
                raise Exception("variable substitution error: {line}")

            var_name = result_line[start_pos+1: end_pos]
            var_value = ''
            if var_name == '':
                var_value = micro
            else:
                var_value = self.find_parent_variable(var_name)
                if var_value is None:
                    raise Exception("var {var_name} is not found in string {line}".format(
                        var_name=var_name, line=line
                    ))
            result_line = result_line[:start_pos] + var_value + result_line[end_pos+1:]
            pos = start_pos + len(var_value)

    ##############################
    # section for task script
    ##############################
    def get_script_path(self):
        root = self.get_root()
        if "suite_home" in root.var_map:
            return root.var_map[VariableName.SUITE_HOME] + self.get_node_path() + '.' + \
                   takler.constant.SCRIPT_EXTENSION
        else:
            return None

    def get_job_path(self):
        root = self.get_root()
        if "takler_run_home" in root.var_map:
            return root.var_map[VariableName.TAKLER_RUN_HOME] + self.get_node_path() + '.' + \
                   takler.constant.JOB_SCRIPT_EXTENSION
        else:
            return None

    def get_job_output_path(self):
        root = self.get_root()
        if "takler_run_home" in root.var_map:
            return root.var_map[VariableName.TAKLER_RUN_HOME] + self.get_node_path() + '.' + \
                   takler.constant.JOB_OUTPUT_EXTENSION
        else:
            return None

    def get_job_output_error_path(self):
        root = self.get_root()
        if "takler_run_home" in root.var_map:
            return root.var_map[VariableName.TAKLER_RUN_HOME] + self.get_node_path() + '.' + \
                   takler.constant.JOB_OUTPUT_ERROR_EXTENSION
        else:
            return None