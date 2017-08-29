# coding: utf-8
from pyparsing import Word, Literal, alphas, alphanums, OneOrMore


node_name = Word(alphanums + '_')

node_path = OneOrMore(node_name | Literal('/') | Literal('.') | Literal('..'))

operator = Literal("==")

status = Literal('complete') | Literal('aborted')

trigger_expr = node_path.setResultsName("node_path").setParseAction(lambda t: ''.join(t)) \
               + operator.setResultsName("operator") \
               + status.setResultsName("status")


def parse_trigger(trigger):
    return trigger_expr.parseString(trigger)
