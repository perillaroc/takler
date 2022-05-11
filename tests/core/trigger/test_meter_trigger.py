import pytest

from takler.core import Flow, Task


class ObjectContainer:
    pass


@pytest.fixture
def meter_simple_case_1():
    """
    A simple flow with only three tasks.

    |- flow1
        |- task1
            meter: meter1
            event: event2
        |- task2
            trigger task1:event1 == set
        |- task3
            trigger task1:event2 == set
    """
    result = ObjectContainer()

    flow1 = Flow("flow1")
    result.flow1 = flow1

    with flow1.add_task("task1") as task1:
        result.task1 = task1
        task1.add_meter("meter1", 0, 10)

    with flow1.add_task("task2") as task2:
        result.task2 = task2
        task2.add_trigger("./task1:meter1 >= 4")

    with flow1.add_task("task3") as task3:
        result.task3 = task3
        task3.add_trigger("./task1:meter1 >= 8")

    flow1.requeue()

    return result


def test_evaluate_meter(meter_simple_case_1):
    task1: Task = meter_simple_case_1.task1
    task2: Task = meter_simple_case_1.task2
    task3: Task = meter_simple_case_1.task3

    assert not task2.evaluate_trigger()
    assert not task3.evaluate_trigger()

    task1.set_meter("meter1", 2)
    assert not task2.evaluate_trigger()
    assert not task3.evaluate_trigger()

    task1.set_meter("meter1", 4)
    assert task2.evaluate_trigger()
    assert not task3.evaluate_trigger()

    task1.set_meter("meter1", 6)
    assert task2.evaluate_trigger()
    assert not task3.evaluate_trigger()

    task1.set_meter("meter1", 8)
    assert task2.evaluate_trigger()
    assert task3.evaluate_trigger()

    task1.set_meter("meter1", 10)
    assert task2.evaluate_trigger()
    assert task3.evaluate_trigger()
