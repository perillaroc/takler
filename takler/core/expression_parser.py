from lark import Lark, Transformer

from .expression_ast import (
    AstNodePath, AstOpEq, AstOpAnd, AstOpOr, AstOpGt, AstOpGe,
    AstNodeStatus, AstRoot,
    AstVariablePath, AstInteger,
)
from .state import NodeStatus


class ExpressionTransformer(Transformer):
    """
    Transform Lark tokens into takler expression AST.
    """
    def node_path(self, items) -> AstNodePath:
        """
        path for a Node, including Flow, NodeContainer and Task
        """
        return AstNodePath("".join(items))

    def variable_path(self, items) -> AstVariablePath:
        """
        path for a variable, include node and attribute
        """
        node = items[0]
        variable_name = items[2]
        return AstVariablePath(node=node, variable_name=variable_name)

    def pure_node_name(self, items) -> str:
        """
        a "true" node name, excluding . and ..
        """
        return "".join(items)

    def dot(self, _) -> str:
        """
        node name for current node.
        """
        return "."

    def double_dot(self, _) -> str:
        """
        node name for parent node.
        """
        return ".."

    def st_complete(self, _) -> AstNodeStatus:
        """Node status: complete"""
        return AstNodeStatus(NodeStatus.complete)

    def st_aborted(self, _) -> AstNodeStatus:
        """Node status: complete"""
        return AstNodeStatus(NodeStatus.aborted)

    def op_eq(self, _) -> AstOpEq:
        """Operator: equal (==)"""
        return AstOpEq()

    def op_gt(self, _) -> AstOpGt:
        """Operator: greater than (>)"""
        return AstOpGt()

    def op_ge(self, _) -> AstOpGe:
        """Operator: greater equal than (>=)"""
        return AstOpGe()

    def op_and(self, _) -> AstOpAnd:
        """Operator: and"""
        return AstOpAnd()

    def op_or(self, _) -> AstOpOr:
        """Operator: or"""
        return AstOpOr()

    def event_set(self, _) -> AstInteger:
        """
        event is set.
        """
        return AstInteger(1)

    def event_unset(self, _) -> AstInteger:
        """
        event is unset
        """
        return AstInteger(0)

    def meter_value(self, s) -> AstInteger:
        """
        value of meter
        """
        return AstInteger(int(s[0]))

    def expression(self, s):
        """
        trigger expression, start from here.
        """
        if len(s) == 3:
            s[1].left = s[0]
            s[1].right = s[2]
            return s[1]
        elif len(s) == 1:
            return s[0]
        else:
            raise ValueError(f"value is not supported: {s}")


# Lark version of expression trigger parser.
trigger_parser: Lark = Lark(r"""
    !node_path: ("."|"..")?"/"node_name("/"node_name)*
    !variable_path: node_path":"variable_name
    path: node_path | variable_path

    op_eq: "==" | "eq"i
    op_gt: ">"
    op_ge: ">="
    op_and: "and"i
    op_or: "or"i
    ?operator: op_eq | op_gt | op_ge
    ?logical_operator: op_and | op_or

    st_complete: "complete"i
    st_aborted: "aborted"i
    ?status: st_complete | st_aborted
    
    event_set: "set"i
    event_unset: "unset"i
    ?event_value: event_set|event_unset
    
    meter_value: NUMBER

    ?node_name: pure_node_name | dot | double_dot
    dot: "."
    double_dot: ".."
    !pure_node_name: (LETTER|DIGIT)("_"|LETTER|DIGIT)*
    ?variable_name: CNAME

    expression: "(" expression ")"
              | (node_path operator status) 
              | (variable_path operator event_value)
              | (variable_path operator meter_value)
              | (expression logical_operator expression)

    %import common.CNAME
    %import common.DIGIT
    %import common.LETTER
    %import common.WORD
    %import common.WS
    %import common.NUMBER
    %ignore WS
""", start="expression")


def parse_trigger(trigger_text: str) -> AstRoot:
    """
    Parse trigger expression string and return expression's AST.

    Parameters
    ----------
    trigger_text
        trigger expression string

    Returns
    -------
    AstRoot
    """
    tree = trigger_parser.parse(trigger_text)
    expression_ast = ExpressionTransformer().transform(tree)
    return expression_ast
