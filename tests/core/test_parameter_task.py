import pytest

from takler.core import Parameter, parameter


@pytest.fixture
def simple_flow_objects_with_parameter(simple_flow_objects):
    flow1 = simple_flow_objects["flow1"]
    flow1.add_parameter("ECF_HOME", "/home/johndoe")
    flow1.add_parameter("NODES", 4)
    flow1.add_parameter("TIME_INTERVAL", 0.1)

    container1 = simple_flow_objects["container1"]
    container1.add_parameter("TASKS", 32)

    task1 = simple_flow_objects["task1"]
    task1.add_parameter("FLAG", True)

    task1.init(task_id="1001")

    return simple_flow_objects


def test_update_generated_parameter(simple_flow_objects_with_parameter):
    task1 = simple_flow_objects_with_parameter["task1"]
    task1.update_generated_parameters()

    assert task1.find_generated_parameter(parameter.TASK) == \
           Parameter(parameter.TASK, "task1")
    assert task1.find_generated_parameter(parameter.TAKLER_NAME) == \
           Parameter(parameter.TAKLER_NAME, "/flow1/container1/task1")
    assert task1.find_generated_parameter(parameter.TAKLER_RID) == \
           Parameter(parameter.TAKLER_RID, "1001")
