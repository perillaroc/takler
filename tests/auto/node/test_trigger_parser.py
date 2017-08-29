# coding: utf-8
from takler.node.trigger_parser import parse_trigger


class TestNodeTrigger(object):
    def test_parse_trigger(self):
        tokens = parse_trigger("node == complete")
        assert tokens.node_path == 'node'
        assert tokens.operator == '=='
        assert tokens.status == 'complete'

        tokens = parse_trigger("../task==aborted")
        assert tokens.node_path == '../task'
        assert tokens.operator == '=='
        assert tokens.status == 'aborted'

        tokens = parse_trigger('/root/family/task1==complete')
        assert tokens.node_path == '/root/family/task1'
        assert tokens.operator == '=='
        assert tokens.status == 'complete'
