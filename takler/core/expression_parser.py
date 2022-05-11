from lark import Lark, Transformer

from .expression_ast import (
    AstNodePath, AstOpEq, AstOpAnd, AstNodeStatus, AstRoot,
    AstVariablePath, AstEventValue
)
from .state import NodeStatus


class ExpressionTransformer(Transformer):
    """
    Transform Lark tokens into takler expression AST.
    """
    def node_path(self, items) -> AstNodePath:
        return AstNodePath("".join(items))

    def variable_path(self, items) -> AstVariablePath:
        node = items[0]
        variable_name = items[2]
        return AstVariablePath(node=node, variable_name=variable_name)

    # def node_name(self, s: str) -> str:
    #     (s, ) = s
    #     return s

    def st_complete(self, _) -> AstNodeStatus:
        """Node status: complete"""
        return AstNodeStatus(NodeStatus.complete)

    def st_aborted(self, _) -> AstNodeStatus:
        """Node status: complete"""
        return AstNodeStatus(NodeStatus.aborted)

    def op_eq(self, _) -> AstOpEq:
        """Operation: equal (==)"""
        return AstOpEq()

    def op_and(self, _) -> AstOpAnd:
        """Operation: and"""
        return AstOpAnd()

    def event_set(self, _) -> AstEventValue:
        return AstEventValue(1)

    def event_unset(self, _) -> AstEventValue:
        return AstEventValue(0)

    def expression(self, s):
        s[1].left = s[0]
        s[1].right = s[2]
        return s[1]


# Lark version of expression trigger parser.
trigger_parser: Lark = Lark(r"""
    !node_path: ("."|"..")?"/"node_name("/"node_name)*
    !variable_path: node_path":"variable_name
    path: node_path | variable_path

    op_eq: "==" | "eq"i
    op_gt: ">"
    op_ge: ">="
    op_and: "and"i
    ?operator: op_eq | op_gt | op_ge | op_and

    st_complete: "complete"i
    st_aborted: "aborted"i
    ?status: st_complete | st_aborted
    
    event_set: "set"i
    event_unset: "unset"i
    ?event_value: event_set|event_unset

    ?node_name: CNAME | "." | ".."
    ?variable_name: CNAME

    expression: (node_path operator status) 
              | (variable_path operator event_value)
              | (expression op_and expression) 

    %import common.CNAME
    %import common.WORD
    %import common.WS
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
