class NodeState(object):
    Unknown = 1
    Complete = 2
    Queued = 3
    Submitted = 4
    Active = 5
    Aborted = 6

    state_mapper = {
        "unknown": Unknown,
        "queued": Queued,
        "submitted": Submitted,
        "active": Active,
        "complete": Complete,
        "aborted": Aborted
    }

    def __init__(self):
        self.node_state = self.Unknown

    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

    @staticmethod
    def compute_node_state(node):
        if len(node.children) == 0:
            return node.state
        state = NodeState.Unknown
        for a_child in node.children:
            child_node_state = NodeState.compute_node_state(a_child)
            if child_node_state > state:
                state = child_node_state
        return state

    @staticmethod
    def to_state(state_str):
        return NodeState.state_mapper[state_str.lower()]