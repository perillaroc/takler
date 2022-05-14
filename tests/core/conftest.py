import pytest

from takler.core import Flow


class ObjectContainer:
    pass


@pytest.fixture
def simple_flow():
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
    flow = ObjectContainer()
    flow1 = Flow("flow1")
    flow.flow1 = flow1
    container1 = flow1.add_container("container1")
    flow.container1 = container1
    task1 = container1.add_task("task1")
    flow.task1 = task1
    container2 = container1.add_container("container2")
    flow.container2 = container2
    task2 = container2.add_task("task2")
    flow.task2 = task2
    task3 = container2.add_task("task3")
    flow.task3 = task3
    task4 = flow1.add_task("task4")
    flow.task4 = task4
    container3 = flow1.add_container("container3")
    flow.container3 = container3
    task5 = container3.add_task("task5")
    flow.task5 = task5
    task6 = flow1.add_task("task6")
    flow.task6 = task6
    return flow


@pytest.fixture
def simple_flow_2():
    """
    Flow:

        |- flow2 [unknown]
          |- task1 [unknown]
          |- container1 [unknown]
            |- task2 [unknown]
          |- container2 [unknown]
            |- task3 [unknown]
            |- container3 [unknown]
              |- task4 [unknown]
              |- task5 [unknown]
            |- task6 [unknown]
          |- task7 [unknown]

    """
    result = ObjectContainer()
    with Flow("flow2") as flow2:
        result.flow2 = flow2
        with flow2.add_task("task1") as task1:
            result.task1 = task1
        with flow2.add_container("container1") as container1:
            result.container1 = container1
            with container1.add_task("task2") as task2:
                result.task2 = task2
        with flow2.add_container("container2") as container2:
            result.container2 = container2
            with container2.add_task("task3") as task3:
                result.task3 = task3
            with container2.add_container("container3") as container3:
                result.container3 = container3
                with container3.add_task("task4") as task4:
                    result.task4 = task4
                with container3.add_task("task5") as task5:
                    result.task5 = task5
            with container2.add_task("task6") as task6:
                result.task6 = task6
        with flow2.add_task("task7") as task7:
            result.task7 = task7

    return result
