from math import nan
import parser


def test_is_numeric():
    assert parser.is_numeric(" ") is False
    assert parser.is_numeric("0") is True
    assert parser.is_numeric("1") is True


def test_get_leading_numeric():
    assert parser.get_leading_numeric("1a", 0) == (1, 1)
    assert parser.get_leading_numeric("123a", 0) == (123, 3)
    assert parser.get_leading_numeric("a", 0) == (nan, 0)
    assert parser.get_leading_numeric("12", 0) == (12, 2)


def test_get_literal_position():
    assert parser.get_literal_position("abc-", 0, "-") == ("abc", 3)


def test_get_numeric_size():
    assert parser.get_numeric_size(1) == 1
    assert parser.get_numeric_size(0) == 1
    assert parser.get_numeric_size(10) == 2
    assert parser.get_numeric_size(100) == 3


def test_is_alphabet():
    assert parser.is_alphabet("a") is True
    assert parser.is_alphabet("A") is False
    assert parser.is_alphabet("z") is True
    assert parser.is_alphabet("Z") is False
    assert parser.is_alphabet("0") is False
    assert parser.is_alphabet("-") is False
