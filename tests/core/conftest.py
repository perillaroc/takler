import pytest

from takler.core import Flow


@pytest.fixture
def simple_flow_objects():
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


@pytest.fixture
def simple_flow_2_objects():
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
    with Flow("flow2") as flow2:
        with flow2.add_task("task1") as task1:
            pass
        with flow2.add_container("container1") as container1:
            with container1.add_task("task2") as task2:
                pass
        with flow2.add_container("container2") as container2:
            with container2.add_task("task3") as task3:
                pass
            with container2.add_container("container3") as container3:
                with container3.add_task("task4") as task4:
                    pass
                with container3.add_task("task5") as task5:
                    pass
            with container2.add_task("task6") as task6:
                pass
        with flow2.add_task("task7") as task7:
            pass

    return dict(
        flow2=flow2,
        container1=container1,
        container2=container2,
        container3=container3,
        task1=task1,
        task2=task2,
        task3=task3,
        task4=task4,
        task5=task5,
        task6=task6,
        task7=task7,
    )
