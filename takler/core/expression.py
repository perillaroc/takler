from typing import Optional, Union

from .expression_parser import parse_trigger
from .expression_ast import AstRoot


class Expression(object):
    def __init__(self, expression_str: str):
        self.free = False  # type: bool
        self.ast = None  # type: Optional[AstRoot]
        self.expression_str = expression_str  # type: str

    def create_ast(self, parent_node):
        self.parse_expression()
        self.ast.set_parent_node(parent_node)

    def evaluate(self) -> bool:
        return self.ast.evaluate()

    def parse_expression(self):
        self.ast = parse_trigger(self.expression_str)
