from typing import Mapping

import pytest

from takler.core import Flow, NodeStatus
from takler.core.node import Node


class ObjectContainer:
    pass


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
    oc = ObjectContainer()
    flow1 = Flow("flow1")
    oc.flow1 = flow1
    container1 = flow1.add_container("container1")
    oc.container1 = container1
    task1 = container1.add_task("task1")
    oc.task1 = task1
    container2 = container1.add_container("container2")
    oc.container2 = container2
    task2 = container2.add_task("task2")
    oc.task2 = task2
    task3 = container2.add_task("task3")
    oc.task3 = task3
    task4 = flow1.add_task("task4")
    oc.task4 = task4
    container3 = flow1.add_container("container3")
    oc.container3 = container3
    task5 = container3.add_task("task5")
    oc.task5 = task5
    task6 = flow1.add_task("task6")
    oc.task6 = task6
    return oc


def test_flow_requeue(flow_objects):
    flow1 = flow_objects.flow1
    flow1.requeue()

    for name, node in vars(flow_objects).items():
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
          |- task4 [complete]

    """
    oc = ObjectContainer()
    flow1 = Flow("flow1")
    oc.flow1 = flow1
    flow1.set_node_status_only(NodeStatus.active)
    container1 = flow1.add_container("container1")
    oc.container1 = container1
    container1.set_node_status_only(NodeStatus.active)
    task1 = container1.add_task("task1")
    oc.task1 = task1
    task1.set_node_status_only(NodeStatus.queued)
    container2 = container1.add_container("container2")
    oc.container2 = container2
    container2.set_node_status_only(NodeStatus.active)
    task2 = container2.add_task("task2")
    oc.task2 = task2
    task2.set_node_status_only(NodeStatus.active)
    task3 = container2.add_task("task3")
    oc.task3 = task3
    task3.set_node_status_only(NodeStatus.queued)
    task4 = flow1.add_task("task4")
    oc.task4 = task4
    task4.set_node_status_only(NodeStatus.complete)
    return oc


def test_container_requeue(flow_objects_case_2):
    container2 = flow_objects_case_2.container2
    container2.requeue()

    """
    Flow:

        |- flow1 [active]
          |- container1 [active]
            |- task1 [queued]
            |- container2 [queued]
              |- task2 [queued]
              |- task3 [queued]
          |- task4 [complete]
    """
    assert flow_objects_case_2.flow1.state.node_status == NodeStatus.active
    assert flow_objects_case_2.container1.state.node_status == NodeStatus.active
    assert flow_objects_case_2.task1.state.node_status == NodeStatus.queued
    assert flow_objects_case_2.container2.state.node_status == NodeStatus.queued
    assert flow_objects_case_2.task2.state.node_status == NodeStatus.queued
    assert flow_objects_case_2.task3.state.node_status == NodeStatus.queued
    assert flow_objects_case_2.task4.state.node_status == NodeStatus.complete

