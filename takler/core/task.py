from .node import Node


class Task(Node):
    def __init__(self, name: str):
        super(Task, self).__init__(name)