from dataclasses import dataclass
from typing import Optional, Mapping

import pytest

from takler.core import Task, NodeContainer, Flow
from takler.core.node import Node
from takler.core.state import NodeStatus


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


def test_flow_requeue(flow_objects: Mapping[str, Node]):
    flow1 = flow_objects["flow1"]
    flow1.requeue()

    for name, node in flow_objects.items():
        assert node.state.node_status == NodeStatus.queued


@pytest.fixture
def flow_objects_case_2():
    """
    Flow:

        |- flow1 [active]
          |- container1 [active]
            |- task1 [queued]
            |- container2 [active]
              |- task2 [active]
              |- task3 [queued]
          |- task4 [queued]

    """
    flow1 = Flow("flow1")
    flow1.set_node_status_only(NodeStatus.active)
    container1 = flow1.add_container("container1")
    container1.set_node_status_only(NodeStatus.active)
    task1 = container1.add_task("task1")
    task1.set_node_status_only(NodeStatus.queued)
    container2 = container1.add_container("container2")
    container2.set_node_status_only(NodeStatus.active)
    task2 = container2.add_task("task2")
    task2.set_node_status_only(NodeStatus.active)
    task3 = container2.add_task("task3")
    task3.set_node_status_only(NodeStatus.queued)
    task4 = flow1.add_task("task4")
    task4.set_node_status_only(NodeStatus.queued)
    return dict(
        flow1=flow1,
        container1=container1,
        task1=task1,
        container2=container2,
        task2=task2,
        task3=task3,
        task4=task4,
    )


def test_container_requeue(flow_objects_case_2):
    container2 = flow_objects_case_2["container2"]
    container2.requeue()

