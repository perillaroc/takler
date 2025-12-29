import pytest
from pydantic import BaseModel, ConfigDict

from takler.core import Flow, Task


class CompleteFlow(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    flow1: Flow
    task1: Task
    task2: Task
    task3: Task
    task4: Task
    task5: Task
    task6: Task
    task7: Task
    task8: Task
    task9: Task
    task10: Task


@pytest.fixture
def complex_flow() -> CompleteFlow:
    with Flow("flow1") as flow1:
        with flow1.add_task("task1") as task1:
            pass
        with flow1.add_task("task2") as task2:
            pass
        with flow1.add_task("task3") as task3:
            pass
        with flow1.add_task("task4") as task4:
            pass
        with flow1.add_task("task5") as task5:
            pass
        with flow1.add_task("task6") as task6:
            pass
        with flow1.add_task("task7") as task7:
            pass
        with flow1.add_task("task8") as task8:
            pass
        with flow1.add_task("task9") as task9:
            pass
        with flow1.add_task("task10") as task10:
            pass

    complete_flow = CompleteFlow(
        flow1=flow1,
        task1=task1,
        task2=task2,
        task3=task3,
        task4=task4,
        task5=task5,
        task6=task6,
        task7=task7,
        task8=task8,
        task9=task9,
        task10=task10,
    )
    return complete_flow


def test_add_trigger(complex_flow):
    flow1 = complex_flow.flow1
    task1 = complex_flow.task1
    task2 = complex_flow.task2
    task3 = complex_flow.task3
    task4 = complex_flow.task4
    task10 = complex_flow.task10

    flow1.requeue()
    task10.add_trigger(
        "((./task1 == complete) or (./task2 == complete)) "
        "and ((./task3 == complete) or (./task4 == complete))"
    )
    assert not task10.evaluate_trigger()

    flow1.requeue()
    task1.complete()
    assert not task10.evaluate_trigger()

    task3.complete()
    assert task10.evaluate_trigger()

    flow1.requeue()
    task1.complete()
    task2.complete()
    assert not task10.evaluate_trigger()

    flow1.requeue()
    task3.complete()
    task4.complete()
    assert not task10.evaluate_trigger()

    flow1.requeue()
    task1.abort("trap")
    task2.complete()
    task3.complete()
    assert task10.evaluate_trigger()

