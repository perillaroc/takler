from dataclasses import dataclass
from typing import Optional

import pytest

from takler.core import Task, NodeContainer, Flow
from takler.visitor import pre_order_travel, SimplePrintVisitor


@pytest.fixture
def flow_objects():
    """
    Flow:

        |- flow1 [unknown]
          |- container1 [unknown]
            |- task1 [unknown]
            |- container2 [unknown]
              |- task2 [unknown]
              |- task3 [unknown]
          |- task4 [unknown]
          |- container3 [unknown]
            |- task5 [unknown]
          |- task6 [unknown]

    """
    flow1 = Flow("flow1")
    container1 = flow1.add_container("container1")
    task1 = container1.add_task("task1")
    container2 = container1.add_container("container2")
    task2 = container2.add_task("task2")
    task3 = container2.add_task("task3")
    task4 = flow1.add_task("task4")
    container3 = flow1.add_container("container3")
    task5 = container3.add_task("task5")
    task6 = flow1.add_task("task6")
    return dict(
        flow1=flow1,
        container1=container1,
        task1=task1,
        container2=container2,
        task2=task2,
        task3=task3,
        task4=task4,
        container3=container3,
        task5=task5,
        task6=task6
    )


def test_node_path(flow_objects):
    assert flow_objects["flow1"].node_path == "/flow1"
    assert flow_objects["container1"].node_path == "/flow1/container1"
    assert flow_objects["task1"].node_path == "/flow1/container1/task1"
    assert flow_objects["container2"].node_path == "/flow1/container1/container2"
    assert flow_objects["task2"].node_path == "/flow1/container1/container2/task2"
    assert flow_objects["task3"].node_path == "/flow1/container1/container2/task3"
    assert flow_objects["task4"].node_path == "/flow1/task4"
    assert flow_objects["container3"].node_path == "/flow1/container3"
    assert flow_objects["task5"].node_path == "/flow1/container3/task5"
    assert flow_objects["task6"].node_path == "/flow1/task6"


def test_get_root(flow_objects):
    flow1 = flow_objects["flow1"]

    assert flow_objects["flow1"].get_root() == flow1
    assert flow_objects["container1"].get_root() == flow1
    assert flow_objects["task1"].get_root() == flow1
    assert flow_objects["container2"].get_root() == flow1
    assert flow_objects["task2"].get_root() == flow1
    assert flow_objects["task3"].get_root() == flow1
    assert flow_objects["task4"].get_root() == flow1
    assert flow_objects["container3"].get_root() == flow1
    assert flow_objects["task5"].get_root() == flow1
    assert flow_objects["task6"].get_root() == flow1


def test_is_leaf_node(flow_objects):
    assert not flow_objects["flow1"].is_leaf_node()
    assert not flow_objects["container1"].is_leaf_node()
    assert flow_objects["task1"].is_leaf_node()
    assert not flow_objects["container2"].is_leaf_node()
    assert flow_objects["task2"].is_leaf_node()
    assert flow_objects["task3"].is_leaf_node()
    assert flow_objects["task4"].is_leaf_node()
    assert not flow_objects["container3"].is_leaf_node()
    assert flow_objects["task5"].is_leaf_node()
    assert flow_objects["task6"].is_leaf_node()


def test_find_node(flow_objects):
    @dataclass
    class QueryOption:
        node_name: str
        node_path: str

    @dataclass
    class TestCase:
        query: QueryOption
        expected_node_name: Optional[str]

    def do_tests(cases):
        for test_case in cases:
            node = flow_objects[test_case.query.node_name]
            if test_case.expected_node_name is None:
                expected_node = None
            else:
                expected_node = flow_objects[test_case.expected_node_name]
            assert node.find_node(test_case.query.node_path) == expected_node

    test_cases = [
        TestCase(
            query=QueryOption(node_name="flow1", node_path="flow1/container1"),
            expected_node_name="container1",
        ),
        TestCase(
            query=QueryOption(node_name="flow1", node_path="/flow1/container1"),
            expected_node_name="container1",
        ),
        TestCase(
            query=QueryOption(node_name="flow1", node_path="/flow1/container3/task5"),
            expected_node_name="task5",
        ),
        TestCase(
            query=QueryOption(node_name="flow1", node_path="container1"),
            expected_node_name=None,
        ),
    ]

    do_tests(cases=test_cases)

    test_cases = [
        TestCase(
            query=QueryOption(node_name="container1", node_path="container1/task1"),
            expected_node_name="task1",
        ),
        TestCase(
            query=QueryOption(node_name="container1", node_path="task4"),
            expected_node_name="task4",
        ),

        TestCase(
            query=QueryOption(node_name="task4", node_path="./container3"),
            expected_node_name="container3",
        ),
    ]

    do_tests(cases=test_cases)

    test_cases = [
        TestCase(
            query=QueryOption(node_name="task2", node_path="./task3"),
            expected_node_name="task3",
        ),
        TestCase(
            query=QueryOption(node_name="task2", node_path="../task1"),
            expected_node_name="task1",
        ),
        TestCase(
            query=QueryOption(node_name="task2", node_path="../../task4"),
            expected_node_name="task4",
        )
    ]
    do_tests(cases=test_cases)

