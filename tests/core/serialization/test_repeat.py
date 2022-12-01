from takler.core import Repeat, RepeatDate


def test_repeat_date():
    repeat_date = RepeatDate("TAKLER_DATE", "20221101", "20221110")
    assert repeat_date.to_dict() == dict(
        name="TAKLER_DATE",
        start_date="20221101",
        end_date="20221110",
        step=1,
        value=20221101,
        class_type="RepeatDate"
    )

    repeat_date.increment()

    assert repeat_date.to_dict() == dict(
        name="TAKLER_DATE",
        start_date="20221101",
        end_date="20221110",
        step=1,
        value=20221102,
        class_type="RepeatDate"
    )


def test_repeat():
    repeat_date = RepeatDate("TAKLER_DATE", "20221101", "20221110")
    repeat = Repeat(repeat_date)

    assert repeat.to_dict() == dict(
        r=dict(
            name="TAKLER_DATE",
            start_date="20221101",
            end_date="20221110",
            step=1,
            value=20221101,
            class_type="RepeatDate"
        )
    )

