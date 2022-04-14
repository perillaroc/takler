

def test_add_trigger(simple_flow_objects):
    flow1 = simple_flow_objects["flow1"]
    flow1.requeue()

    task2 = simple_flow_objects["task2"]
    task2.add_trigger("../task1 == complete")
    assert not task2.evaluate_trigger()

    task3 = simple_flow_objects["task3"]
    task3.add_trigger("./task2 == complete")
    assert not task3.evaluate_trigger()

    task4 = simple_flow_objects["task4"]
    task4.add_trigger("/flow1/container1 == complete")
    assert not task4.evaluate_trigger()

    container3 = simple_flow_objects["container3"]
    container3.add_trigger("./task4 == complete")
    assert not container3.evaluate_trigger()

    task6 = simple_flow_objects["task6"]
    task6.add_trigger("/flow1/container3/task5 == complete")
    assert not task6.evaluate_trigger()
