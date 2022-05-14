

def test_add_trigger(simple_flow):
    flow1 = simple_flow.flow1
    flow1.requeue()

    task2 = simple_flow.task2
    task2.add_trigger("../task1 == complete")
    assert not task2.evaluate_trigger()

    task3 = simple_flow.task3
    task3.add_trigger("./task2 == complete")
    assert not task3.evaluate_trigger()

    task4 = simple_flow.task4
    task4.add_trigger("/flow1/container1 == complete")
    assert not task4.evaluate_trigger()

    container3 = simple_flow.container3
    container3.add_trigger("./task4 == complete")
    assert not container3.evaluate_trigger()

    task6 = simple_flow.task6
    task6.add_trigger("/flow1/container3/task5 == complete")
    assert not task6.evaluate_trigger()
