import pytest


from takler.core import NodeStatus
from takler.core.expression_parser import parse_trigger
from takler.core.expression_ast import (
    AstOpEq, AstOpGt, AstOpGe,
    AstOpOr, AstOpAnd,
    AstNodePath, AstVariablePath, AstNodeStatus, AstInteger
)


def test_node_path():
    expr_cases = [
        "/flow1/task1 == complete",
        "./task1 == aborted",
        "../container1/task1 == complete",
        "../../container1/task1 == complete"
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        assert isinstance(ast.left, AstNodePath)


def test_variable_path():
    expr_cases = [
        "/flow1/task1:event1 == set",
        "./task1:meter1 >= 20",
        "../container1/task1:event2 == set",
        "../../container1/task1:meter2 > 10"
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        assert isinstance(ast.left, AstVariablePath)


def test_op_eq():
    expr_cases = [
        "/flow1/task1 == complete",
        "/flow1/task1 eq complete",
        "/flow1/task1 EQ complete",
        "/flow1/task1 eQ complete",
        "/flow1/task1 Eq complete",
        "/flow1/task1:event1 == set",
        "/flow1/task1:meter1 == 10",  # not suggested.
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        assert isinstance(ast, AstOpEq)


def test_op_gt():
    expr_cases = [
        "/flow1/task1:meter1 > 20"
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        assert isinstance(ast, AstOpGt)


def test_op_ge():
    expr_cases = [
        "/flow1/task1:meter1 >= 20"
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        assert isinstance(ast, AstOpGe)


def test_op_and():
    expr_cases = [
        "/flow1/task1 == complete and /flow1/task2 == complete",
        "/flow1/task1 == complete AND /flow1/task2 == complete",
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        assert isinstance(ast, AstOpAnd)


def test_op_or():
    expr_cases = [
        "/flow1/task1 == complete or /flow1/task2 == complete",
        "/flow1/task1 == complete OR /flow1/task2 == complete",
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        assert isinstance(ast, AstOpOr)


def test_status_complete():
    expr_cases = [
        "/flow1/task1 == complete",
        "/flow1/task1 == COMPLETE",
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        ast_right = ast.right
        assert isinstance(ast_right, AstNodeStatus)
        assert ast_right.value() == NodeStatus.complete


def test_status_abort():
    expr_cases = [
        "/flow1/task1 == aborted",
        "/flow1/task1 == ABORTED",
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        ast_right = ast.right
        assert isinstance(ast_right, AstNodeStatus)
        assert ast_right.value() == NodeStatus.aborted


def test_event_set():
    expr_cases = [
        "/flow1/task1:event1 == set",
        "/flow1/task1:event1 == SET"
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        ast_right = ast.right
        assert isinstance(ast_right, AstInteger)
        assert ast_right.value() == 1


def test_event_unset():
    expr_cases = [
        "/flow1/task1:event1 == unset",
        "/flow1/task1:event1 == UNSET"
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        ast_right = ast.right
        assert isinstance(ast_right, AstInteger)
        assert ast_right.value() == 0


def test_meter_value():
    expr_cases = [
        "/flow1/task1:meter1 == 10",
        "/flow1/task1:meter1 > 10",
        "/flow1/task1:meter1 >= 10",
    ]
    for expr_string in expr_cases:
        ast = parse_trigger(expr_string)
        ast_right = ast.right
        assert isinstance(ast_right, AstInteger)
        assert ast_right.value() == 10

