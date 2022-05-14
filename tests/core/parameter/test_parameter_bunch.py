import pytest

from takler.core import Parameter, parameter, Bunch


@pytest.fixture
def simple_bunch_default_port(simple_flow):
    flow1 = simple_flow.flow1
    flow1.add_parameter("ECF_HOME", "/home/johndoe")
    flow1.add_parameter("NODES", 4)
    flow1.add_parameter("TIME_INTERVAL", 0.1)

    container1 = simple_flow.container1
    container1.add_parameter("TASKS", 32)

    task1 = simple_flow.task1
    task1.add_parameter("FLAG", True)

    bunch = Bunch("nwpc_op")
    bunch.add_flow(flow1)

    simple_flow.bunch = bunch

    return simple_flow


def test_bunch_generated_parameter(simple_bunch_default_port):
    bunch = simple_bunch_default_port.bunch
    assert bunch.find_generated_parameter(parameter.TAKLER_HOST) == \
           Parameter(parameter.TAKLER_HOST, "localhost")
    assert bunch.find_generated_parameter(parameter.TAKLER_PORT) == \
           Parameter(parameter.TAKLER_PORT, "33083")
    assert bunch.find_parent_parameter(parameter.TAKLER_HOME) == \
           Parameter(parameter.TAKLER_HOME, ".")

    assert bunch.find_parent_parameter("NOT_EXIST") is None


def test_task_find_bunch_parameter(simple_bunch_default_port):
    task1 = simple_bunch_default_port.task1
    assert task1.find_parent_parameter(parameter.TAKLER_PORT) == Parameter(parameter.TAKLER_PORT, "33083")
    assert task1.find_parameter(parameter.TAKLER_PORT) is None


def test_container_find_bunch_parameter(simple_bunch_default_port):
    container1 = simple_bunch_default_port.container1
    assert container1.find_parent_parameter(parameter.TAKLER_HOME) == Parameter(parameter.TAKLER_HOME, ".")
    assert container1.find_parameter(parameter.TAKLER_HOME) is None


def test_flow_find_bunch_parameter(simple_bunch_default_port):
    flow1 = simple_bunch_default_port.flow1
    assert flow1.find_parent_parameter(parameter.TAKLER_HOME) == Parameter(parameter.TAKLER_HOME, ".")
    assert flow1.find_parameter(parameter.TAKLER_HOME) is None
