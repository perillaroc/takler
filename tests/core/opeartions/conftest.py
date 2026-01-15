import pytest
from pydantic import BaseModel, ConfigDict

from takler.core import Flow, NodeContainer, Task


class SimpleFlow(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    flow1: Flow
    task1: Task
    container1: NodeContainer
    task2: Task
    container2: NodeContainer
    task3: Task
    task4: Task
    container3: NodeContainer
    task5: Task
    task6: Task
    task7: Task
    container4: NodeContainer
    task8: Task
    task9: Task
    task10: Task


@pytest.fixture
def simple_flow_for_operation() -> SimpleFlow:
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
    with Flow("flow1") as flow1:
        with flow1.add_task("task1") as task1:
            pass
        with flow1.add_container("container1") as container1:
            with container1.add_task("task2") as task2:
                pass
            with container1.add_container("container2") as container2:
                with container2.add_task("task3") as task3:
                    pass
                with container2.add_task("task4") as task4:
                    pass
            with container1.add_container("container3") as container3:
                with container3.add_task("task5") as task5:
                    pass
                with container3.add_task("task6") as task6:
                    pass
        with flow1.add_task("task7") as task7:
            pass
        with flow1.add_container("container4") as container4:
            with container4.add_task("task8") as task8:
                pass
            with container4.add_task("task9") as task9:
                pass
        with flow1.add_task("task10") as task10:
            pass

    flow = SimpleFlow(
        flow1=flow1,
        task1=task1,
        container1=container1,
        task2=task2,
        container2=container2,
        task3=task3,
        task4=task4,
        container3=container3,
        task5=task5,
        task6=task6,
        task7=task7,
        container4=container4,
        task8=task8,
        task9=task9,
        task10=task10,
    )

    return flow
