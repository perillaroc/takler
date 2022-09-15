import sys

import pytest

from takler.core import Limit, Flow, Task
from takler.visitor import pre_order_travel, PrintVisitor


def test_create_limit():
    limit_count = 20
    limit_name = "post_limit"
    limit = Limit(limit_name, limit_count)
    assert limit.name == limit_name
    assert limit.limit == limit_count
    assert limit.value == 0


def test_limit_increment():
    limit = Limit("post_limit", 2)
    assert len(limit.node_paths) == 0

    limit.increment(1, "/flow1/task1")
    assert len(limit.node_paths) == 1

    limit.increment(1, "/flow1/task2")
    assert len(limit.node_paths) == 2


def test_limit_decrement():
    limit = Limit("post_limit", 2)
    assert len(limit.node_paths) == 0

    limit.increment(1, "/flow1/task1")
    limit.increment(1, "/flow1/task2")
    assert len(limit.node_paths) == 2

    limit.decrement(1, "/flow1/task1")
    assert len(limit.node_paths) == 1
    limit.decrement(1, "/flow1/task2")
    assert len(limit.node_paths) == 0


def test_limit_in_limit():
    limit = Limit("post_limit", 2)
    assert limit.in_limit(1)
    assert limit.in_limit(2)
    assert not limit.in_limit(3)

    limit.increment(1, "/flow1/task1")
    assert limit.in_limit(1)
    assert not limit.in_limit(2)
    assert not limit.in_limit(3)

    limit.increment(1, "/flow1/task2")
    assert not limit.in_limit(1)
    assert not limit.in_limit(2)
    assert not limit.in_limit(3)


class ObjectContainer:
    pass


@pytest.fixture
def flow_with_limit():
    """

        flow1
            limit limit1 2
            limit limit2 1
            inlimit limit1
            container1
                task1
                task2
            container2
                inlimit limit2
                task3
                task4

    """
    oc = ObjectContainer()
    with Flow("flow1") as flow1:
        oc.flow1 = flow1
        flow1.add_limit("limit1", 2)
        flow1.add_limit("limit2", 1)
        flow1.add_in_limit("limit1")
        with flow1.add_container("container1") as container1:
            oc.container1 = container1
            with container1.add_task("task1") as task1:
                oc.task1 = task1
            with container1.add_task("task2") as task2:
                oc.task2 = task2
        with flow1.add_container("container2") as container2:
            oc.container2 = container2
            container2.add_in_limit("limit2")
            with container2.add_task("task3") as task3:
                oc.task3 = task3
            with container2.add_task("task4") as task4:
                oc.task4 = task4

    return oc


def test_flow_with_limit(flow_with_limit):
    pre_order_travel(flow_with_limit.flow1, PrintVisitor(sys.stdout))


def test_manual_run(flow_with_limit):
    # pre_order_travel(flow_with_limit.flow1, SimplePrintVisitor())
    flow1: Flow = flow_with_limit.flow1
    task1: Task = flow_with_limit.task1
    task2: Task = flow_with_limit.task2
    task3: Task = flow_with_limit.task3
    task4: Task = flow_with_limit.task4

    limit1 = flow1.find_limit("limit1")
    assert limit1 is not None
    limit2 = flow1.find_limit("limit2")
    assert limit2 is not None

    flow1.requeue()

    assert limit1.value == 0
    assert limit2.value == 0

    # Task1 run
    assert task1.check_in_limit_up()
    task1.run()
    assert limit1.value == 1
    assert limit2.value == 0
    task1.init("1001")
    assert limit1.value == 1
    assert limit2.value == 0

    # Task2 run
    assert task2.check_in_limit_up()
    task2.run()
    assert limit1.value == 2
    assert limit2.value == 0

    assert not task3.check_in_limit_up()

    # Task1 finish
    task1.complete()
    assert limit1.value == 1
    assert limit2.value == 0

    assert task3.check_in_limit_up()

    # Task3 run
    task3.run()
    assert limit1.value == 2
    assert limit2.value == 1

    assert not task4.check_in_limit_up()

    # Task2 complete
    task2.complete()
    assert limit1.value == 1
    assert limit2.value == 1

    assert not task4.check_in_limit_up()

    # Task3 complete
    task3.complete()
    assert limit1.value == 0
    assert limit2.value == 0

    assert task4.check_in_limit_up()

    # Task4 run
    task4.run()
    assert limit1.value == 1
    assert limit2.value == 1

    # Task4 complete
    task4.complete()
    assert limit1.value == 0
    assert limit2.value == 0
