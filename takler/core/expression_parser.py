from lark import Lark, Transformer

from .expression_ast import AstNodePath, AstOpEq, AstNodeStatus, AstRoot
from .state import NodeStatus


class ExpressionTransformer(Transformer):
    def node_path(self, items):
        return AstNodePath("".join(items))

    def node_name(self, s):
        (s, ) = s
        return s

    def st_complete(self, _):
        return AstNodeStatus(NodeStatus.complete)

    def op_eq(self, _):
        return AstOpEq()

    def expression(self, s):
        s[1].left = s[0]
        s[1].right = s[2]
        return s[1]


trigger_parser = Lark(r"""
    !node_path: "/"node_name("/"node_name)*

    op_eq: "==" | "eq"
    op_gt: ">"
    op_ge: ">="
    ?operator: op_eq | op_gt | op_ge

    st_complete: "complete"
    st_aborted: "aborted"
    ?status: st_complete | st_aborted

    node_name: CNAME

    expression: node_path operator status 

    %import common.CNAME
    %import common.WORD
    %import common.WS
    %ignore WS
""", start="expression")


def parse_trigger(trigger_text: str) -> AstRoot:
    tree = trigger_parser.parse(trigger_text)
    expression_ast = ExpressionTransformer().transform(tree)
    return expression_ast
