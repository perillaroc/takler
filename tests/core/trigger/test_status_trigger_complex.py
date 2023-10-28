import pytest

from takler.core import Flow

class ObjectContainer:
    pass


@pytest.fixture
def complex_flow_case_1():
    result = ObjectContainer()
    with Flow("flow1") as flow1:
        result.flow1 = flow1
        with flow1.add_task("task1") as task1:
            result.task1 = task1
        with flow1.add_task("task2") as task2:
            result.task2 = task2
        with flow1.add_task("task3") as task3:
            result.task3 = task3
        with flow1.add_task("task4") as task4:
            result.task4 = task4
        with flow1.add_task("task5") as task5:
            result.task5 = task5
        with flow1.add_task("task6") as task6:
            result.task6 = task6
        with flow1.add_task("task7") as task7:
            result.task7 = task7
        with flow1.add_task("task8") as task8:
            result.task8 = task8
        with flow1.add_task("task9") as task9:
            result.task9 = task9
        with flow1.add_task("task10") as task10:
            result.task10 = task10
    return result


def test_add_trigger(complex_flow_case_1):
    flow1 = complex_flow_case_1.flow1
    flow1.requeue()

    task10 = complex_flow_case_1.task10
    task10.add_trigger("((./task1 == complete) or (./task2 == complete)) "
                       "and ((./task3 == complete) or (./task4 == complete))")
    assert not task10.evaluate_trigger()
