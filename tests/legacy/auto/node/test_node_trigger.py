# coding: utf-8
from takler.node.node_trigger import NodeTrigger
from takler.node.node_state import NodeState


class SimpleNode(object):
    def __init__(self, name):
        self.name = name
        self.children = list()
        self.parent = None
        self.state = NodeState.unknown

    def append_child_node(self, child_node):
        child_node.parent = self
        self.children.append(child_node)
        return child_node

    def get_root(self):
        root = self
        while root.parent is not None:
            root = root.parent
        return root
        
    def find_node(self, node_path):
        cur_node = self
        node_path = node_path
        root = cur_node.get_root()
        if node_path.startswith("/"):
            node_path = node_path[1:]

        if node_path.startswith(root.name):
            node_path = node_path[len(root.name) + 1:]
            cur_node = root
        else:
            cur_node = self.parent

        if len(node_path) == 0:
            return cur_node

        tokens = node_path.split("/")
        for a_token in tokens:
            if a_token == "..":
                cur_node = cur_node.parent
            else:
                t_node = None
                for a_child in cur_node.children:
                    if a_child.name == a_token:
                        t_node = a_child
                        break
                if t_node is None:
                    return None
                cur_node = t_node

        return cur_node


class TestNodeTrigger(object):
    def test_to_dict(self):
        root = SimpleNode('root')
        trigger = NodeTrigger('suite1 == complete', root)
        d = trigger.to_dict()
        assert 'expr' in d
        assert d['expr'] == 'suite1 == complete'

    def test_create_from_dict(self):
        root = SimpleNode('root')
        d = {
            'expr': 'suite1 == complete'
        }
        trigger = NodeTrigger.create_from_dict(d, root)
        assert isinstance(trigger, NodeTrigger)

    def test_equal_trigger(self):
        root_node = SimpleNode("root")
        family1_node = SimpleNode("family1")
        task1_node = SimpleNode("task1")
        task2_node = SimpleNode("task2")
        family1_node.append_child_node(task1_node)
        family1_node.append_child_node(task2_node)

        family2_node = SimpleNode("family2")
        task3_node = SimpleNode("task3")
        task4_node = SimpleNode("task4")
        family2_node.append_child_node(task3_node)
        family2_node.append_child_node(task4_node)

        root_node.append_child_node(family1_node)
        root_node.append_child_node(family2_node)

        trigger = NodeTrigger('task1 == complete', task2_node)

        task1_node.state = NodeState.complete
        assert trigger.evaluate()

        task1_node.state = NodeState.queued
        assert not trigger.evaluate()

        trigger = NodeTrigger('../family1 == complete', task3_node)

        family1_node.state = NodeState.complete
        assert trigger.evaluate()

        family1_node.state = NodeState.queued
        assert not trigger.evaluate()

        trigger = NodeTrigger('/root/family1/task1 == complete', task2_node)

        task1_node.state = NodeState.complete
        assert trigger.evaluate()

        task1_node.state = NodeState.queued
        assert not trigger.evaluate()
