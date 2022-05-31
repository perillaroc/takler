from __future__ import annotations

from typing import Union, List, Optional, Dict, TYPE_CHECKING, Set
from pathlib import PurePosixPath
from collections import defaultdict
from abc import ABC

from .state import State, NodeStatus
from .parameter import Parameter
from .event import Event
from .meter import Meter
from .limit import Limit, InLimit, InLimitManager
from .expression import Expression

if TYPE_CHECKING:
    from .bunch import Bunch


# def compute_node_status(node: Node, immediate: bool) -> NodeStatus:
#     """
#     Compute node_status of a node from its children. Won't change anything in ``node``.
#
#     If ``immediate`` is True, use children's node_status.
#     If ``immediate`` is False, compute each child's node_status
#
#     Parameters
#     ----------
#     node
#     immediate
#
#     Returns
#     -------
#     NodeStatus
#     """
#     if len(node.children) == 0:
#         return node.state.node_status
#
#     state = compute_most_significant_state(node.children, immediate)
#
#     return state


def compute_most_significant_status(nodes: List[Node], immediate: bool) -> NodeStatus:
    """
    Compute the most significant node status from node list. Won't change anything in ``node``.

    If ``immediate`` is True, use children's node_status.
    If ``immediate`` is False, compute each child's node_status

    Parameters
    ----------
    nodes
    immediate

    Returns
    -------
    NodeStatus
    """
    count = defaultdict(int)
    for node in nodes:
        if immediate:
            child_node_state = node.state.node_status
        else:
            child_node_state = node.computed_status(immediate)
        count[child_node_state] += 1

    for status in (
        NodeStatus.aborted,
        NodeStatus.active,
        NodeStatus.submitted,
        NodeStatus.queued,
        NodeStatus.complete,
    ):
        if count[status] > 0:
            return status

    return NodeStatus.unknown


