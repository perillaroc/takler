import pytest

from takler.core import Flow, Event, Task


class ObjectContainer:
    pass


@pytest.fixture
def event_simple_case_1():
    """
    A simple flow with only three tasks.

    |- flow1
        |- task1
            event: event1
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
        task1.add_event("event1")
        task1.add_event("event2")

    with flow1.add_task("task2") as task2:
        result.task2 = task2
        task2.add_trigger("./task1:event1 == set")

    with flow1.add_task("task3") as task3:
        result.task3 = task3
        task3.add_trigger("./task1:event2==set")

    flow1.requeue()

    return result


def test_evaluate_event(event_simple_case_1):
    task1: Task = event_simple_case_1.task1
    task2: Task = event_simple_case_1.task2
    task3: Task = event_simple_case_1.task3

    assert not task2.evaluate_trigger()
    assert not task3.evaluate_trigger()

    task1.set_event("event1", True)
    assert task2.evaluate_trigger()
    assert not task3.evaluate_trigger()

    task1.set_event("event2", True)
    assert task2.evaluate_trigger()
    assert task3.evaluate_trigger()
