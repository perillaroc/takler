from .task import Task
from .node_container import NodeContainer


class Flow(NodeContainer):
    def __init__(self, name: str):
        super(Flow, self).__init__(name)