class Node(ABC):
    def __init__(self, name: str):
        # 树形
        self.name: str = name

        # 状态
        self.state: State = State()

        # 树形结构
        self.parent: Optional["Node"] = None
        self.children: List["Node"] = list()

        # 参数
        self.user_parameters: Dict[str, Parameter] = dict()

        # 触发器
        self.trigger_expression: Optional[Expression] = None

        # 事件
        self.events: List[Event] = list()

        # 标尺
        self.meters: List[Meter] = list()

        # 限制
        self.limits: List[Limit] = list()
        self.in_limit_manager: InLimitManager = InLimitManager(self)

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

    @property
    def node_path(self) -> str:
        """
        str: full path from root node, starts with "/" and split each level with "/"
        """
        cur_node = self
        node_list = []
        while cur_node is not None:
            node_list.insert(0, cur_node.name)
            cur_node = cur_node.parent
        return str(PurePosixPath("/", *node_list))

    def is_leaf_node(self) -> bool:
        if len(self.children) == 0:
            return True
        else:
            return False

    def get_root(self) -> Node:
        """
        get root node

        Returns
        -------
        Node
        """
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    def get_bunch(self) -> "Optional[Bunch]":
        if self.parent is not None:
            return self.parent.get_bunch()
        else:
            return None

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

    @classmethod
    def check_absolute_node_path(cls, node_path: str) -> bool:
        if not node_path.startswith("/"):
            return False
        if node_path == "/":
            return False
        return True

    @classmethod
    def check_node_path(cls, node_path: str) -> bool:
        if node_path.startswith("/"):
            return cls.check_absolute_node_path(node_path)
        if node_path.startswith("../"):
            if len(node_path) == 3:
                return False
            else:
                return True
        if node_path.startswith("./"):
            if len(node_path) == 2:
                return False
            else:
                return True

    # State management -----------------------------------------------------

    def is_suspended(self) -> bool:
        return self.state.suspended

    def computed_status(self, immediate: bool) -> NodeStatus:
        """
        Compute node_status of a node from its children. Won't change anything in ``node``.

        If ``immediate`` is True, use children's node_status.
        If ``immediate`` is False, compute each child's node_status

        Parameters
        ----------
        immediate

        Returns
        -------
        NodeStatus
        """
        raise Exception("Not implemented!")

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

        Sink status down. This method can only be called in set_state and itself.
        """
        self.set_node_status_only(node_status)

    def sink_status_change(self, node_status: NodeStatus):
        """
        Apply the node_status change to all its descendants with side effects.
        """
        self.sink_status_change_only(node_status)

    def swim_status_change(self):
        """
        Compute current node's node_status, and swim status change up the tree.

        Swim current status up. This method can only be called in handle_status_change and itself.
        """
        node_state = self.computed_status(immediate=True)

        if node_state != self.state:
            self.state.node_status = node_state

        if self.parent is not None:
            self.parent.swim_status_change()
        return

    def handle_status_change(self):
        pass
        # self.swim_status_change()

    # Trigger --------------------------------------------------------

    def add_trigger(self, trigger: Union[str, Expression]):
        if isinstance(trigger, str):
            self.trigger_expression = Expression(trigger)
        elif isinstance(trigger, Expression):
            self.trigger_expression = trigger
        else:
            raise TypeError("trigger only supports str or Expression.")

        self.trigger_expression.create_ast(self)

    def evaluate_trigger(self) -> bool:
        """
        Evaluate trigger expression of this node.

        Notes
        -----
        该方法仅检查节点自己的触发器是否满足条件，节点是否满足运行条件还取决于父节点是否满足。

        ``resolve_dependencies`` 方法会自顶向下检查各节点触发器。
        """
        if self.trigger_expression is None:
            return True

        self.trigger_expression.create_ast(self)
        return self.trigger_expression.evaluate()

    def resolve_dependencies(self) -> bool:
        if self.is_suspended():
            return False

        if not self.evaluate_trigger():
            return False

        return True

    # Variable (Parameter, Event, Meter) -----------------------------

    def find_variable(self, name: str) -> Optional[Union[Event, Parameter, Meter]]:
        e = self.find_event(name)
        if e is not None:
            return e

        m = self.find_meter(name)
        if m is not None:
            return m

        return None

    # Parameter ------------------------------------------------------

    def add_parameter(self, name: str, value: Union[str, float, int, bool]):
        """
        Add a ``Parameter`` to this node.
        """
        p = Parameter(name=name, value=value)
        self.user_parameters[name] = p
        return p

    def find_parameter(self, name: str) -> Optional[Parameter]:
        """
        Find a ``parameter`` only in this node.
        """
        p = self.find_user_parameter(name)
        if p is not None:
            return p

        p = self.find_generated_parameter(name)
        if p is not None:
            return p

    def find_user_parameter(self, name: str) -> Optional[Parameter]:
        """
        Find user  ``parameter`` only in this node.
        """
        return self.user_parameters.get(name, None)

    # @abstractmethod
    def find_generated_parameter(self, name: str) -> Optional[Parameter]:
        """
        Find generated ``parameter`` only in this node.
        """
        return None

    def find_parent_parameter(self, name: str) -> Optional[Parameter]:
        """
        Find a ``Parameter`` up along the node tree.
        """
        p = self.find_parameter(name)
        if p is not None:
            return p

        parent_node = self.parent
        while parent_node is not None:
            p = parent_node.find_parameter(name)
            if p is not None:
                return p
            parent_node = parent_node.parent

        bunch = self.get_bunch()
        if bunch is None:
            return None

        return bunch.find_parameter(name)

    def update_generated_parameters(self):
        """
        Update generated parameters for this node.
        """
        pass

    def parameters(self) -> Dict[str, Parameter]:
        """
        Return all parameters accessible to this Node.
        """
        params = self.parameters_only().copy()

        parent_node = self.parent
        while parent_node is not None:
            parent_params = parent_node.parameters_only().copy()
            for key, p in parent_params.items():
                if key not in params:
                    params[key] = p
            parent_node = parent_node.parent

        bunch = self.get_bunch()
        if bunch is not None:
            bunch_params = bunch.parameters_only()
            for key, p in bunch_params.items():
                if key not in params:
                    params[key] = p

        return params

    def parameters_only(self) -> Dict[str, Parameter]:
        """
        Return all parameters in this Node.
        """
        user_params = self.user_parameters_only()
        generated_params = self.generated_parameters_only()

        params = {
            **user_params
        }
        for key, p in generated_params.items():
            if key not in params:
                params[key] = p

        return params

    def user_parameters_only(self) -> Dict[str, Parameter]:
        """
        Return user defined parameters in this Node.
        """
        return self.user_parameters

    def generated_parameters_only(self) -> Dict[str, Parameter]:
        """
        Return generated parameters
        """
        return dict()

    # Event ----------------------------------------------------------

    def add_event(self, name: str, initial_value: bool = False, check: bool = True) -> Event:
        if check:
            if self.find_event(name):
                raise RuntimeError(f"add event failed: event name is duplicate: {name}")

        event = Event(name, initial_value=initial_value)
        self.events.append(event)
        return event

    def set_event(self, name: str, value: bool) -> bool:
        event = self.find_event(name)
        if event is not None:
            event.value = value
            return True

        return False

    def find_event(self, name: str, ) -> Optional[Event]:
        for event in self.events:
            if event.name == name:
                return event
        return None

    def reset_event(self, name: str) -> bool:
        event = self.find_event(name)
        if event is not None:
            event.reset()
            return True

        return False

    # Meter ----------------------------------------------------------

    def add_meter(self, name: str, min_value: int, max_value: int) -> Meter:
        meter = Meter(name, min_value=min_value, max_value=max_value)
        self.meters.append(meter)
        return meter

    def set_meter(self, name: str, value: int) -> bool:
        meter = self.find_meter(name)
        if meter is not None:
            meter.value = value
            return True

        return False

    def find_meter(self, name: str) -> Optional[Meter]:
        for meter in self.meters:
            if meter.name == name:
                return meter
        return None

    def reset_meter(self, name: str) -> bool:
        meter = self.find_meter(name)
        if meter is not None:
            meter.reset()
            return True

        return False

    # Limit ----------------------------------------------------------

    def add_in_limit(self, limit_name: str, node_path: Optional[str] = None, tokens: int = 1):
        in_limit = InLimit(limit_name, node_path=node_path, tokens=tokens)
        self.in_limit_manager.add_in_limit(in_limit)

    def add_limit(self, name: str, limit: int):
        if self.find_limit(name) is not None:
            raise RuntimeError(f"add_limit failed: duplicate limit {name} for node {self.node_path}")
        item = Limit(name, limit)
        item.set_node(self)
        self.limits.append(item)

    def find_limit(self, name: str) -> Optional[Limit]:
        for item in self.limits:
            if item.name == name:
                return item
        return None

    def find_limit_up_node_tree(self, name: str) -> Optional[Limit]:
        item = self.find_limit(name)
        if item is not None:
            return item

        the_parent = self.parent
        while the_parent is not None:
            item = the_parent.find_limit(name)
            if item is not None:
                return item
            the_parent = self.parent

        return None

    def check_in_limit_up(self) -> bool:
        if not self.in_limit_manager.in_limit():
            return False

        the_parent = self.parent
        while the_parent is not None:
            if not the_parent.in_limit_manager.in_limit():
                return False
            the_parent = the_parent.parent

        return True

    def increment_in_limit(self, limit_set: Set[Limit]):
        node_path = self.node_path
        self.in_limit_manager.increment_in_limit(limit_set, node_path)

        the_parent = self.parent
        while the_parent is not None:
            the_parent.in_limit_manager.increment_in_limit(limit_set, node_path)
            the_parent = the_parent.parent

    def decrement_in_limit(self, limit_set: Set[Limit]):
        node_path = self.node_path
        self.in_limit_manager.decrement_in_limit(limit_set, node_path)

        the_parent = self.parent
        while the_parent is not None:
            the_parent.in_limit_manager.decrement_in_limit(limit_set, node_path)
            the_parent = the_parent.parent

    # Node Operations ------------------------------------------------

    def requeue(self):
        """
        Requeue the node itself, don't affect children nodes.

        Requeue operation sets node's status to ``NodeStatus.queued``
        """
        self.set_node_status_only(NodeStatus.queued)

        for event in self.events:
            event.reset()

    def suspend(self):
        self.state.suspended = True

    def resume(self):
        self.state.suspended = False
