from takler.core import Limit, Task
from takler.core.limit import InLimit, InLimitManager


def test_limit():
    limit = Limit("upload_limit", 10)
    assert limit.to_dict() == dict(
        name="upload_limit",
        limit=10,
        value=0,
        node_paths=set(),
    )

    limit.increment(1, "/flow1/task1")
    assert limit.to_dict() == dict(
        name="upload_limit",
        limit=10,
        value=1,
        node_paths={"/flow1/task1",}
    )

    limit.increment(1, "/flow1/task2")
    assert limit.to_dict() == dict(
        name="upload_limit",
        limit=10,
        value=2,
        node_paths={
            "/flow1/task1",
            "/flow1/task2",
        }
    )

    limit.decrement(1, "/flow1/task1")
    assert limit.to_dict() == dict(
        name="upload_limit",
        limit=10,
        value=1,
        node_paths={
            "/flow1/task2"
        }
    )


def test_in_limit():
    limit = Limit("upload_limit", 10)
    in_limit = InLimit("upload_limit")
    in_limit.set_limit(limit)

    assert in_limit.to_dict() == dict(
        limit_name="upload_limit",
        tokens=1,
        node_path=None,
    )


def test_in_limit_manager():
    limit = Limit("upload_limit", 10)
    in_limit = InLimit("upload_limit")
    in_limit.set_limit(limit)
    limit_2 = Limit("run_limit", 5)
    in_limit_2 = InLimit("run_limit")
    in_limit_2.set_limit(limit)

    node = Task("task1")
    in_limit_manager = InLimitManager(node)
    in_limit_manager.add_in_limit(in_limit)
    assert in_limit_manager.to_dict() == dict(
        in_limit_list=[
            dict(
                limit_name="upload_limit",
                tokens=1,
                node_path=None,
            )
        ]
    )

    in_limit_manager.add_in_limit(in_limit_2)
    assert in_limit_manager.to_dict() == dict(
        in_limit_list=[
            dict(
                limit_name="upload_limit",
                tokens=1,
                node_path=None,
            ),
            dict(
                limit_name="run_limit",
                tokens=1,
                node_path=None,
            )
        ]
    )
