from __future__ import annotations

from typing import Union, List, Optional, Mapping

from .node_state import NodeState
from .parameter import Parameter


class Node(object):
    def __init__(self, name: str):
        # 树形
        self.name = name  # type: str

        # 状态
        self.state = NodeState()  # type: NodeState

        # 树形结构
        self.parent = None  # type: Optional[Node]
        self.children = list()  # type: List[Node]

        # 参数
        self.parameters = dict()  # type: Mapping[str, Parameter]

    # children operation

    def append_child(self, child: Union[str, Node]) -> Node:
        if isinstance(child, str):
            child_node = Node(child)
        elif isinstance(child, Node):
            child_node = child
        else:
            raise TypeError("child must be a Node or string")

        child_node.parent = self
        self.children.append(child_node)
        return child_node

    def find_child_index(self, child: Union[str, Node]) -> int:
        if isinstance(child, Node):
            child_name = child.name
        elif isinstance(child, str):
            child_name = child
        else:
            raise TypeError("child must be a Node or a string.")

        for child_index in range(0, len(self.children)):
            if self.children[child_index].name == child_name:
                return child_index
        return -1

    def update_child(self, child: Union[str, Node], new_child_node) -> Node:
        child_index = self.find_child_index(child)
        if child_index == -1:
            raise Exception(f"child {child} is not found")

        old_child = self.children[child_index]
        new_child_node.parent = self
        self.children[child_index] = new_child_node
        return old_child

    def delete_child(self, child: Node) -> Node:
        if child in self.children:
            child.delete_children()
            return self.children.pop(self.children.index(child))
        else:
            raise Exception(f"{child} does not exist")

    def delete_children(self):
        while len(self.children) > 0:
            node = self.children.pop(0)
            node.delete_children()
            del node
        self.children = list()

