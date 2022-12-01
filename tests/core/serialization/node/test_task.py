import pprint

import pytest

from takler.core import Flow, RepeatDate


class ObjectContainer:
    pass


@pytest.fixture
def task_case():
    """
    A simple flow with only three tasks.

    |- flow1
        |- task1
            event: event1
            event: event2
        |- task2
            trigger task1:event1 == set
        |- task3
            trigger task1:event2 == set
    """
    result = ObjectContainer()

    flow1 = Flow("flow1")
    result.flow1 = flow1

    with flow1.add_task("task1") as task1:
        result.task1 = task1
        task1.add_event("event1")
        task1.add_event("event2")

    with flow1.add_task("task2") as task2:
        result.task2 = task2
        task2.add_parameter("param1", "one")
        task2.add_trigger("./task1:event1 == set")
        task2.add_event("event1")
        task2.add_meter("meter1", 0, 10)
        task2.add_limit("limit1", 10)
        task2.add_in_limit("limit1")
        task2.add_repeat(RepeatDate("TAKLER_DATE", 20221201, 20221202))
        task2.add_time("12:00")

    with flow1.add_task("task3") as task3:
        result.task3 = task3
        task3.add_trigger("./task1:event2==set")

    flow1.requeue()

    return result


def test_node(task_case):
    task2 = task_case.task2
    assert task2.to_dict() == dict(
        name="task2",
        state=dict(
            status=3,
            suspended=False,
        ),
        user_parameters=[
            dict(name="param1", value="one"),
        ],
        trigger="./task1:event1 == set",
        events=[
            dict(name="event1", initial_value=False, value=False),
        ],
        meters=[
            dict(name="meter1", min_value=0, max_value=10, value=0)
        ],
        limits=[
            dict(name="limit1", limit=10, node_paths=list(), value=0)
        ],
        in_limit_manager=dict(
            in_limit_list=[
                dict(limit_name="limit1", tokens=1, node_path=None)
            ]
        ),
        repeat=dict(
            r=dict(
                name="TAKLER_DATE",
                start_date="20221201",
                end_date="20221202",
                step=1,
                value=20221201,
                class_type="RepeatDate",
            )
        ),
        times=[
            dict(time="12:00", free=False),
        ],

        # task
        task_id=None,
        aborted_reason=None,
        try_no=0,
    )
