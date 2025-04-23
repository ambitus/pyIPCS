"""
Test suite for Hex object basic methods

Tests:
```
    test_sign():
        Test Hex sign method

    test_unsigned():
        Test Hex unsigned method

    test_hex_indexing():
        Test Hex indexing

    test_hex_to_int():
        Test Hex to_int method

    test_hex_to_str():
        Test Hex to_str, __str__, __repr__ methods

    test_hex_to_char_str():
        Test Hex to_char_str method

    test_concat():
        Test Hex to_char_str method
```
"""

from pyipcs import Hex


def test_sign():
    """
    Object:
        Hex
    Description:
        Test Hex sign method
    """
    assert Hex("4").sign() == ""
    assert Hex("-4").sign() == "-"
    assert Hex("0").sign() == ""
    assert Hex("-0").sign() == ""


def test_unsigned():
    """
    Object:
        Hex
    Description:
        Test Hex unsigned method
    """
    assert Hex("4").unsigned() == Hex("4")
    assert Hex("-4").unsigned() == Hex("4")
    assert Hex("0").unsigned() == Hex("0")
    assert Hex("-0").unsigned() == Hex("0")


def test_hex_indexing():
    """
    Object:
        Hex
    Description:
        Test Hex indexing
    """
    assert Hex("123456789ABCDEF")[1] == Hex("2")
    assert Hex("-123456789ABCDEF")[1] == Hex("2")

    assert Hex("123456789ABCDEF")[-1] == Hex("F")
    assert Hex("-123456789ABCDEF")[-1] == Hex("F")

    assert Hex("123456789ABCDEF")[3:6] == Hex("456")
    assert Hex("-123456789ABCDEF")[3:6] == Hex("456")


def test_hex_to_int():
    """
    Object:
        Hex
    Description:
        Test Hex to_int method
    """
    assert Hex("4").to_int() == 4
    assert Hex("004").to_int() == 4
    assert Hex("-4").to_int() == -4
    assert Hex("-004").to_int() == -4

    assert Hex("A").to_int() == 10
    assert Hex("00A").to_int() == 10
    assert Hex("-A").to_int() == -10
    assert Hex("-00A").to_int() == -10


def test_hex_to_str():
    """
    Object:
        Hex
    Description:
        Test Hex to_str, __str__, __repr__ methods
    """
    assert Hex("4").to_str() == "4"
    assert Hex("004").to_str() == "004"
    assert Hex("-4").to_str() == "-4"
    assert Hex("-004").to_str() == "-004"

    assert Hex("A").to_str() == "A"
    assert Hex("00A").to_str() == "00A"
    assert Hex("-A").to_str() == "-A"
    assert Hex("-00A").to_str() == "-00A"

    assert str(Hex("4")) == "4"
    assert str(Hex("004")) == "004"
    assert str(Hex("-4")) == "-4"
    assert str(Hex("-004")) == "-004"

    assert str(Hex("A")) == "A"
    assert str(Hex("00A")) == "00A"
    assert str(Hex("-A")) == "-A"
    assert str(Hex("-00A")) == "-00A"

    assert repr(Hex("4")) == "4"
    assert repr(Hex("004")) == "004"
    assert repr(Hex("-4")) == "-4"
    assert repr(Hex("-004")) == "-004"

    assert repr(Hex("A")) == "A"
    assert repr(Hex("00A")) == "00A"
    assert repr(Hex("-A")) == "-A"
    assert repr(Hex("-00A")) == "-00A"


def test_hex_to_char_str():
    """
    Object:
        Hex
    Description:
        Test Hex to_char_str method
    """
    assert Hex("E3C5E2E3").to_char_str() == "TEST"
    assert Hex("54455354").to_char_str("utf-8") == "TEST"


def test_concat():
    """
    Object:
        Hex
    Description:
        Test Hex to_char_str method
    """
    assert Hex("ABCD").concat(Hex("EF")) == Hex("ABCDEF")
    assert Hex("-ABCD").concat(Hex("EF")) == Hex("-ABCDEF")
    assert Hex("ABCD").concat(Hex("-EF")) == Hex("ABCDEF")
    assert Hex("-ABCD").concat(Hex("-EF")) == Hex("-ABCDEF")

    assert Hex("AB").concat([Hex("CD"), Hex("EF")]) == Hex("ABCDEF")
    assert Hex("-AB").concat([Hex("CD"), Hex("EF")]) == Hex("-ABCDEF")
    assert Hex("AB").concat([Hex("-CD"), Hex("-EF")]) == Hex("ABCDEF")
    assert Hex("-AB").concat([Hex("-CD"), Hex("-EF")]) == Hex("-ABCDEF")
