from typing import TYPE_CHECKING, Optional, Set, List


if TYPE_CHECKING:
    from .node import Node


class Limit:
    def __init__(self, name: str, limit: int):
        self.name: str = name
        self.limit: int = limit
        self.value: int = 0
        self.node: Optional["Node"] = None
        self.node_paths: Set[str] = set()

    def set_node(self, node: "Node"):
        self.node = node

    def in_limit(self, tokens: int) -> bool:
        return self.value + tokens <= self.limit

    def increment(self, tokens: int, node_path: str):
        if node_path in self.node_paths:
            return
        self.node_paths.add(node_path)
        self.value += tokens

    def decrement(self, tokens: int, node_path: str):
        if node_path not in self.node_paths:
            return
        self.node_paths.remove(node_path)
        self.value -= tokens
        if self.value < 0:
            self.value = 0
            self.node_paths.clear()

    def reset(self):
        self.node_paths.clear()
        self.value = 0


class InLimit:
    def __init__(self, limit_name: str, node_path: str = None, tokens: int = 1):
        self.limit_name: str = limit_name
        self.tokens: int = tokens

        # self.node: Optional[Node] = None
        self.node_path: Optional[str] = node_path
        self.limit: Optional[Limit] = None

    def set_limit(self, limit: Limit):
        self.limit = limit


class InLimitManager:
    def __init__(self, node: "Node"):
        self.node: "Node" = node

        self.in_limit_list: List[InLimit] = list()

    # Access ----------------------------------------

    def add_in_limit(self, in_limit: InLimit):
        if self.find_in_limit(in_limit):
            raise RuntimeError(f"add_in_limit failed: duplicate InLimit in node: {self.node.node_path}")
        self.in_limit_list.append(in_limit)

    def delete_in_limit(self, name: str) -> bool:
        raise NotImplementedError()

    def find_in_limit(self, in_limit: InLimit) -> bool:
        for item in self.in_limit_list:
            if (
                    ((item.limit_name is None and in_limit.limit_name is None) or (item.limit_name == in_limit.limit_name))
                    and ((item.node_path is None and in_limit.node_path is None) or (item.node_path == in_limit.node_path))
            ):
                return True
        return False

    # Check ------------------------------

    def in_limit(self) -> bool:
        if len(self.in_limit_list) == 0:
            return True

        self.resolve_in_limit_references()

        valid_in_limit_count = 0
        fitted_in_limit_count = 0
        for item in self.in_limit_list:
            if item.limit is None:
                continue

            valid_in_limit_count += 1
            if item.limit.in_limit(item.tokens):
                fitted_in_limit_count += 1

        return valid_in_limit_count == fitted_in_limit_count

    # Change ------------------------------------------

    def increment_in_limit(self, limit_set: Set[Limit], node_path: str):
        if len(self.in_limit_list) == 0:
            return

        self.resolve_in_limit_references()

        for item in self.in_limit_list:
            current_limit = item.limit
            if current_limit is None:
                continue
            if current_limit in limit_set:
                continue

            limit_set.add(current_limit)
            current_limit.increment(item.tokens, node_path)

    def decrement_in_limit(self, limit_set: Set[Limit], node_path: str):
        if len(self.in_limit_list) == 0:
            return

        self.resolve_in_limit_references()

        for item in self.in_limit_list:
            current_limit = item.limit
            if current_limit is None:
                continue
            if current_limit in limit_set:
                continue

            limit_set.add(current_limit)
            current_limit.decrement(item.tokens, node_path)

    # Inner use ---------------------------------------

    def resolve_in_limit_references(self):
        for item in self.in_limit_list:
            self.resolve_in_limit(item)

    def resolve_in_limit(self, in_limit: InLimit):
        if in_limit.limit is not None:
            return

        # find limit
        if in_limit.node_path is None:
            limit = self.node.find_limit_up_node_tree(in_limit.limit_name)
            if limit is not None:
                in_limit.set_limit(limit)
            return
        else:
            reference_node = self.node.find_node(in_limit.node_path)
            if reference_node is None:
                return

            limit = reference_node.find_limit(in_limit.limit_name)
            if limit is not None:
                in_limit.set_limit(limit)
            return
