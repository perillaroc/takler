# coding: utf-8
from takler.node.variable import Variable


class TestVariable(object):
    def test_create(self):
        var = Variable('name', 'value')
        assert var.name == 'name'
        assert var.value == 'value'

    def test_to_dict(self):
        var = Variable('some_var', 'some_value')
        var_dict = {
            'name': 'some_var',
            'value': 'some_value'
        }
        assert var.to_dict() == var_dict