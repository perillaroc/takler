from dataclasses import dataclass
from typing import Optional
import pytest

from takler.core import Parameter


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

    return simple_flow_objects


def test_add_parameter(simple_flow_objects):
    flow1 = simple_flow_objects["flow1"]
    flow1.add_parameter("ECF_HOME", "/home/johndoe")
    flow1.add_parameter("NODES", 4)
    flow1.add_parameter("TIME_INTERVAL", 0.1)

    assert flow1.user_parameters["ECF_HOME"] == Parameter(name="ECF_HOME", value="/home/johndoe")
    assert flow1.user_parameters["NODES"] == Parameter(name="NODES", value=4)
    assert flow1.user_parameters["TIME_INTERVAL"] == Parameter(name="TIME_INTERVAL", value=0.1)

    container1 = simple_flow_objects["container1"]
    container1.add_parameter("TASKS", 32)
    assert container1.user_parameters["TASKS"] == Parameter(name="TASKS", value=32)

    task1 = simple_flow_objects["task1"]
    task1.add_parameter("FLAG", True)
    assert task1.user_parameters["FLAG"] == Parameter(name="FLAG", value=True)


def test_find_parameter(simple_flow_objects_with_parameter):
    flow1 = simple_flow_objects_with_parameter["flow1"]

    assert flow1.find_parameter("ECF_HOME") == Parameter("ECF_HOME", "/home/johndoe")
    assert flow1.find_parameter("NO_EXIST") is None

    container1 = simple_flow_objects_with_parameter["container1"]
    assert container1.find_parameter("TASKS") == Parameter("TASKS", 32)
    assert container1.find_parameter("NO_EXIST") is None
    assert container1.find_parameter("ECF_HOME") is None

    task1 = simple_flow_objects_with_parameter["task1"]
    assert task1.find_parameter("FLAG") == Parameter("FLAG", True)
    assert task1.find_parameter("NO_EXIST") is None
    assert task1.find_parameter("TASKS") is None
    assert task1.find_parameter("ECF_HOME") is None


def test_find_parent_parameter(simple_flow_objects_with_parameter):
    flow1 = simple_flow_objects_with_parameter["flow1"]

    assert flow1.find_parent_parameter("ECF_HOME") == Parameter("ECF_HOME", "/home/johndoe")
    assert flow1.find_parent_parameter("NO_EXIST") is None

    container1 = simple_flow_objects_with_parameter["container1"]
    assert container1.find_parent_parameter("TASKS") == Parameter("TASKS", 32)
    assert container1.find_parent_parameter("NO_EXIST") is None
    assert container1.find_parent_parameter("ECF_HOME") == Parameter("ECF_HOME", "/home/johndoe")

    task1 = simple_flow_objects_with_parameter["task1"]
    assert task1.find_parent_parameter("FLAG") == Parameter("FLAG", True)
    assert task1.find_parent_parameter("NO_EXIST") is None
    assert task1.find_parent_parameter("TASKS") == Parameter("TASKS", 32)
    assert task1.find_parent_parameter("ECF_HOME") == Parameter("ECF_HOME", "/home/johndoe")

