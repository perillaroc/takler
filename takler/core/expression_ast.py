from dataclasses import dataclass
from typing import Optional

from .state import NodeStatus


@dataclass
class AstBase:
    def set_parent_node(self, node):
        pass

    def value(self):
        raise NotImplemented()

    def evaluate(self) -> bool:
        raise NotImplemented()


@dataclass
class AstRoot(AstBase):
    left: Optional[AstBase] = None
    right: Optional[AstBase] = None

    def set_parent_node(self, node):
        self.left.set_parent_node(node)
        self.right.set_parent_node(node)


@dataclass
class AstOpEq(AstRoot):
    def evaluate(self):
        return self.left.value() == self.right.value()


@dataclass
class AstOpAnd(AstRoot):
    def evaluate(self):
        return self.left.evaluate() and self.right.evaluate()


@dataclass
class AstNodePath(AstBase):
    node_path: str
    parent_node: Optional = None
    _reference_node: Optional = None

    def set_parent_node(self, node):
        self.parent_node = node
        ref_node = self.get_reference_node()
        if ref_node is None:
            raise ValueError(f"node path '{self.node_path}' is not found from node '{self.parent_node.node_path}'")

    def value(self):
        ref_node = self.get_reference_node()
        if ref_node is not None:
            return ref_node.state.node_status
        else:
            return NodeStatus.unknown

    def get_reference_node(self) -> Optional:
        """
        Find node only once.
        """
        if self._reference_node is not None:
            return self._reference_node

        if self.parent_node is not None:
            self._reference_node = self.parent_node.find_node(self.node_path)
            return self._reference_node
        return None


@dataclass
class AstNodeStatus(AstBase):
    node_status: NodeStatus

    def value(self):
        return self.node_status