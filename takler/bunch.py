from takler.suite import Suite


class Bunch(object):
    def __init__(self):
        self.suites = []

    def add_suite(self, a_suite):
        if isinstance(a_suite, Suite):
            self.suites.append(a_suite)
            return a_suite
        elif isinstance(a_suite, basestring):
            new_suite = Suite(a_suite)
            self.suites.append(new_suite)
            return new_suite
        else:
            raise Exception("{a_suite} is not a suite".format(a_suite=a_suite))

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
