"""
Test suite for Hex object arithmetic

Tests:
```
    test_add():
        Test Hex add

    test_sub():
        Test Hex subtract

    test_mul():
        Test Hex multiply

    test_div():
        Test Hex division

    test_modulo():
        Test Hex modulo
```
"""

import pytest
from pyipcs import Hex


def test_add():
    """
    Object:
        Hex
    Description:
        Test Hex add
    """
    assert Hex("1") + Hex("9") == Hex("A")
    assert Hex(1) + Hex(9) == Hex("A")
    assert Hex("1") + Hex(9) == Hex("A")
    assert Hex(1) + Hex("9") == Hex("A")

    assert Hex("-1") + Hex("-9") == Hex("-A")
    assert Hex(-1) + Hex(-9) == Hex("-A")
    assert Hex("-1") + Hex(-9) == Hex("-A")
    assert Hex(-1) + Hex("-9") == Hex("-A")

    assert Hex("-1") + Hex("9") == Hex("8")
    assert Hex(-1) + Hex(9) == Hex("8")
    assert Hex("1") + Hex("-9") == Hex("-8")
    assert Hex("-1") + Hex("1") == Hex("0")


def test_sub():
    """
    Object:
        Hex
    Description:
        Test Hex subtract
    """
    assert Hex("9") - Hex("1") == Hex("8")
    assert Hex(9) - Hex(1) == Hex("8")
    assert Hex("9") - Hex(1) == Hex("8")
    assert Hex(9) - Hex("1") == Hex("8")

    assert Hex("-9") - Hex("-1") == Hex("-8")
    assert Hex(-9) - Hex(-1) == Hex("-8")
    assert Hex("-9") - Hex(-1) == Hex("-8")
    assert Hex(-9) - Hex("-1") == Hex("-8")

    assert Hex("-1") - Hex("9") == Hex("-A")
    assert Hex(-1) - Hex(9) == Hex("-A")
    assert Hex("1") - Hex("-9") == Hex("A")
    assert Hex("1") - Hex("1") == Hex("0")


def test_mul():
    """
    Object:
        Hex
    Description:
        Test Hex multiply
    """
    assert Hex("2") * Hex("4") == Hex("8")
    assert Hex(2) * Hex(4) == Hex("8")
    assert Hex("2") * Hex(4) == Hex("8")
    assert Hex(2) * Hex("4") == Hex("8")

    assert Hex("-2") * Hex("-4") == Hex("8")
    assert Hex(-2) * Hex(-4) == Hex("8")
    assert Hex("-2") * Hex(-4) == Hex("8")
    assert Hex(-2) * Hex("-4") == Hex("8")

    assert Hex("-2") * Hex("4") == Hex("-8")
    assert Hex("2") * Hex("-4") == Hex("-8")
    assert Hex(-2) * Hex(4) == Hex("-8")
    assert Hex(2) * Hex(-4) == Hex("-8")

    assert Hex("0") * Hex("4") == Hex("0")
    assert Hex("4") * Hex("0") == Hex("0")


def test_div():
    """
    Object:
        Hex
    Description:
        Test Hex division
    """
    assert Hex("4") / Hex("2") == Hex("2")
    assert Hex(4) / Hex(2) == Hex("2")
    assert Hex("4") / Hex(2) == Hex("2")
    assert Hex(4) / Hex("2") == Hex("2")

    assert Hex("5") / Hex("2") == Hex("2")
    assert Hex(5) / Hex(2) == Hex("2")
    assert Hex("5") / Hex(2) == Hex("2")
    assert Hex(5) / Hex("2") == Hex("2")

    assert Hex("-4") / Hex("-2") == Hex("2")
    assert Hex(-4) / Hex(-2) == Hex("2")
    assert Hex("-4") / Hex(-2) == Hex("2")
    assert Hex(-4) / Hex("-2") == Hex("2")

    assert Hex("-4") / Hex("2") == Hex("-2")
    assert Hex(4) / Hex(-2) == Hex("-2")
    assert Hex("-4") / Hex(2) == Hex("-2")
    assert Hex(4) / Hex("-2") == Hex("-2")

    with pytest.raises(ZeroDivisionError):
        assert Hex("4") / Hex("0")


def test_modulo():
    """
    Object:
        Hex
    Description:
        Test Hex modulo
    """
    assert Hex("5") % Hex("2") == Hex("1")
    assert Hex(5) % Hex(2) == Hex("1")
    assert Hex("5") % Hex(2) == Hex("1")
    assert Hex(5) % Hex("2") == Hex("1")

    assert Hex("-5") % Hex("2") == Hex("1")
    assert Hex(-5) % Hex(2) == Hex("1")
    assert Hex("-5") % Hex(2) == Hex("1")
    assert Hex(-5) % Hex("2") == Hex("1")

    assert Hex("5") % Hex("-2") == Hex("-1")
    assert Hex(5) % Hex(-2) == Hex("-1")
    assert Hex("5") % Hex(-2) == Hex("-1")
    assert Hex(5) % Hex("-2") == Hex("-1")

    assert Hex("-5") % Hex("-2") == Hex("-1")
    assert Hex(-5) % Hex(-2) == Hex("-1")
    assert Hex("-5") % Hex(-2) == Hex("-1")
    assert Hex(-5) % Hex("-2") == Hex("-1")
