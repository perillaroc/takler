import json
import unittest
import os
from takler.bunch import Bunch, Node
from takler.service_handler import TaklerServiceHandler
from takler.suite import Suite
from helper import check_node_state, empty_fork_for_parent, empty_wait_pid


class TaklerServiceHandlerTestCase(unittest.TestCase):
    def setUp(self):
        import os

        os.fork = empty_fork_for_parent
        os.waitpid = empty_wait_pid
        self.bunch = Bunch()
        self.service_handler = TaklerServiceHandler(self.bunch)

        self.empty_suite = self.bunch.add_suite("empty_suite")
        self.empty_suite.var_map["suite_home"] = os.path.join(os.path.dirname(__file__), 'test_data/py')
        self.family1 = self.empty_suite.append_child("family1")
        self.task1 = self.family1.append_child("task1")
        self.task2 = self.family1.append_child("task2")
        self.task2.add_trigger("task1 == complete")

        self.family2 = self.empty_suite.append_child("family2")
        self.family2.add_trigger("family1 == complete")

        self.task3 = self.family2.append_child("task3")

        self.family3 = self.family2.append_child("family3")
        self.family3.add_trigger("task3 == complete")
        self.task4 = self.family3.append_child("task4")

    def test_handler_create(self):
        reload(os)

    def test_handler_queue(self):
        self.service_handler.queue("/empty_suite")
        state_mapper = {
            "/empty_suite": "submitted",
            "/empty_suite/family1": "submitted",
            "/empty_suite/family1/task1": "submitted",
            "/empty_suite/family1/task2": "queued",
            "/empty_suite/family2": "queued",
            "/empty_suite/family2/task3": "queued",
            "/empty_suite/family2/family3": "queued",
            "/empty_suite/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)

    def test_handler_run(self):
        self.service_handler.queue("/empty_suite")
        self.service_handler.run("/empty_suite/family2/task3")
        state_mapper = {
            "/empty_suite": "submitted",
            "/empty_suite/family1": "submitted",
            "/empty_suite/family1/task1": "submitted",
            "/empty_suite/family1/task2": "queued",
            "/empty_suite/family2": "submitted",
            "/empty_suite/family2/task3": "submitted",
            "/empty_suite/family2/family3": "queued",
            "/empty_suite/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)

    def test_handler_init(self):
        self.service_handler.queue("/empty_suite")
        self.service_handler.init("/empty_suite/family1/task1", "1234567")
        state_mapper = {
            "/empty_suite": "active",
            "/empty_suite/family1": "active",
            "/empty_suite/family1/task1": "active",
            "/empty_suite/family1/task2": "queued",
            "/empty_suite/family2": "queued",
            "/empty_suite/family2/task3": "queued",
            "/empty_suite/family2/family3": "queued",
            "/empty_suite/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)

    def test_handler_complete(self):
        self.service_handler.queue("/empty_suite")
        self.service_handler.init("/empty_suite/family1/task1", "1234567")
        self.service_handler.complete("/empty_suite/family1/task1")
        state_mapper = {
            "/empty_suite": "submitted",
            "/empty_suite/family1": "submitted",
            "/empty_suite/family1/task1": "complete",
            "/empty_suite/family1/task2": "submitted",
            "/empty_suite/family2": "queued",
            "/empty_suite/family2/task3": "queued",
            "/empty_suite/family2/family3": "queued",
            "/empty_suite/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)

    def test_handler_abort(self):
        self.service_handler.queue("/empty_suite")
        self.service_handler.init("/empty_suite/family1/task1", "1234567")
        self.service_handler.abort("/empty_suite/family1/task1")
        state_mapper = {
            "/empty_suite": "aborted",
            "/empty_suite/family1": "aborted",
            "/empty_suite/family1/task1": "aborted",
            "/empty_suite/family1/task2": "queued",
            "/empty_suite/family2": "queued",
            "/empty_suite/family2/task3": "queued",
            "/empty_suite/family2/family3": "queued",
            "/empty_suite/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)

    def test_handler_kill(self):
        self.service_handler.queue("/empty_suite")
        self.service_handler.init("/empty_suite/family1/task1", "1234567")
        self.service_handler.kill("/empty_suite/family1/task1")
        state_mapper = {
            "/empty_suite": "aborted",
            "/empty_suite/family1": "aborted",
            "/empty_suite/family1/task1": "aborted",
            "/empty_suite/family1/task2": "queued",
            "/empty_suite/family2": "queued",
            "/empty_suite/family2/task3": "queued",
            "/empty_suite/family2/family3": "queued",
            "/empty_suite/family2/family3/task4": "queued",
        }
        check_node_state(self, self.bunch, state_mapper)

    def test_handler_get_bunch_tree(self):
        tree_str = self.service_handler.bunch_tree().str
        bunch_tree = json.loads(tree_str)
        print json.dumps(bunch_tree, indent=2, separators=(',', ';'))

    def test_handler_add_suite(self):
        test_suite2 = Suite("test_suite2")
        test_suite2.var_map["suite_home"] = os.path.join(os.path.dirname(__file__), 'test_data/py')
        family1 = test_suite2.append_child("family1")
        task1 = family1.append_child("task1")
        task2 = family1.append_child("task2")
        task2.add_trigger("task1 == complete")

        family2 = test_suite2.append_child("family2")
        family2.add_trigger("family1 == complete")

        task3 = family2.append_child("task3")

        family3 = family2.append_child("family3")
        family3.add_trigger("task3 == complete")
        task4 = family3.append_child("task4")

        self.service_handler.add_suite(test_suite2.to_json())
        print "[test_handler_add_suite]"
        print json.dumps(self.service_handler.bunch.to_dict(),
                         indent=4, separators=(',', ';'))

    def test_handler_update_suite(self):
        self.assertIsNotNone(self.bunch.find_node("/empty_suite/family1"))
        self.assertIsNotNone(self.bunch.find_node("/empty_suite/family1/task1"))
        self.assertIsNotNone(self.bunch.find_node("/empty_suite/family1/task2"))
        new_empty_suite = Node("empty_suite")
        new_empty_suite.append_child("task1-1")
        new_empty_suite.append_child("task2-1")
        self.service_handler.update_suite(new_empty_suite.to_json())
        self.assertIsNotNone(self.bunch.find_node("/empty_suite"))
        self.assertIsNotNone(self.bunch.find_node("/empty_suite/task1-1"))
        self.assertIsNotNone(self.bunch.find_node("/empty_suite/task2-1"))
        self.assertIsNone(self.bunch.find_node("/empty_suite/family1"))
        self.assertIsNone(self.bunch.find_node("/empty_suite/family1/task1"))
        self.assertIsNone(self.bunch.find_node("/empty_suite/family1/task2"))
        self.assertIsNone(self.bunch.find_node("/empty_suite/family2"))

    def test_handler_update_node(self):
        new_family1 = Node("family1")
        new_family1.append_child("task1-1")
        new_family1.append_child("task2-1")
        self.service_handler.update_node("/empty_suite/family1", new_family1.to_json())
        self.assertIsNotNone(self.bunch.find_node("/empty_suite/family1"))
        self.assertIsNotNone(self.bunch.find_node("/empty_suite/family1/task1-1"))
        self.assertIsNotNone(self.bunch.find_node("/empty_suite/family1/task2-1"))
        self.assertIsNone(self.bunch.find_node("/empty_suite/family1/task1"))
        self.assertIsNone(self.bunch.find_node("/empty_suite/family1/task2"))



if __name__ == '__main__':
    unittest.main()
