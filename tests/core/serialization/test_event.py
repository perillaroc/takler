from takler.core import Event


def test_event():
    event = Event("some_event")
    assert event.to_dict() == dict(
        name="some_event",
        initial_value=False,
        value=False,
    )

    event.value = True
    assert event.to_dict() == dict(
        name="some_event",
        initial_value=False,
        value=True,
    )
