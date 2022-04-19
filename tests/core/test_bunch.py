from takler.core import Bunch


def test_add_flow(simple_flow_objects, simple_flow_2_objects):
    bunch = Bunch()
    flow1 = simple_flow_objects["flow1"]
    bunch.add_flow(flow1)
    assert bunch.flows == {
        "flow1": flow1
    }

    flow2 = simple_flow_2_objects["flow2"]
    bunch.add_flow(flow2)
    assert bunch.flows == {
        "flow1": flow1,
        "flow2": flow2,
    }

    f = bunch.find_flow("flow1")
    assert f == flow1

    flow1_task3 = simple_flow_objects["task3"]
    node = bunch.find_node("/flow1/container1/container2/task3")
    assert node == flow1_task3

    f = bunch.delete_flow("flow1")
    assert f == flow1
    assert bunch.flows == {
        "flow2": flow2
    }
