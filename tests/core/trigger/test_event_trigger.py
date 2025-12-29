import pytest
from pydantic import BaseModel, ConfigDict

from takler.core import Flow, Task


class EventSimpleFlow(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    flow1: Flow
    task1: Task
    task2: Task
    task3: Task


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
    flow1 = Flow("flow1")

    with flow1.add_task("task1") as task1:
        task1.add_event("event1")
        task1.add_event("event2")

    with flow1.add_task("task2") as task2:
        task2.add_trigger("./task1:event1 == set")

    with flow1.add_task("task3") as task3:
        task3.add_trigger("./task1:event2==set")

    flow1.requeue()

    flow = EventSimpleFlow(
        flow1=flow1,
        task1=task1,
        task2=task2,
        task3=task3,
    )

    return flow


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
