import os
from takler import Server


class TestServer(object):
    def __init__(self):
        self.server = Server()
        self.bunch = self.server.bunch

        self.suite1 = self.bunch.add_suite("suite1")
        self.suite1.var_map["suite_home"] = os.path.join(os.path.dirname(__file__), '../test_data/py')
        self.family1 = self.suite1.append_child("family1")
        self.task1 = self.family1.append_child("task1")
        self.task2 = self.family1.append_child("task2")
        self.task2.add_trigger("task1 == complete")

        self.family2 = self.suite1.append_child("family2")
        self.family2.add_trigger("family1 == complete")

        self.task3 = self.family2.append_child("task3")

        self.family3 = self.family2.append_child("family3")
        self.family3.add_trigger("task3 == complete")
        self.task4 = self.family3.append_child("task4")


def main():
    # add suite
    test_server = TestServer()
    test_server.server.run_server()


if __name__ == "__main__":
    main()
