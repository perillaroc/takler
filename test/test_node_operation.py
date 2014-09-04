import unittest
import os
import takler.suite
import takler.node_state


class NodeOperationTestCase(unittest.TestCase):
    def setUp(self):
        self.empty_suite = takler.suite.Suite("empty_suite")
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

    def test_node_operation(self):
        def check_node_state(root, a_state_mapper):
            for a_state_exp in a_state_mapper:
                self.assertEqual(root.find_node(a_state_exp).state,
                                 takler.node_state.NodeState.to_state(a_state_mapper[a_state_exp]))

        self.empty_suite.queue()
        state_mapper = {
            "/empty_suite": "submitted",
            "/empty_suite/family1": "submitted",
            "/empty_suite/family1/task1": "submitted",
            "/empty_suite/family1/task2": "queued",
            "/empty_suite/family2/task3": "queued",
            "/empty_suite/family2/family3": "queued",
            "/empty_suite/family2/family3/task4": "queued",
        }
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        self.task1.init("123456")
        state_mapper["/empty_suite"] = "active"
        state_mapper["/empty_suite/family1"] = "active"
        state_mapper["/empty_suite/family1/task1"] = "active"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        self.task1.complete()
        state_mapper["/empty_suite"] = "submitted"
        state_mapper["/empty_suite/family1"] = "submitted"
        state_mapper["/empty_suite/family1/task1"] = "complete"
        state_mapper["/empty_suite/family1/task2"] = "submitted"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        self.task2.init("123456")
        state_mapper["/empty_suite"] = "active"
        state_mapper["/empty_suite/family1"] = "active"
        state_mapper["/empty_suite/family1/task2"] = "active"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        self.task2.complete()
        state_mapper["/empty_suite"] = "submitted"
        state_mapper["/empty_suite/family1"] = "complete"
        state_mapper["/empty_suite/family1/task2"] = "complete"
        state_mapper["/empty_suite/family2"] = "submitted"
        state_mapper["/empty_suite/family2/task3"] = "submitted"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        self.task3.init("123456")
        state_mapper["/empty_suite"] = "active"
        state_mapper["/empty_suite/family2"] = "active"
        state_mapper["/empty_suite/family2/task3"] = "active"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        self.task3.complete()
        state_mapper["/empty_suite"] = "submitted"
        state_mapper["/empty_suite/family2"] = "submitted"
        state_mapper["/empty_suite/family2/task3"] = "complete"
        state_mapper["/empty_suite/family2/family3"] = "submitted"
        state_mapper["/empty_suite/family2/family3/task4"] = "submitted"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        self.task4.init("123456")
        state_mapper["/empty_suite"] = "active"
        state_mapper["/empty_suite/family2"] = "active"
        state_mapper["/empty_suite/family2/family3"] = "active"
        state_mapper["/empty_suite/family2/family3/task4"] = "active"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        self.task4.complete()
        state_mapper["/empty_suite"] = "complete"
        state_mapper["/empty_suite/family2"] = "complete"
        state_mapper["/empty_suite/family2/family3"] = "complete"
        state_mapper["/empty_suite/family2/family3/task4"] = "complete"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        self.task2.run()
        state_mapper["/empty_suite"] = "submitted"
        state_mapper["/empty_suite/family1"] = "submitted"
        state_mapper["/empty_suite/family1/task2"] = "submitted"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        self.family2.queue()
        state_mapper["/empty_suite/family2"] = "queued"
        state_mapper["/empty_suite/family2/task3"] = "queued"
        state_mapper["/empty_suite/family2/family3"] = "queued"
        state_mapper["/empty_suite/family2/family3/task4"] = "queued"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        # force queue
        self.family1.queue()
        state_mapper["/empty_suite/family1"] = "submitted"
        state_mapper["/empty_suite/family1/task1"] = "submitted"
        state_mapper["/empty_suite/family1/task2"] = "queued"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())

        self.task1.abort()
        state_mapper["/empty_suite"] = "aborted"
        state_mapper["/empty_suite/family1"] = "aborted"
        state_mapper["/empty_suite/family1/task1"] = "aborted"
        check_node_state(self.empty_suite, state_mapper)
        #pre_order_travel(self.empty_suite, SimplePrintVisitor())


if __name__ == '__main__':
    unittest.main()
