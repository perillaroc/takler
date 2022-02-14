from __future__ import annotations

from typing import Union, List, Optional, Mapping
from pathlib import PurePosixPath

from .state import State, NodeStatus
from .parameter import Parameter


def compute_node_status(node: Node, immediate: bool) -> NodeStatus:
    """
    Compute node_status of a node from its children. Won't change anything in ``node``.

    If ``immediate`` is True, use children's node_status.
    If ``immediate`` is False, compute each child's node_status

    Parameters
    ----------
    node
    immediate

    Returns
    -------
    NodeStatus
    """
    if len(node.children) == 0:
        return node.state.node_status

    state = NodeStatus.unknown
    for a_child in node.children:
        if immediate:
            child_node_state = a_child.state.node_status
        else:
            child_node_state = compute_node_status(a_child, immediate)
        if child_node_state > state:
            state = child_node_state
    return state


class Node(object):
    def __init__(self, name: str):
        # 树形
        self.name = name  # type: str

        # 状态
        self.state = State()  # type: State

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
        return f"{self.__class__.__name__} {self.name}"

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}"

    # Children operation ------------------------------------------------

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

    # State management -----------------------------------------------------

    def set_node_status_only(self, node_status: NodeStatus):
        """
        Set node status to some status without any side effect.

        Parameters
        ----------
        node_status
            Node status, just an enum without any additional data.
        """
        old_state = self.state.node_status
        if old_state == node_status:
            return

        self.state.node_status = node_status

    def set_node_status(self, node_status: NodeStatus):
        """
        Set node status to some status with side effect.

        Parameters
        ----------
        node_status
            Node status, just an enum without any additional data.
        """
        if self.state.node_status == node_status:
            return

        self.set_node_status_only(node_status)
        self.handle_status_change()

    def sink_status_change_only(self, node_status: NodeStatus):
        """
        Apply the node_status change to all its descendants without doing anything.

        Sink current status down. This method can only be called in set_state and itself.
        """
        self.state.node_status = node_status
        for a_node in self.children:
            a_node.sink_status_change_only(node_status)

    def swim_status_change(self):
        """
        Compute current node's node_status, and swim status change up the tree.

        Swim current status up. This method can only be called in handle_status_change and itself.
        """
        node_state = compute_node_status(self, immediate=True)

        if node_state != self.state:
            self.state.node_status = node_state

        if self.parent is not None:
            self.parent.swim_status_change()
        return

    def handle_status_change(self):
        self.swim_status_change()

    # Node Operations ------------------------------------------------

    def requeue(self):
        """
        Node requeue itself, don't affect children nodes.
        """
        self.set_node_status_only(NodeStatus.queued)

