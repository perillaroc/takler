import os

from takler.node import Node


class Suite(Node):
    def __init__(self, node_name):
        Node.__init__(self, node_name)
        self.root = Node(node_name)
        self.suite_home = os.getcwd()
        self.var_map["suite_home"] = os.getcwd()