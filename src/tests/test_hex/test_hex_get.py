"""
Test suite for Hex object get methods

Tests
-----
test_get_nibble
    Test Hex get_nibble method

test_get_byte
    Test Hex get_byte method

test_get_half_word
    Test Hex get_half_word method

test_get_word
    Test Hex get_word method

test_get_doubleword
    Test Hex get_doubleword method
"""

from pyipcs import Hex


def test_get_nibble():
    """
    Test Hex get_nibble method
    """
    assert Hex("ABCD").get_nibble(1) == Hex("B")
    assert Hex("ABCD").get_nibble(1, True) == Hex("C")

    assert Hex("-ABCD").get_nibble(1) == Hex("B")
    assert Hex("-ABCD").get_nibble(1, True) == Hex("C")


def test_get_byte():
    """
    Test Hex get_byte method
    """
    assert Hex("1234ABCD").get_byte(1) == Hex("34")
    assert Hex("1234ABCD").get_byte(1, True) == Hex("AB")

    assert Hex("-1234ABCD").get_byte(1) == Hex("34")
    assert Hex("-1234ABCD").get_byte(1, True) == Hex("AB")


def test_get_half_word():
    """
    Test Hex get_half_word method
    """
    assert Hex("0123456789ABCD").get_half_word(1) == Hex("4567")
    assert Hex("0123456789ABCD").get_half_word(1, True) == Hex("6789")

    assert Hex("-0123456789ABCD").get_half_word(1) == Hex("4567")
    assert Hex("-0123456789ABCD").get_half_word(1, True) == Hex("6789")


def test_get_word():
    """
    Test Hex get_word method
    """
    assert Hex("0123456789ABCDEF").get_word(1) == Hex("89ABCDEF")
    assert Hex("0123456789ABCDEF").get_word(1, True) == Hex("01234567")

    assert Hex("-0123456789ABCDEF").get_word(1) == Hex("89ABCDEF")
    assert Hex("-0123456789ABCDEF").get_word(1, True) == Hex("01234567")


def test_get_doubleword():
    """
    Test Hex get_doubleword method
    """
    assert Hex("0123456789ABCDEFFEDCBA9876543210").get_doubleword(1) == Hex(
        "FEDCBA9876543210"
    )
    assert Hex("0123456789ABCDEFFEDCBA9876543210").get_doubleword(1, True) == Hex(
        "0123456789ABCDEF"
    )

    assert Hex("-0123456789ABCDEFFEDCBA9876543210").get_doubleword(1) == Hex(
        "FEDCBA9876543210"
    )
    assert Hex("-0123456789ABCDEFFEDCBA9876543210").get_doubleword(1, True) == Hex(
        "0123456789ABCDEF"
    )
