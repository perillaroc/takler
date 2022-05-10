from takler.core import Event


def test_create_event(simple_flow_objects):
    task1 = simple_flow_objects["task1"]
    event = task1.add_event("arrived")
    assert task1.events == [Event("arrived")]
    assert not event.initial_value
    assert not event.value


def test_set_event(simple_flow_objects):
    task1 = simple_flow_objects["task1"]
    event1 = task1.add_event("event1")
    event2 = task1.add_event("event2")

    assert task1.set_event("event1", True)
    assert event1.value
    assert task1.set_event("event1", False)
    assert not event1.value

    assert task1.set_event("event2", True)
    assert event2.value
    assert task1.set_event("event2", False)
    assert not event2.value

    assert not task1.set_event("not_exist_event", True)


def test_reset_event(simple_flow_objects):
    task1 = simple_flow_objects["task1"]
    event1 = task1.add_event("event1")
    event2 = task1.add_event("event2", True)

    assert task1.set_event("event1", True)
    assert event1.value
    assert task1.reset_event("event1")
    assert not event1.value

    assert task1.set_event("event2", False)
    assert not event2.value
    assert task1.reset_event("event2")
    assert event2.value


