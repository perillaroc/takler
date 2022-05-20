from takler.core import NodeContainer, Task


def test_suspend(simple_flow_1):
    flow1 = simple_flow_1.flow1
    flow1.requeue()

    container1: NodeContainer = simple_flow_1.container1
    assert not container1.state.suspended

    container1.suspend()
    assert container1.state.suspended
    assert not container1.resolve_dependencies()

    container1.resume()
    assert not container1.state.suspended
    assert container1.resolve_dependencies()

