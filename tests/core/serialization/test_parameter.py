from takler.core import Parameter


def test_int_parameter():
    param = Parameter("int_param", 1)
    assert param.to_dict() == dict(
        name="int_param",
        value=1
    )


def test_str_parameter():
    param = Parameter("str_param", "arrived")
    assert param.to_dict() == dict(
        name="str_param",
        value="arrived"
    )


def test_float_parameter():
    param = Parameter("float_param", 0.25)
    assert param.to_dict() == dict(
        name="float_param",
        value=0.25
    )


def test_bool_parameter():
    param = Parameter("bool_param", True)
    assert param.to_dict() == dict(
        name="bool_param",
        value=True
    )
