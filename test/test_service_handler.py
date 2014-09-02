import unittest
from takler.bunch import Bunch
from takler.service_handler import TaklerServiceHandler
from helper import check_node_state


class TaklerServiceHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.bunch = Bunch()
        self.service_handler = TaklerServiceHandler(self.bunch)

        self.suite1 = self.bunch.add_suite("suite1")
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

    def test_handler_create(self):
        pass

    def test_handler_queue(self):
        self.service_handler.queue("/suite1")
        state_mapper = {
            "/suite1": "submitted",
            "/suite1/family1": "submitted",
            "/suite1/family1/task1": "submitted",
            "/suite1/family1/task2": "queued",
            "/suite1/family2": "queued",
            "/suite1/family2/task3": "queued",
            "/suite1/family2/family3": "queued",
            "/suite1/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)

    def test_handler_run(self):
        self.service_handler.queue("/suite1")
        self.service_handler.run("/suite1/family2/task3")
        state_mapper = {
            "/suite1": "submitted",
            "/suite1/family1": "submitted",
            "/suite1/family1/task1": "submitted",
            "/suite1/family1/task2": "queued",
            "/suite1/family2": "submitted",
            "/suite1/family2/task3": "submitted",
            "/suite1/family2/family3": "queued",
            "/suite1/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)

    def test_handler_init(self):
        self.service_handler.queue("/suite1")
        self.service_handler.init("/suite1/family1/task1", "1234567")
        state_mapper = {
            "/suite1": "active",
            "/suite1/family1": "active",
            "/suite1/family1/task1": "active",
            "/suite1/family1/task2": "queued",
            "/suite1/family2": "queued",
            "/suite1/family2/task3": "queued",
            "/suite1/family2/family3": "queued",
            "/suite1/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)

    def test_handler_complete(self):
        self.service_handler.queue("/suite1")
        self.service_handler.init("/suite1/family1/task1", "1234567")
        self.service_handler.complete("/suite1/family1/task1")
        state_mapper = {
            "/suite1": "submitted",
            "/suite1/family1": "submitted",
            "/suite1/family1/task1": "complete",
            "/suite1/family1/task2": "submitted",
            "/suite1/family2": "queued",
            "/suite1/family2/task3": "queued",
            "/suite1/family2/family3": "queued",
            "/suite1/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)

    def test_handler_abort(self):
        self.service_handler.queue("/suite1")
        self.service_handler.init("/suite1/family1/task1", "1234567")
        self.service_handler.abort("/suite1/family1/task1")
        state_mapper = {
            "/suite1": "aborted",
            "/suite1/family1": "aborted",
            "/suite1/family1/task1": "aborted",
            "/suite1/family1/task2": "queued",
            "/suite1/family2": "queued",
            "/suite1/family2/task3": "queued",
            "/suite1/family2/family3": "queued",
            "/suite1/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)

    def test_handler_kill(self):
        self.service_handler.queue("/suite1")
        self.service_handler.init("/suite1/family1/task1", "1234567")
        self.service_handler.kill("/suite1/family1/task1")
        state_mapper = {
            "/suite1": "aborted",
            "/suite1/family1": "aborted",
            "/suite1/family1/task1": "aborted",
            "/suite1/family1/task2": "queued",
            "/suite1/family2": "queued",
            "/suite1/family2/task3": "queued",
            "/suite1/family2/family3": "queued",
            "/suite1/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)


if __name__ == '__main__':
    unittest.main()
