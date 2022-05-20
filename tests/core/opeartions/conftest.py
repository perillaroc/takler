import pytest

from takler.core import Flow


class ObjectContainer:
    pass


@pytest.fixture
def simple_flow_1():
    """
    Flow:

        |- flow1 [unknown]
          |- task1 [unknown]
          |- container1 [unknown]
            |- task2 [unknown]
            |- container2 [unknown]
              |- task3 [unknown]
              |- task4 [unknown]
            |- container3 [unknown]
              |- task5 [unknown]
              |- task6 [unknown]
          |- task7 [unknown]
          |- container4 [unknown]
            |- task8 [unknown]
            |- task9 [unknown]
          |- task10 [unknown]

    """
    oc = ObjectContainer()
    with Flow("flow1") as flow1:
        oc.flow1 = flow1
        with flow1.add_task("task1") as task1:
            oc.task1 = task1
        with flow1.add_container("container1") as container1:
            oc.container1 = container1
            with container1.add_task("task2") as task2:
                oc.task2 = task2
            with container1.add_container("container2") as container2:
                oc.container2 = container2
                with container1.add_task("task3") as task3:
                    oc.task3 = task3
                with container2.add_task("task4") as task4:
                    oc.task4 = task4
            with container1.add_container("container3") as container3:
                oc.container3 = container3
                with container3.add_task("task5") as task5:
                    oc.task5 = task5
                with container3.add_task("task6") as task6:
                    oc.task6 = task6
        with flow1.add_task("task7") as task7:
            oc.task7 = task7
        with flow1.add_container("container4") as container4:
            oc.container4 = container4
            with container4.add_task("task8") as task8:
                oc.task8 = task8
            with container4.add_task("task9") as task9:
                oc.task9 = task9
        with flow1.add_task("task10") as task10:
            oc.task10 = task10

    return oc
