from __future__ import annotations

from typing import Union

from .node import Node
from .task import Task


class NodeContainer(Node):
    def __init__(self, name: str):
        super(NodeContainer, self).__init__(name)

    # Build tree structure -------------------------------------------

    def add_container(self, container: Union[str, NodeContainer]) -> NodeContainer:
        if isinstance(container, str):
            container_node = NodeContainer(name=container)
        elif isinstance(container, NodeContainer):
            container_node = container
        else:
            raise TypeError("container must be str or NodeContainer")

        c = self.append_child(container_node)
        return c

    def add_task(self, task: Union[str, Task]) -> Task:
        if isinstance(task, str):
            task_node = Task(name=task)
        elif isinstance(task, Task):
            task_node = task
        else:
            raise TypeError("task must be str or Task")

        t = self.append_child(task_node)
        return t

    # Node operation -----------------------------------------

    def requeue(self):
        super(NodeContainer, self).requeue()

        for child in self.children:
            child.requeue()
