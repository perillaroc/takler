from typing import Optional, TYPE_CHECKING
from .expression_parser import parse_trigger
from .expression_ast import AstRoot


if TYPE_CHECKING:
    from .node import Node


class Expression:
    def __init__(self, expression_str: str):
        self.free: bool = False
        self.ast: Optional[AstRoot] = None
        self.expression_str: str = expression_str

    def create_ast(self, parent_node: "Node"):
        self.parse_expression()
        self.ast.set_parent_node(parent_node)

    def evaluate(self) -> bool:
        return self.ast.evaluate()

    def parse_expression(self):
        self.ast = parse_trigger(self.expression_str)
