"""
Test suite for Hex object bitwise methods

Tests
-----
test_resize
    Test Hex resize method

test_bit_len_no_pad
    Test Hex bit_len_no_pad method

test_bit_len
    Test Hex bit_len method

test_turn_on_bit
    Test Hex turn_on_bit method

test_turn_off_bit
    est Hex turn_off_bit method

test_check_bit
    Test Hex check_bit method
"""

from pyipcs import Hex


def test_resize():
    """
    Test Hex resize method
    """

    assert Hex("ABCD").resize(8) == Hex("CD")
    assert Hex("AB").resize(16) == Hex("00AB")

    assert Hex("-ABCD").resize(8) == Hex("-CD")
    assert Hex("-AB").resize(16) == Hex("-00AB")


def test_bit_len_no_pad():
    """
    Test Hex bit_len_no_pad method
    """

    assert Hex("ABCD").bit_len_no_pad() == 16
    assert Hex("00AB").bit_len_no_pad() == 8

    assert Hex("-ABCD").bit_len_no_pad() == 16
    assert Hex("-00AB").bit_len_no_pad() == 8


def test_bit_len():
    """
    Test Hex bit_len method
    """
    assert Hex("ABCD").bit_len() == 16
    assert Hex("00AB").bit_len() == 16

    assert Hex("-ABCD").bit_len() == 16
    assert Hex("-00AB").bit_len() == 16


def test_turn_on_bit():
    """
    Test Hex turn_on_bit method
    """
    assert Hex("00").turn_on_bit(1) == Hex("40")
    assert Hex("00").turn_on_bit(1, True) == Hex("02")

    assert Hex("41").turn_on_bit(1) == Hex("41")
    assert Hex("12").turn_on_bit(1, True) == Hex("12")

    assert Hex("-41").turn_on_bit(1) == Hex("-41")
    assert Hex("-12").turn_on_bit(1, True) == Hex("-12")

    assert Hex("-80").turn_on_bit(1) == Hex("-C0")
    assert Hex("-01").turn_on_bit(1, True) == Hex("-03")


def test_turn_off_bit():
    """
    Test Hex turn_off_bit method
    """
    assert Hex("41").turn_off_bit(1) == Hex("01")
    assert Hex("12").turn_off_bit(1, True) == Hex("10")

    assert Hex("00").turn_off_bit(1) == Hex("00")
    assert Hex("00").turn_off_bit(1, True) == Hex("00")

    assert Hex("-41").turn_off_bit(1) == Hex("-01")
    assert Hex("-12").turn_off_bit(1, True) == Hex("-10")

    assert Hex("-80").turn_off_bit(0) == Hex("00")
    assert Hex("-01").turn_off_bit(0, True) == Hex("00")


def test_check_bit():
    """
    Test Hex check_bit method
    """
    assert Hex("41").check_bit(1) is True
    assert Hex("41").check_bit(0) is False

    assert Hex("41").check_bit(1, True) is False
    assert Hex("41").check_bit(0, True) is True

    assert Hex("-41").check_bit(1) is True
    assert Hex("-41").check_bit(0) is False

    assert Hex("-41").check_bit(1, True) is False
    assert Hex("-41").check_bit(0, True) is True
