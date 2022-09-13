import datetime

import pytest

from takler.core import Flow, Task


class ObjectContainer:
    pass


@pytest.fixture
def one_task_time_flow() -> ObjectContainer:
    """
    |- flow1
        |- task1
            time 12:00
    """
    oc = ObjectContainer()
    with Flow("flow1") as flow:
        oc.flow = flow
        with flow.add_task("task1") as task1:
            task1.add_time(datetime.time(12, 0))
            oc.task1 = task1

    return oc


TEST_TIME = datetime.datetime(2022, 9, 12, 10, 0, 0)


@pytest.fixture
def patch_datetime_now(monkeypatch):
    """
    set ``datetime.datetime.now`` to a fixed time, 2022-09-12 10:00:01
    """
    class TestDateTime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return TEST_TIME

    monkeypatch.setattr(datetime, "datetime", TestDateTime)


def test_time_attr_catch_time_point(one_task_time_flow, patch_datetime_now):
    flow: Flow = one_task_time_flow.flow
    task1: Task = one_task_time_flow.task1

    start_time = datetime.datetime(2022, 9, 12, 10, 0, 0)
    flow.calendar.begin(start_time)
    # flow.calendar.flow_time = start_time
    # flow.calendar.last_real_time = start_time

    flow.update_calendar(datetime.datetime(2022, 9, 12, 11, 0, 0))
    assert not task1.times[0].free
    assert not task1.resolve_time_dependencies()

    flow.update_calendar(datetime.datetime(2022, 9, 12, 12, 0, 0))
    assert task1.times[0].free
    assert task1.resolve_time_dependencies()

    flow.update_calendar(datetime.datetime(2022, 9, 12, 12, 1, 10))
    assert task1.times[0].free

    assert task1.resolve_time_dependencies()


def test_time_attr_miss_time_point(one_task_time_flow, patch_datetime_now):
    flow: Flow = one_task_time_flow.flow
    task1: Task = one_task_time_flow.task1

    start_time = datetime.datetime(2022, 9, 12, 10, 0, 0)
    flow.calendar.begin(start_time)
    # flow.calendar.flow_time = start_time
    # flow.calendar.last_real_time = start_time

    flow.update_calendar(datetime.datetime(2022, 9, 12, 11, 59, 0))
    assert not task1.times[0].free
    assert not task1.resolve_time_dependencies()

    flow.update_calendar(datetime.datetime(2022, 9, 12, 12, 1, 0))
    assert not task1.times[0].free
    assert not task1.resolve_time_dependencies()

    flow.update_calendar(datetime.datetime(2022, 9, 12, 13, 0, 10))
    assert not task1.times[0].free
    assert not task1.resolve_time_dependencies()


def test_time_attr_requeue(one_task_time_flow, patch_datetime_now):
    flow: Flow = one_task_time_flow.flow
    task1: Task = one_task_time_flow.task1

    start_time = datetime.datetime(2022, 9, 12, 10, 0, 0)
    flow.calendar.begin(start_time)
    # flow.calendar.flow_time = start_time
    # flow.calendar.last_real_time = start_time

    flow.update_calendar(datetime.datetime(2022, 9, 12, 11, 59, 0))
    assert not task1.times[0].free
    assert not task1.resolve_time_dependencies()

    flow.update_calendar(datetime.datetime(2022, 9, 12, 12, 0, 0))
    assert task1.times[0].free
    assert task1.resolve_time_dependencies()

    flow.update_calendar(datetime.datetime(2022, 9, 12, 13, 0, 10))
    assert task1.times[0].free
    assert task1.resolve_time_dependencies()

    # SECTION: requeue
    flow.requeue()
    assert not task1.times[0].free
    assert not task1.resolve_time_dependencies()

    flow.update_calendar(datetime.datetime(2022, 9, 12, 12, 0, 0))
    assert task1.times[0].free
    assert task1.resolve_time_dependencies()


def test_time_attr_free_dependencies(one_task_time_flow, patch_datetime_now):
    flow: Flow = one_task_time_flow.flow
    task1: Task = one_task_time_flow.task1

    start_time = datetime.datetime(2022, 9, 12, 10, 0, 0)
    flow.calendar.begin(start_time)
    # flow.calendar.flow_time = start_time
    # flow.calendar.last_real_time = start_time

    flow.update_calendar(datetime.datetime(2022, 9, 12, 11, 50, 0))
    assert not task1.times[0].free
    assert not task1.resolve_time_dependencies()

    task1.free_dependencies(dep_type="time")
    assert task1.times[0].free
    assert task1.resolve_time_dependencies()
