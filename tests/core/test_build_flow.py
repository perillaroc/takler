from takler.core import Flow
from takler.visitor import pre_order_travel, SimplePrintVisitor


def test_build_flow():
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

    print()
    pre_order_travel(flow1, SimplePrintVisitor())


def test_build_flow_using_with():
    with Flow("flow1") as flow1:
        with flow1.add_container("container1") as container1:
            with container1.add_task("task1") as task1:
                pass
            with container1.add_container("container2") as container2:
                with container2.add_task("task2") as task2:
                    pass
                with container2.add_task("task3") as task3:
                    pass
            with flow1.add_task("task4") as task4:
                pass
        with flow1.add_container("container3") as container3:
            with container3.add_task("task5") as task5:
                pass
        with flow1.add_task("task6") as task6:
            pass

        print()
        pre_order_travel(flow1, SimplePrintVisitor())
