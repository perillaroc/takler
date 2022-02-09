from __future__ import annotations

from typing import Union, List, Optional, Mapping
from pathlib import PurePosixPath

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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __repr__(self):
        return f"Node {self.name}"

    # children operation ------------------------------------------------

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

    # Node access -----------------------------------------------------

    def is_leaf_node(self) -> bool:
        if len(self.children) == 0:
            return True
        else:
            return False

    def get_root(self) -> Node:
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    @property
    def node_path(self) -> str:
        cur_node = self
        node_list = []
        while cur_node is not None:
            node_list.insert(0, cur_node.name)
            cur_node = cur_node.parent
        return str(PurePosixPath("/", *node_list))

    def find_node(self, a_path: str) -> Optional[Node]:
        """
        use node path to find a node.

        Parameters
        ----------
        a_path
            type of node path

                1. node1: relative to currently level
                2. ../node1/node2
                3. /node1/node2

        Returns
        -------
        Node or None
            node with node_path or None if not found
        """
        full_node_path = PurePosixPath(self.node_path).parent.joinpath(a_path)
        cur_node = self.get_root()
        parts = full_node_path.parts[1:]
        if parts[0] != cur_node.name:
            return None
        for a_token in parts[1:]:
            if cur_node is None:
                break
            if a_token == ".":
                continue
            if a_token == "..":
                cur_node = cur_node.parent
                continue

            t_node = None
            for a_child in cur_node.children:
                if a_child.name == a_token:
                    t_node = a_child
                    break
            if t_node is None:
                return None
            cur_node = t_node
        return cur_node
