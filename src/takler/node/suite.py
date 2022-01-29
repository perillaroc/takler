import os

from takler.node.node import Node
from takler.visitor import SimplePrintVisitor, pre_order_travel


class Suite(Node):
    def __init__(self, node_name):
        Node.__init__(self, node_name)
        self.root = Node(node_name)
        self.suite_home = os.getcwd()
        self.var_map["suite_home"] = os.getcwd()
        self.var_map["takler_run_home"] = os.getcwd()

    def print_suite(self):
        pre_order_travel(self, SimplePrintVisitor())