"""
Test suite for util functions that can be tested locally without IPCS

Tests:
```
    test_is_hex():
        Test is_hex util function

    test_psw_scrunch():
        Test psw_scrunch util function

    test_psw_parse():
        Test psw_parse util function
```
"""

import pytest
from pyipcs import Hex
from pyipcs.util import is_hex, psw_scrunch, psw_parse


def test_is_hex():
    """
    Util Function:
        psw_scrunch
    Description:
        Test is_hex util function
    """
    assert is_hex("1234567890") is True

    assert is_hex("abcdef") is True
    assert is_hex("ABCDEF") is True

    assert is_hex("GHIJK") is False
    assert is_hex("ghijk") is False

    assert is_hex("abcgdef") is False
    assert is_hex("ABCGDEF") is False


def test_psw_scrunch():
    """
    Util Function:
        psw_scrunch
    Description:
        Test psw_scrunch util function
    """
    assert psw_scrunch(Hex("070430008000000000000000054387AA")) == Hex(
        "070C3000854387AA"
    )
    assert psw_scrunch(Hex("070C3000854387AA")) == Hex("070C3000854387AA")

    assert psw_scrunch(Hex("0785200080000000000000002102345C")) == Hex(
        "078D2000A102345C"
    )
    assert psw_scrunch(Hex("078D2000A102345C")) == Hex("078D2000A102345C")

    assert psw_scrunch(Hex("0774000180000000000000001F123456")) == Hex(
        "077C00019F123456"
    )
    assert psw_scrunch(Hex("077C00019F123456")) == Hex("077C00019F123456")

    assert psw_scrunch(Hex("04041000000000000000000000FFEC24")) == Hex(
        "040C100000FFEC24"
    )
    assert psw_scrunch(Hex("040C100000FFEC24")) == Hex("040C100000FFEC24")
    with pytest.raises(ValueError):
        psw_scrunch(Hex("-040C100000FFEC24"))
    with pytest.raises(ValueError):
        psw_scrunch(Hex("040C100000FFEC2"))


def test_psw_parse():
    """
    Util Function:
        psw_parse
    Description:
        Test psw_parse util function
    """
    assert psw_parse(Hex("078D00000000634E")) == {
        "enabled": True,
        "key": 8,
        "privileged": False,
        "asc_mode": "PRIMARY",
        "cc": 0,
        "amode": 24,
        "instr_addr": Hex("00634E"),
    }

    assert psw_parse(Hex("078D40000000634E")) == {
        "enabled": True,
        "key": 8,
        "privileged": False,
        "asc_mode": "AR",
        "cc": 0,
        "amode": 24,
        "instr_addr": Hex("00634E"),
    }

    assert psw_parse(Hex("040CF0008131F224")) == {
        "enabled": False,
        "key": 0,
        "privileged": True,
        "asc_mode": "HOME",
        "cc": 3,
        "amode": 31,
        "instr_addr": Hex("0131F224"),
    }

    assert psw_parse(Hex("070C9001B65040E0")) == {
        "enabled": True,
        "key": 0,
        "privileged": True,
        "asc_mode": "SECONDARY",
        "cc": 1,
        "amode": 64,
        "instr_addr": Hex("365040E0"),
    }

    with pytest.raises(ValueError):
        psw_parse(Hex("-040C100000FFEC24"))
    with pytest.raises(ValueError):
        psw_parse(Hex("040C100000FFEC2"))
