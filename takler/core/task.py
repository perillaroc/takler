from .node import Node


class Task(Node):
    def __init__(self, name: str):
        super(Task, self).__init__(name)

    def __repr__(self):
        return f"Task {self.name}"

    def run(self):
        pass
