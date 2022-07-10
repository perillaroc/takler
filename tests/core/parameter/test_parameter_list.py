import pytest

from takler.core import Parameter, Bunch


@pytest.fixture
def simple_bunch(simple_flow, simple_flow_2):
    bunch = Bunch("nwpc_op")
    bunch.add_parameter("TAKLER_HOME", "/home/johndoe/takler_out")

    # flow1
    with simple_flow.flow1 as flow1:
        bunch.add_flow(flow1)
        flow1.add_parameter("TAKLER_HOME", "/home/johndoe/bunch/flow1")
        flow1.add_parameter("HH", "00")
        flow1.add_parameter("FORECAST_INTERVAL", 3)
        flow1.add_parameter("FORECAST_LENGTH", 240)

    with simple_flow.container1 as container1:
        container1.add_parameter("CLASS", "serial_op")

    with simple_flow.task1 as task1:
        task1.add_parameter("UPLOAD_GRIB2", True)
        task1.add_parameter("FORECAST_LENGTH", 120)

    with simple_flow.task3 as task3:
        task3.add_parameter("FORECAST_LENGTH", 24)
        task3.add_parameter("TASKS", 64)

    # flow2
    with simple_flow_2.flow2 as flow2:
        flow2.add_parameter("TAKLER_HOME", "/home/johndoe/bunch/flow2")
        bunch.add_flow(flow2)

    return bunch


def test_get_flow1_task1_parameters(simple_bunch, simple_flow):
    task1 = simple_flow.task1
    task1.update_generated_parameters()
    params = task1.parameters()
    params_keys = params.keys()
    assert list(params_keys) == [
        # task1
        "UPLOAD_GRIB2",
        "FORECAST_LENGTH",
        "TASK",
        "TAKLER_NAME",
        "TAKLER_RID",
        "TAKLER_TRY_NO",

        # container1
        "CLASS",

        # flow1
        "TAKLER_HOME",
        "HH",
        "FORECAST_INTERVAL",

        # bunch
        "TAKLER_HOST",
        "TAKLER_PORT",
    ]

    # task1
    assert params["UPLOAD_GRIB2"] == Parameter("UPLOAD_GRIB2", True)
    assert params["FORECAST_LENGTH"] == Parameter("FORECAST_LENGTH", 120)
    assert params["TASK"] == Parameter("TASK", "task1")
    assert params["TAKLER_NAME"] == Parameter("TAKLER_NAME", "/flow1/container1/task1")
    assert params["TAKLER_RID"] == Parameter("TAKLER_RID", None)
    assert params["TAKLER_TRY_NO"] == Parameter("TAKLER_TRY_NO", 0)

    # container1
    assert params["CLASS"] == Parameter("CLASS", "serial_op")

    # flow1
    assert params["TAKLER_HOME"] == Parameter("TAKLER_HOME", "/home/johndoe/bunch/flow1")
    assert params["HH"] == Parameter("HH", "00")
    assert params["FORECAST_INTERVAL"] == Parameter("FORECAST_INTERVAL", 3)

    # bunch
    assert params["TAKLER_HOST"] == Parameter("TAKLER_HOST", "localhost")
    assert params["TAKLER_PORT"] == Parameter("TAKLER_PORT", "33083")


def test_get_flow1_task3_parameters(simple_bunch, simple_flow):
    task3 = simple_flow.task3
    task3.update_generated_parameters()
    params = task3.parameters()
    params_keys = params.keys()
    assert list(params_keys) == [
        # task1
        "FORECAST_LENGTH",
        "TASKS",
        "TASK",
        "TAKLER_NAME",
        "TAKLER_RID",
        "TAKLER_TRY_NO",

        # container1
        "CLASS",

        # flow1
        "TAKLER_HOME",
        "HH",
        "FORECAST_INTERVAL",

        # bunch
        "TAKLER_HOST",
        "TAKLER_PORT",
    ]

    # task1
    assert params["FORECAST_LENGTH"] == Parameter("FORECAST_LENGTH", 24)
    assert params["TASKS"] == Parameter("TASKS", 64)
    assert params["TASK"] == Parameter("TASK", "task3")
    assert params["TAKLER_NAME"] == Parameter("TAKLER_NAME", "/flow1/container1/container2/task3")
    assert params["TAKLER_RID"] == Parameter("TAKLER_RID", None)
    assert params["TAKLER_TRY_NO"] == Parameter("TAKLER_TRY_NO", 0)

    # container1
    assert params["CLASS"] == Parameter("CLASS", "serial_op")

    # flow1
    assert params["TAKLER_HOME"] == Parameter("TAKLER_HOME", "/home/johndoe/bunch/flow1")
    assert params["HH"] == Parameter("HH", "00")
    assert params["FORECAST_INTERVAL"] == Parameter("FORECAST_INTERVAL", 3)

    # bunch
    assert params["TAKLER_HOST"] == Parameter("TAKLER_HOST", "localhost")
    assert params["TAKLER_PORT"] == Parameter("TAKLER_PORT", "33083")