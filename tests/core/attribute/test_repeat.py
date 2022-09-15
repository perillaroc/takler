from datetime import date
from takler.core import Repeat, RepeatDate, Flow, NodeStatus, Parameter

import pytest


# RepeatDate

@pytest.fixture
def start_date_int():
    return 20220601


@pytest.fixture
def end_date_int():
    return 20220607


def test_repeat_date_create(start_date_int, end_date_int):
    r = RepeatDate("TAKLER_DATE", start_date_int, end_date_int)
    assert r.start == 20220601
    assert r.end == 20220607
    assert r.step == 1
    assert r.value == 20220601


def test_repeat_date_increment(start_date_int, end_date_int):
    # step = 1
    r = RepeatDate("TAKLER_DATE", start_date_int, end_date_int)
    assert r.increment()
    assert r.value == 20220602
    assert r.increment()
    assert r.value == 20220603
    assert r.increment()
    assert r.value == 20220604
    assert r.increment()
    assert r.value == 20220605
    assert r.increment()
    assert r.value == 20220606
    assert r.increment()
    assert r.value == 20220607

    assert not r.increment()
    assert r.value == 20220607

    # step = 2
    r = RepeatDate("TAKLER_DATE", start_date_int, end_date_int, 2)
    assert r.increment()
    assert r.value == 20220603
    assert r.increment()
    assert r.value == 20220605
    assert r.increment()
    assert r.value == 20220607

    assert not r.increment()
    assert r.value == 20220607


def test_repeat_date_reset(start_date_int, end_date_int):
    r = RepeatDate("TAKLER_DATE", start_date_int, end_date_int)
    assert r.increment()
    assert r.increment()
    assert r.increment()
    assert r.value == 20220604

    r.reset()
    assert r.value == 20220601


def test_repeat_date_change(start_date_int, end_date_int):
    r = RepeatDate("TAKLER_DATE", start_date_int, end_date_int)
    r.change(20220602)
    assert r.value == 20220602

    r.change("20220603")
    assert r.value == 20220603

    r.change(date(2022, 6, 4))
    assert r.value == 20220604

    with pytest.raises(ValueError):
        r.change(date(2022, 6, 8))

    r = RepeatDate("TAKLER_DATE", start_date_int, end_date_int, 2)
    r.change(20220603)
    assert r.value == 20220603

    r.change("20220605")
    assert r.value == 20220605

    r.change(date(2022, 6, 7))
    assert r.value == 20220607

    with pytest.raises(ValueError):
        r.change(date(2022, 5, 8))

    with pytest.raises(ValueError):
        r.change(date(2022, 6, 8))

    with pytest.raises(ValueError):
        r.change(date(2022, 6, 2))


def test_repeat_date_generated_params(start_date_int, end_date_int):
    r = RepeatDate("TAKLER_DATE", start_date_int, end_date_int)
    assert r.generated_parameters() == {
        "TAKLER_DATE": Parameter("TAKLER_DATE", 20220601)
    }

    r.increment()
    assert r.generated_parameters() == {
        "TAKLER_DATE": Parameter("TAKLER_DATE", 20220602)
    }


def test_repeat_date_create_in_flow(start_date_int, end_date_int):
    flow1 = Flow("flow1")
    task1 = flow1.add_task("task1")
    task1.add_repeat(RepeatDate("YMD", start_date_int, end_date_int))


def test_repeat_date_run_in_flow(start_date_int, end_date_int):
    # create flow
    flow1 = Flow("flow1")
    task1 = flow1.add_task("task1")
    task1.add_repeat(RepeatDate("YMD", start_date_int, end_date_int))

    # requeue
    task1.requeue()

    # run 1
    task1.resolve_dependencies()
    assert task1.find_generated_parameter("YMD").value == 20220601

    # run 2
    task1.complete()
    task1.resolve_dependencies()
    assert task1.find_generated_parameter("YMD").value == 20220602

    # run 3
    task1.complete()
    task1.resolve_dependencies()
    assert task1.find_generated_parameter("YMD").value == 20220603

    # run 4
    task1.complete()
    task1.resolve_dependencies()
    assert task1.find_generated_parameter("YMD").value == 20220604

    # run 5
    task1.complete()
    task1.resolve_dependencies()
    assert task1.find_generated_parameter("YMD").value == 20220605

    # run 6
    task1.complete()
    task1.resolve_dependencies()
    assert task1.find_generated_parameter("YMD").value == 20220606

    # run 7
    task1.complete()
    task1.resolve_dependencies()
    assert task1.find_generated_parameter("YMD").value == 20220607

    # full complete
    task1.complete()
    task1.resolve_dependencies()

    assert task1.state.node_status == NodeStatus.complete
    assert task1.find_generated_parameter("YMD").value == 20220607
