# coding=utf-8
from takler.base.ordered_enum import OrderedEnum


def test_ordered_enum():
    class NumberTestEnum(OrderedEnum):
        One = 1
        Two = 2
        Three = 3
        ThreeAgain = 3

    assert NumberTestEnum.One < NumberTestEnum.Two
    assert NumberTestEnum.One <= NumberTestEnum.Two
    assert NumberTestEnum.Three > NumberTestEnum.Two
    assert NumberTestEnum.Three >= NumberTestEnum.Two
    assert NumberTestEnum.Three >= NumberTestEnum.ThreeAgain
    assert NumberTestEnum.Three <= NumberTestEnum.ThreeAgain
