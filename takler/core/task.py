from .node import Node
from .state import NodeStatus


class Task(Node):
    def __init__(self, name: str):
        super(Task, self).__init__(name)

    def __repr__(self):
        return f"Task {self.name}"

    # State management --------------------------------------------

    def swim_status_change(self):
        """
        Task node use its own status, and needn't compute status again.
        So swim status change from its parent.
        """
        return self.parent.swim_status_change()

    # Node Operation ----------------------------------------------

    def run(self):
        # TODO: Run task.

        # change node status
        self.set_node_status(node_status=NodeStatus.submitted)
        self.handle_status_change()

    def init(self):
        self.set_node_status(node_status=NodeStatus.active)
        self.handle_status_change()

    def complete(self):
        self.set_node_status(node_status=NodeStatus.complete)
        self.handle_status_change()

    def abort(self):
        self.set_node_status(node_status=NodeStatus.aborted)
        self.handle_status_change()
