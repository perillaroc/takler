from takler.node_state import NodeState


class NodeTrigger(object):
    def __init__(self, trigger_str, parent):
        self.exp_str = trigger_str
        self.node = None
        self.state = None
        self.operator = None
        self._parent_node = parent
        self.parse()

    def to_str(self):
        return self.exp_str

    @property
    def parent_node(self):
        return self._parent_node

    @parent_node.setter
    def parent_node(self, value):
        self._parent_node = value

    def parse(self):
        tokens = self.exp_str.split()
        if len(tokens) == 3:
            left_part = tokens[0]
            trigger_operator = tokens[1]
            right_part = tokens[2]

            self.node = self.parent_node.find_node(left_part)
            if self.node is None:
                raise Exception("trigger %s is not supported" % self.exp_str)
            self.operator = trigger_operator
            self.state = NodeState.to_state(right_part)
        else:
            raise Exception("trigger %s is not supported" % self.exp_str)

    def evaluate(self):
        if self.operator == "==":
            return self.node.state == self.state