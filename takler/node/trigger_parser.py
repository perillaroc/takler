# coding: utf-8
from pyparsing import Word, Literal, alphas, alphanums, OneOrMore, ZeroOrMore, infixNotation, opAssoc, oneOf


node_name = Word(alphanums + '_')

node_path = OneOrMore(node_name | Literal('/') | Literal('.') | Literal('..'))

operator = Literal("==")

status = Literal('complete') | Literal('aborted')

logical_operator = Literal('and') | Literal('or')

single_trigger_expr = node_path.setResultsName("node_path").setParseAction(lambda t: ''.join(t)) \
               + operator.setResultsName("operator") \
               + status.setResultsName("status")

trigger_expr = infixNotation(
    single_trigger_expr.setResultsName("single_expr"),
    [(oneOf("and", "AND"), 2, opAssoc.LEFT),
    (oneOf("or", "OR"), 2, opAssoc.RIGHT)]
)


def parse_trigger(trigger):
    return single_trigger_expr.parseString(trigger)
