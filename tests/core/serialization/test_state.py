from takler.core.state import State, NodeStatus


def test_state_to_dict():
    state = State(NodeStatus.complete)
    assert state.to_dict() == dict(
        status=2,
        suspended=False,
    )
