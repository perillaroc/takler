import json
from takler.suite import Suite
from takler.node import Node


class Bunch(object):
    def __init__(self):
        self.suites = []

    def to_dict(self):
        ret = []
        for a_suite in self.suites:
            ret.append(a_suite.to_dict())
        return ret

    def to_json(self):
        return json.dumps(self.to_dict())

    def add_suite(self, suite):
        if isinstance(suite, Node):
            # change to suite
            suite.__class__ = Suite
        elif isinstance(suite, basestring):
            suite = Suite(suite)
        else:
            raise Exception("{a_suite} is not a suite".format(a_suite=suite))
        if self.find_suite(suite.name):
            raise Exception("Suite {a_suite} is already exist".format(a_suite=suite.name))
        self.suites.append(suite)
        return suite

    def update_suite(self, suite):
        pass

    def update_node(self, path, node):
        pass

    def delete_suite(self, suite):
        if isinstance(suite, Node):
            suite_name = suite.name
        elif isinstance(suite, basestring):
            suite_name = suite
        else:
            raise Exception("suite must be a Node or string.")
        node_no = -1
        for cur_no in range(0, len(self.suites)):
            if self.suites[cur_no].name == suite_name:
                node_no = cur_no
                break
        if node_no != -1:
            return self.suites.pop(node_no)
        else:
            raise Exception("suite {suite} doesn't exist.".format(suite=suite_name))

    def delete_node(self, path):
        node = self.find_node(path)
        if node is None:
            raise Exception("{path} doesn't exist.".format(path=path))
        if len(node.children) == 0:
            return self.delete_suite(node)
        else:
            node.delete_children()
            return node.parent.delete_child(node)

    def find_suite(self, name):
        for a_suite in self.suites:
            if a_suite.name == name:
                return a_suite
        return None

    def find_node(self, path):
        assert path.startswith('/')
        tokens = path.split('/')
        assert len(tokens) > 1
        suite_name = tokens[1]
        a_suite = self.find_suite(suite_name)
        return a_suite.find_node(path)
