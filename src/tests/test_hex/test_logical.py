# pylint: disable=unnecessary-negation
"""
Test suite for Hex object logical functions

Tests:
```
    test_eq():
        Test Hex equal

    test_ne():
        Test Hex not equal

    test_lt():
        Test Hex less than

    test_le():
        Test Hex less than or equal to

    test_gt():
        Test Hex greater than

    test_ge():
        Test Hex greater than or equal to

    test_or():
        Test Hex or

    test_and():
        Test Hex and
```
"""
from pyipcs import Hex


def test_eq():
    """
    Object:
        Hex
    Description:
        Test Hex equal
    """
    assert Hex("3") == Hex("3")
    assert Hex(3) == Hex(3)
    assert Hex("3") == Hex(3)
    assert Hex(3) == Hex("3")

    assert Hex("-3") == Hex("-3")
    assert Hex(-3) == Hex(-3)
    assert Hex("-3") == Hex(-3)
    assert Hex(-3) == Hex("-3")

    assert Hex("0") == Hex("0")
    assert Hex(0) == Hex(0)
    assert Hex("0") == Hex(0)
    assert Hex(0) == Hex("0")

    assert not Hex("3") == "3"
    assert not "3" == Hex("3")

    assert not Hex("3") == Hex("1")
    assert not Hex("1") == Hex("3")
    assert not Hex("-3") == Hex("3")


def test_ne():
    """
    Object:
        Hex
    Description:
        Test Hex not equal
    """
    assert Hex("3") != Hex("1")
    assert Hex(3) != Hex(1)
    assert Hex("3") != Hex(1)
    assert Hex(3) != Hex("1")

    assert Hex("3") != Hex("-3")
    assert Hex("-3") != Hex("3")

    assert Hex("3") != "3"
    assert "3" != Hex("3")

    assert not Hex("3") != Hex("3")
    assert not Hex("-3") != Hex("-3")
    assert not Hex("0") != Hex("0")


def test_lt():
    """
    Object:
        Hex
    Description:
        Test Hex less than
    """
    assert Hex("1") < Hex("3")
    assert Hex(1) < Hex(3)
    assert Hex("1") < Hex(3)
    assert Hex(1) < Hex("3")

    assert not Hex("3") < Hex("1")
    assert not Hex(3) < Hex(1)
    assert not Hex("3") < Hex(1)
    assert not Hex(3) < Hex("1")

    assert not Hex("3") < Hex("3")
    assert not Hex(3) < Hex(3)
    assert not Hex("3") < Hex(3)
    assert not Hex(3) < Hex("3")

    assert Hex("-1") < Hex("0")
    assert Hex(-1) < Hex(0)
    assert Hex("-1") < Hex(0)
    assert Hex(-1) < Hex("0")


def test_le():
    """
    Object:
        Hex
    Description:
        Test Hex less than or equal to
    """
    assert Hex("1") <= Hex("3")
    assert Hex(1) <= Hex(3)
    assert Hex("1") <= Hex(3)
    assert Hex(1) <= Hex("3")

    assert not Hex("3") <= Hex("1")
    assert not Hex(3) <= Hex(1)
    assert not Hex("3") <= Hex(1)
    assert not Hex(3) <= Hex("1")

    assert Hex("3") <= Hex("3")
    assert Hex(3) <= Hex(3)
    assert Hex("3") <= Hex(3)
    assert Hex(3) <= Hex("3")

    assert Hex("-1") <= Hex("0")
    assert Hex(-1) <= Hex(0)
    assert Hex("-1") <= Hex(0)
    assert Hex(-1) <= Hex("0")


def test_gt():
    """
    Object:
        Hex
    Description:
        Test Hex greater than
    """
    assert Hex("3") > Hex("1")
    assert Hex(3) > Hex(1)
    assert Hex("3") > Hex(1)
    assert Hex(3) > Hex("1")

    assert not Hex("1") > Hex("3")
    assert not Hex(1) > Hex(3)
    assert not Hex("1") > Hex(3)
    assert not Hex(1) > Hex("3")

    assert not Hex("3") > Hex("3")
    assert not Hex(3) > Hex(3)
    assert not Hex("3") > Hex(3)
    assert not Hex(3) > Hex("3")

    assert Hex("0") > Hex("-1")
    assert Hex(0) > Hex(-1)
    assert Hex("0") > Hex(-1)
    assert Hex(0) > Hex("-1")


def test_ge():
    """
    Object:
        Hex
    Description:
        Test Hex greater than or equal to
    """
    assert Hex("3") >= Hex("1")
    assert Hex(3) >= Hex(1)
    assert Hex("3") >= Hex(1)
    assert Hex(3) >= Hex("1")

    assert not Hex("1") >= Hex("3")
    assert not Hex(1) >= Hex(3)
    assert not Hex("1") >= Hex(3)
    assert not Hex(1) >= Hex("3")

    assert Hex("3") >= Hex("3")
    assert Hex(3) >= Hex(3)
    assert Hex("3") >= Hex(3)
    assert Hex(3) >= Hex("3")

    assert Hex("0") >= Hex("-1")
    assert Hex(0) >= Hex(-1)
    assert Hex("0") >= Hex(-1)
    assert Hex(0) >= Hex("-1")


def test_or():
    """
    Object:
        Hex
    Description:
        Test Hex or
    """
    assert Hex("8") | Hex("2") == Hex("A")
    assert Hex(8) | Hex(2) == Hex("A")
    assert Hex("8") | Hex(2) == Hex("A")
    assert Hex(8) | Hex("2") == Hex("A")

    assert Hex("3") | Hex("8") == Hex("B")
    assert Hex(3) | Hex(8) == Hex("B")
    assert Hex("3") | Hex(8) == Hex("B")
    assert Hex(3) | Hex("8") == Hex("B")


def test_and():
    """
    Object:
        Hex
    Description:
        Test Hex and
    """
    assert Hex("8") & Hex("A") == Hex("8")
    assert Hex(8) & Hex(10) == Hex("8")
    assert Hex("8") & Hex(10) == Hex("8")
    assert Hex(8) & Hex("A") == Hex("8")

    assert Hex("8") & Hex("2") == Hex("0")
    assert Hex(8) & Hex(2) == Hex("0")
    assert Hex("8") & Hex(2) == Hex("0")
    assert Hex(8) & Hex("2") == Hex("0")
