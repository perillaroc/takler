from takler.core import NodeStatus


def test_requeue_on_flow(simple_flow_for_operation):
    flow1 = simple_flow_for_operation.flow1
    flow1.requeue()

    for name, node in vars(simple_flow_for_operation).items():
        print(vars(simple_flow_for_operation))
        assert node.state.node_status == NodeStatus.queued


def test_requeue_on_container(simple_flow_for_operation):
    flow1 = simple_flow_for_operation.flow1
    flow1.requeue()

    """
    |- flow1 [queued]
      |- task1 [queued]
      |- container1 [aborted]
        |- task2 [complete]
        |- container2 [active]
          |- task3 [complete]
          |- task4 [active]
        |- container3 [aborted]
          |- task5 [queued]
          |- task6 [aborted]
      |- task7 [queued]
      |- container4 [queued]
        |- task8 [queued]
        |- task9 [queued]
      |- task10 [queued]
    """

    container1 = simple_flow_for_operation.container1
    task2 = simple_flow_for_operation.task2
    container2 = simple_flow_for_operation.container2
    task3 = simple_flow_for_operation.task3
    task4 = simple_flow_for_operation.task4
    container3 = simple_flow_for_operation.container3
    task5 = simple_flow_for_operation.task5
    task6 = simple_flow_for_operation.task6

    task2.set_node_status(NodeStatus.complete)
    task3.set_node_status(NodeStatus.complete)
    task4.set_node_status(NodeStatus.active)
    task5.set_node_status(NodeStatus.queued)
    task6.set_node_status(NodeStatus.aborted)

    assert container1.state.node_status == NodeStatus.aborted
    assert task2.state.node_status == NodeStatus.complete
    assert container2.state.node_status == NodeStatus.active
    assert task3.state.node_status == NodeStatus.complete
    assert task4.state.node_status == NodeStatus.active
    assert container3.state.node_status == NodeStatus.aborted
    assert task5.state.node_status == NodeStatus.queued
    assert task6.state.node_status == NodeStatus.aborted

    container3.requeue()
    container3.handle_status_change()

    assert container1.state.node_status == NodeStatus.active
    assert task2.state.node_status == NodeStatus.complete
    assert container2.state.node_status == NodeStatus.active
    assert task3.state.node_status == NodeStatus.complete
    assert task4.state.node_status == NodeStatus.active
    assert container3.state.node_status == NodeStatus.queued
    assert task5.state.node_status == NodeStatus.queued
    assert task6.state.node_status == NodeStatus.queued
