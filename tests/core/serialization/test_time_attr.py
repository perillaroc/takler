import datetime

from takler.core import TimeAttribute


def test_time_attr():
    time_attr = TimeAttribute("10:00")
    assert time_attr.to_dict() == dict(
        time="10:00",
        free=False,
    )

    time_attr.set_free()
    assert time_attr.to_dict() == dict(
        time="10:00",
        free=True
    )

    time_attr = TimeAttribute(datetime.time(11, 10))
    assert time_attr.to_dict() == dict(
        time="11:10",
        free=False,
    )
