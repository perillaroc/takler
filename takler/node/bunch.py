import json
from .suite import Suite
from .node import Node


class Bunch(Node):
    def __init__(self):
        Node.__init__(self, '')
        self.suites = dict()

    def to_dict(self):
        ret = dict()
        for a_key in self.suites.keys():
            ret[a_key] = self.suites[a_key].to_dict()
        return ret

    def to_json(self):
        return json.dumps(self.to_dict())

    def add_suite(self, suite):
        if isinstance(suite, Node):
            # change to suite
            suite.__class__ = Suite
        elif isinstance(suite, str):
            suite = Suite(suite)
        else:
            raise Exception("{a_suite} is not a suite".format(a_suite=suite))
        if self.find_suite(suite.name):
            raise Exception("Suite {a_suite} is already exist".format(a_suite=suite.name))
        self.suites[suite.name] = suite
        return suite

    def add_node(self, parent, node):
        parent = self.find_node(parent)
        if parent is None:
            raise Exception("Node {parent} doesn't exist".format(parent=parent))
        return parent.append_child_node(node)

    def find_suite(self, name):
        if name in self.suites:
            return self.suites[name]
        return None

    def find_node(self, path):
        assert path.startswith('/')
        tokens = path.split('/')
        assert len(tokens) > 1
        suite_name = tokens[1]
        a_suite = self.find_suite(suite_name)
        if a_suite is None:
            return None
        return a_suite.find_node(path)

    def update_suite(self, suite):
        if suite.name not in self.suites:
            raise Exception("Update failed.Suite {suite} doesn't exist.".format(suite=suite.name))
        old_suite = self.suites[suite.name]
        self.suites[suite.name] = suite
        return old_suite

    def update_node(self, path, node):
        """
        path and node must have the same name.
        :param path:
        :param node:
        :return:
        """
        old_node = self.find_node(path)
        if old_node is None:
            raise Exception("{path} is not found.".format(path=path))
        assert old_node.name == node.name
        if not old_node.is_leaf_node:
            return self.update_suite(node)
        return old_node.parent.update_child(old_node.name, node)

    def delete_suite(self, suite):
        if isinstance(suite, Node):
            suite_name = suite.name
        elif isinstance(suite, str):
            suite_name = suite
        else:
            raise TypeError("param suite must be a Node or string.")
        if suite_name not in self.suites:
            raise Exception("suite {suite} doesn't exist.".format(suite=suite_name))
        return self.suites.pop(suite_name)

    def delete_node(self, path):
        node = self.find_node(path)
        if node is None:
            raise Exception("{path} doesn't exist.".format(path=path))
        if len(node.children) == 0:
            return self.delete_suite(node)
        else:
            node.delete_children()
            return node.parent.delete_child(node)
