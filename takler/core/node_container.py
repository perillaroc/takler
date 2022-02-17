from __future__ import annotations

from typing import Union

from .node import Node, compute_most_significant_status
from .state import NodeStatus
from .task_node import Task


class NodeContainer(Node):
    def __init__(self, name: str):
        super(NodeContainer, self).__init__(name)

    # State management ----------------------------------------------------

    def computed_status(self, immediate: bool) -> NodeStatus:
        if len(self.children) == 0:
            return self.state.node_status

        c_state = compute_most_significant_status(self.children, immediate)
        return c_state

    # Build flow tree structure -------------------------------------------

    def add_container(self, container: Union[str, NodeContainer]) -> NodeContainer:
        """
        Add a ``NodeContainer``.
        If ``container`` is a string, a new ``NodeContainer`` will be created.

        Parameters
        ----------
        container

        Returns
        -------
        NodeContainer
        """
        if isinstance(container, str):
            container_node = NodeContainer(name=container)
        elif isinstance(container, NodeContainer):
            container_node = container
        else:
            raise TypeError("container must be str or NodeContainer")

        c = self.append_child(container_node)
        return c

    def add_task(self, task: Union[str, Task]) -> Task:
        """
        Add a ``Task``.

        Should use a real ``Task`` instead of base ``Task`` object.

        Parameters
        ----------
        task

        Returns
        -------
        Task
        """
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
        """
        Requeue the node and all its child nodes.

        Call ``Node.requeue`` first and then requeue its children.

        Returns
        -------

        """
        super(NodeContainer, self).requeue()

        for child in self.children:
            child.requeue()
