import os
import sys
import takler.constant
from takler.node_state import NodeState
from takler.node_trigger import NodeTrigger


class Node(object):
    def __init__(self, node_name=""):
        self.parent = None
        self.children = list()

        self.state = NodeState.Unknown
        self.name = node_name
        self.task_id = ""
        self.path = ""

        self.trigger = None

        self.var_map = dict()

    def __str__(self):
        return "[{class_name}] {node_name}".format(class_name=self.__class__.__name__,
                                                   node_name=self.name)

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

    def append_child(self, child_name):
        child_node = Node(child_name)
        child_node.parent = self
        self.children.append(child_node)
        return child_node

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
        script_path = self.get_root().var_map["suite_home"] + self.get_node_path() + '.' \
            + takler.constant.SCRIPT_EXTENSION
        print "[Node]{node} submitted. script is {script_path}".format(node=node_path, script_path=script_path)
        if len(script_path) > 0:
            if os.path.exists(script_path):
                child_pid = os.fork()
                if child_pid == 0:
                    child_pid = os.fork()
                    if child_pid == 0:
                        os.execl("/bin/sh", "sh", "-c", "python {script_path}".format(script_path=script_path))
                        os._exit(127)
                    elif child_pid == -1:
                        print "[Node]{node} submitted failed: can't fork.".format(node=node_path)
                        sys.exit()
                    else:
                        sys.exit()
                elif child_pid == -1:
                    print "[Node]{node} submitted failed: can't fork.".format(node=node_path)
                    return
                else:
                    os.waitpid(child_pid, 0)
                    self.set_state(NodeState.Submitted)
                    return
            else:
                print "[Node]{node} submitted failed: no script ({script_path}).".format(node=node_path,
                                                                                   script_path=script_path)
                return
        else:
            print "[Node]{node} submitted failed: no script path.".format(node=node_path)
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
        self.set_state(NodeState.Aborted)

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

    ##############################
    # section for task script
    ##############################

    def get_script_path(self):
        root = self.get_root()
        if "suite_home" in root.var_map:
            return root.var_map["suite_home"] + self.get_node_path() + '.' + takler.constant.SCRIPT_EXTENSION
        else:
            return ""