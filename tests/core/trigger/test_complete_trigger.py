from takler.core import NodeStatus


def test_complete_trigger_on_task(trigger_simple_flow):
    flow1 = trigger_simple_flow.flow1
    task1 = trigger_simple_flow.task1
    task2 = trigger_simple_flow.task2

    task1.add_event("event_a")
    task2.add_trigger("./task1 == complete")
    task2.add_complete_trigger("./task1:event_a == set")

    flow1.requeue()

    assert not task2.evaluate_trigger()
    assert not task2.evaluate_complete_trigger()

    task1.set_event("event_a", True)
    assert not task2.evaluate_trigger()
    assert task2.evaluate_complete_trigger()


def test_complete_trigger_in_run_mode(trigger_simple_flow):
    flow1 = trigger_simple_flow.flow1
    task1 = trigger_simple_flow.task1
    task2 = trigger_simple_flow.task2

    task1.add_event("event_a")
    task2.add_trigger("./task1 == complete")
    task2.add_complete_trigger("./task1:event_a == set")

    flow1.requeue()

    assert not task2.is_complete_triggered
    assert task2.state.node_status == NodeStatus.queued

    task1.set_event("event_a", True)
    flow1.resolve_dependencies()

    assert task2.is_complete_triggered
    assert task2.state.node_status == NodeStatus.complete


def test_complete_trigger_and_trigger_in_run_mode(trigger_simple_flow):
    flow1 = trigger_simple_flow.flow1
    task1 = trigger_simple_flow.task1
    task2 = trigger_simple_flow.task2

    task1.add_event("event_a")
    task2.add_trigger("./task1 == complete")
    task2.add_complete_trigger("./task1:event_a == set")

    flow1.requeue()

    assert not task2.is_complete_triggered
    assert task2.state.node_status == NodeStatus.queued

    task1.set_event("event_a", True)
    task1.complete()
    flow1.resolve_dependencies()

    assert task2.is_complete_triggered
    assert task2.state.node_status == NodeStatus.complete
