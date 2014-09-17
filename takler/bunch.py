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

    def add_suite(self, a_suite):
        if isinstance(a_suite, Node):
            # change to suite
            a_suite.__class__ = Suite
        elif isinstance(a_suite, basestring):
            a_suite = Suite(a_suite)
        else:
            raise Exception("{a_suite} is not a suite".format(a_suite=a_suite))
        if self.find_suite_by_name(a_suite.name):
            raise Exception("Suite {a_suite} is already exist".format(a_suite=a_suite.name))
        self.suites.append(a_suite)
        return a_suite

    def update_suite(self, a_suite):
        pass

    def update_node_by_absolute_path(self, a_path, node):
        pass

    def delete_suite(self, a_suite):
        pass

    def delete_node_by_absolute_path(self, a_path, node):
        pass

    def find_suite_by_name(self, suite_name):
        for a_suite in self.suites:
            if a_suite.name == suite_name:
                return a_suite
        return None

    def find_node_by_absolute_path(self, absolute_path):
        assert absolute_path.startswith('/')
        tokens = absolute_path.split('/')
        assert len(tokens) > 1
        suite_name = tokens[1]
        a_suite = self.find_suite_by_name(suite_name)
        return a_suite.find_node(absolute_path)
