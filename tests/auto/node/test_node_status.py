# coding: utf-8
from takler.node.node_state import NodeState


class TestNodeState(object):
    def test_create(self):
        state = NodeState.unknown

    def test_string_to_state(self):
        assert NodeState['unknown'] == NodeState.unknown
        assert NodeState['complete'] == NodeState.complete
        assert NodeState['queued'] == NodeState.queued
        assert NodeState['submitted'] == NodeState.submitted
        assert NodeState['active'] == NodeState.active
        assert NodeState['aborted'] == NodeState.aborted

    def test_compare_state(self):
        assert NodeState.unknown < NodeState.complete
        assert NodeState.complete < NodeState.queued
        assert NodeState.queued < NodeState.submitted
        assert NodeState.submitted < NodeState.active
        assert NodeState.active < NodeState.aborted

