import pytest

from takler.core import Meter


def test_create_meter(simple_flow_objects):
    task1 = simple_flow_objects["task1"]
    meter = task1.add_meter("forecast_hour", 0, 240)
    assert task1.meters == [Meter("forecast_hour", 0, 240)]
    assert meter.min_value == 0
    assert meter.max_value == 240
    assert meter.value == 0


def test_set_meter(simple_flow_objects):
    task1 = simple_flow_objects["task1"]
    meter1 = task1.add_meter("meter1", 0, 24)
    meter2 = task1.add_meter("meter2", 10, 100)

    assert task1.set_meter("meter1", 0)
    assert meter1.value == 0
    assert task1.set_meter("meter1", 10)
    assert meter1.value == 10
    assert task1.set_meter("meter1", 24)
    assert meter1.value == 24
    with pytest.raises(ValueError):
        task1.set_meter("meter1", 50)

    assert task1.set_meter("meter2", 10)
    assert meter2.value == 10
    assert task1.set_meter("meter2", 50)
    assert meter2.value == 50
    assert task1.set_meter("meter2", 100)
    assert meter2.value == 100

    assert not task1.set_meter("not_exist_meter", 10)


def test_reset_event(simple_flow_objects):
    task1 = simple_flow_objects["task1"]
    meter1 = task1.add_meter("meter1", 0, 24)
    meter2 = task1.add_meter("meter2", 10, 100)

    assert task1.set_meter("meter1", 10)
    assert meter1.value == 10
    assert task1.reset_meter("meter1")
    assert meter1.value == 0

    assert task1.set_meter("meter2", 50)
    assert meter2.value == 50
    assert task1.reset_meter("meter2")
    assert meter2.value == 10


