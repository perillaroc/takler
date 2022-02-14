from typing import Mapping

import pytest

from takler.core import Flow, Task
from takler.core.state import NodeStatus
from takler.core.node import Node


@pytest.fixture
def unknown_flow() -> Mapping[str, Node]:
    """
    Flow:

        |- flow1 [queued]
          |- container1 [queued]
            |- task1 [queued]
            |- container2 [queued]
              |- task2 [queued]
              |- task3 [queued]
          |- task4 [queued]
          |- container3 [queued]
            |- task5 [queued]
          |- task6 [queued]

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


@pytest.fixture
def queued_flow(unknown_flow) -> Mapping[str, Node]:
    unknown_flow["flow1"].requeue()
    return unknown_flow


def test_init_task1(queued_flow: Mapping[str, Node]):
    task1 = queued_flow["task1"]  # type: Task
    task1.init()

    """
    Flow:

        |- flow1 [active]
          |- container1 [active]
            |- task1 [active]
            |- container2 [queued]
              |- task2 [queued]
              |- task3 [queued]
          |- task4 [queued]
          |- container3 [queued]
            |- task5 [queued]
          |- task6 [queued]
    """

    assert queued_flow["flow1"].state.node_status == NodeStatus.active
    assert queued_flow["container1"].state.node_status == NodeStatus.active
    assert queued_flow["task1"].state.node_status == NodeStatus.active
    assert queued_flow["container2"].state.node_status == NodeStatus.queued
    assert queued_flow["task2"].state.node_status == NodeStatus.queued
    assert queued_flow["task3"].state.node_status == NodeStatus.queued
    assert queued_flow["task4"].state.node_status == NodeStatus.queued


def test_init_task3(queued_flow: Mapping[str, Node]):
    task3 = queued_flow["task3"]  # type: Task
    task3.init()

    """
    Flow:

        |- flow1 [active]
          |- container1 [active]
            |- task1 [queued]
            |- container2 [active]
              |- task2 [queued]
              |- task3 [active]
          |- task4 [queued]
          |- container3 [queued]
            |- task5 [queued]
          |- task6 [queued]
    """

    assert queued_flow["flow1"].state.node_status == NodeStatus.active
    assert queued_flow["container1"].state.node_status == NodeStatus.active
    assert queued_flow["task1"].state.node_status == NodeStatus.queued
    assert queued_flow["container2"].state.node_status == NodeStatus.active
    assert queued_flow["task2"].state.node_status == NodeStatus.queued
    assert queued_flow["task3"].state.node_status == NodeStatus.active
    assert queued_flow["task4"].state.node_status == NodeStatus.queued
