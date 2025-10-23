"""
Test suite for Subcmd methods such as
indexing, length, find, and get_field methods

Tests
-----
test_indexing
    Test Subcmd indexing

test_len
    Test Subcmd len function

test_find
    Run find method

test_rfind
    Run rfind method

test_get_field
    Run get_field method

test_get_field2
    Run get_field2 method

test_rget_field
    Run rget_field method

test_rget_field2
    Run rget_field2 method
"""

from pyipcs import Hex
from ..mock_subcmd import MockSubcmd


def test_indexing():
    """
    Test Subcmd indexing
    """
    # =========================
    # Test with string output
    # =========================

    subcmd_string = MockSubcmd("STRING", "YOUR SUBCMD")

    assert subcmd_string[1] == "T"
    assert subcmd_string[2:4] == "RI"
    assert subcmd_string[-1] == "G"

    # =========================
    # Test with file output
    # =========================

    subcmd_file = MockSubcmd("FILE OUTPUT", "YOUR SUBCMD", outfile=True)

    assert subcmd_file[1] == "I"
    assert subcmd_file[2:4] == "LE"
    assert subcmd_file[-1] == "T"


def test_subcmd_length():
    """
    Test Subcmd Test Subcmd len function
    """
    # =========================
    # Test with string output
    # =========================

    subcmd_string = MockSubcmd("STRING", "YOUR SUBCMD")

    assert len(subcmd_string) == 6

    # =========================
    # Test with file output
    # =========================

    subcmd_file = MockSubcmd("FILE", "YOUR SUBCMD", outfile=True)

    assert len(subcmd_file) == 4


def test_find():
    """
    Run find method
    """
    # =========================
    # Test with string output
    # =========================

    subcmd_string = MockSubcmd("STRING STRING STRING", "YOUR SUBCMD")

    assert subcmd_string.find("STRING") == 0
    assert subcmd_string.find("S") == 0
    assert subcmd_string.find("STRING1") == -1
    assert subcmd_string.find("STRING", start=8) == 14
    assert subcmd_string.find("STRING", start=1, end=13) == 7

    # =========================
    # Test with file output
    # =========================

    subcmd_file = MockSubcmd("FILE FILE FILE", "YOUR SUBCMD", outfile=True)

    assert subcmd_file.find("FILE") == 0
    assert subcmd_file.find("F") == 0
    assert subcmd_file.find("FILE1") == -1
    assert subcmd_file.find("FILE", start=6) == 10
    assert subcmd_file.find("FILE", start=1, end=9) == 5


def test_rfind():
    """
    Run rfind method
    """
    # =========================
    # Test with string output
    # =========================

    subcmd_string = MockSubcmd("STRING STRING STRING", "YOUR SUBCMD")

    assert subcmd_string.rfind("STRING") == 14
    assert subcmd_string.rfind("S") == 14
    assert subcmd_string.rfind("STRING1") == -1
    assert subcmd_string.rfind("STRING", end=8) == 0
    assert subcmd_string.rfind("STRING", start=1, end=13) == 7

    # =========================
    # Test with file output
    # =========================

    subcmd_file = MockSubcmd("FILE FILE FILE", "YOUR SUBCMD", outfile=True)

    assert subcmd_file.rfind("FILE") == 10
    assert subcmd_file.rfind("F") == 10
    assert subcmd_file.rfind("FILE1") == -1
    assert subcmd_file.rfind("FILE", end=6) == 0
    assert subcmd_file.rfind("FILE", start=1, end=9) == 5


def test_get_field():
    """
    Run get_field method
    """
    # =========================
    # Test with string output
    # =========================

    subcmd_string = MockSubcmd(
        "STRING : ABC HEX(ABC)\n STRING : DEF \n STRING : GHI \n", "YOUR SUBCMD"
    )

    assert subcmd_string.get_field("STRING", " ", separator=" : ") == ["ABC", 9, 12]
    assert subcmd_string.get_field("HEX", ")", separator="(", to_hex=True) == [
        Hex("ABC"),
        17,
        20,
    ]
    assert subcmd_string.get_field("STRING1", " ", separator=" : ") == [
        None,
        -1,
        -1,
    ]
    assert subcmd_string.get_field("STRING", " ", separator=" : ", start=30) == [
        "GHI",
        47,
        50,
    ]
    assert subcmd_string.get_field("STRING", " ", separator=" : ", start=1, end=40) == [
        "DEF",
        32,
        35,
    ]

    # =========================
    # Test with file output
    # =========================

    subcmd_file = MockSubcmd(
        "STRING : ABC HEX(ABC)\n STRING : DEF \n STRING : GHI \n",
        "YOUR SUBCMD",
        outfile=True,
    )

    assert subcmd_file.get_field("STRING", " ", separator=" : ") == ["ABC", 9, 12]
    assert subcmd_file.get_field("HEX", ")", separator="(", to_hex=True) == [
        Hex("ABC"),
        17,
        20,
    ]
    assert subcmd_file.get_field("STRING1", " ", separator=" : ") == [None, -1, -1]
    assert subcmd_file.get_field("STRING", " ", separator=" : ", start=30) == [
        "GHI",
        47,
        50,
    ]
    assert subcmd_file.get_field("STRING", " ", separator=" : ", start=1, end=40) == [
        "DEF",
        32,
        35,
    ]


def test_get_field2():
    """
    Run get_field2 method
    """
    # =========================
    # Test with string output
    # =========================

    subcmd_string = MockSubcmd(
        "STRING : ABC HEX(ABC)\n STRING : DEF \n STRING : GHI \n", "YOUR SUBCMD"
    )

    assert subcmd_string.get_field2("STRING", 3, separator=" : ") == ["ABC", 9, 12]
    assert subcmd_string.get_field2("HEX", 3, separator="(", to_hex=True) == [
        Hex("ABC"),
        17,
        20,
    ]
    assert subcmd_string.get_field2("STRING1", 3, separator=" : ") == [None, -1, -1]
    assert subcmd_string.get_field2("STRING", 3, separator=" : ", start=30) == [
        "GHI",
        47,
        50,
    ]
    assert subcmd_string.get_field2("STRING", 3, separator=" : ", start=1, end=40) == [
        "DEF",
        32,
        35,
    ]

    # =========================
    # Test with file output
    # =========================

    subcmd_file = MockSubcmd(
        "STRING : ABC HEX(ABC)\n STRING : DEF \n STRING : GHI \n",
        "YOUR SUBCMD",
        outfile=True,
    )

    assert subcmd_file.get_field2("STRING", 3, separator=" : ") == ["ABC", 9, 12]
    assert subcmd_file.get_field2("HEX", 3, separator="(", to_hex=True) == [
        Hex("ABC"),
        17,
        20,
    ]
    assert subcmd_file.get_field2("STRING1", 3, separator=" : ") == [None, -1, -1]
    assert subcmd_file.get_field2("STRING", 3, separator=" : ", start=30) == [
        "GHI",
        47,
        50,
    ]
    assert subcmd_file.get_field2("STRING", 3, separator=" : ", start=1, end=40) == [
        "DEF",
        32,
        35,
    ]


def test_rget_field():
    """
    Run rget_field method
    """
    # =========================
    # Test with string output
    # =========================

    subcmd_string = MockSubcmd(
        "STRING : ABC HEX(ABC)\n STRING : DEF \n STRING : GHI \n", "YOUR SUBCMD"
    )

    assert subcmd_string.rget_field("STRING", " ", separator=" : ") == [
        "GHI",
        47,
        50,
    ]
    assert subcmd_string.rget_field("HEX", ")", separator="(", to_hex=True) == [
        Hex("ABC"),
        17,
        20,
    ]
    assert subcmd_string.rget_field("STRING1", " ", separator=" : ") == [
        None,
        -1,
        -1,
    ]
    assert subcmd_string.rget_field("STRING", " ", separator=" : ", end=20) == [
        "ABC",
        9,
        12,
    ]
    assert subcmd_string.rget_field(
        "STRING", " ", separator=" : ", start=1, end=40
    ) == ["DEF", 32, 35]

    # =========================
    # Test with file output
    # =========================

    subcmd_file = MockSubcmd(
        "STRING : ABC HEX(ABC)\n STRING : DEF \n STRING : GHI \n",
        "YOUR SUBCMD",
        outfile=True,
    )

    assert subcmd_file.rget_field("STRING", " ", separator=" : ") == ["GHI", 47, 50]
    assert subcmd_file.rget_field("HEX", ")", separator="(", to_hex=True) == [
        Hex("ABC"),
        17,
        20,
    ]
    assert subcmd_file.rget_field("STRING1", " ", separator=" : ") == [None, -1, -1]
    assert subcmd_file.rget_field("STRING", " ", separator=" : ", end=20) == [
        "ABC",
        9,
        12,
    ]
    assert subcmd_file.rget_field("STRING", " ", separator=" : ", start=1, end=40) == [
        "DEF",
        32,
        35,
    ]


def test_rget_field2():
    """
    Run rget_field2 method
    """
    # =========================
    # Test with string output
    # =========================

    subcmd_string = MockSubcmd(
        "STRING : ABC HEX(ABC)\n STRING : DEF \n STRING : GHI \n", "YOUR SUBCMD"
    )

    assert subcmd_string.rget_field2("STRING", 3, separator=" : ") == [
        "GHI",
        47,
        50,
    ]
    assert subcmd_string.rget_field2("HEX", 3, separator="(", to_hex=True) == [
        Hex("ABC"),
        17,
        20,
    ]
    assert subcmd_string.rget_field2("STRING1", 3, separator=" : ") == [
        None,
        -1,
        -1,
    ]
    assert subcmd_string.rget_field2("STRING", 3, separator=" : ", end=20) == [
        "ABC",
        9,
        12,
    ]
    assert subcmd_string.rget_field2("STRING", 3, separator=" : ", start=1, end=40) == [
        "DEF",
        32,
        35,
    ]

    # =========================
    # Test with file output
    # =========================

    subcmd_file = MockSubcmd(
        "STRING : ABC HEX(ABC)\n STRING : DEF \n STRING : GHI \n",
        "YOUR SUBCMD",
        outfile=True,
    )

    assert subcmd_file.rget_field2("STRING", 3, separator=" : ") == ["GHI", 47, 50]
    assert subcmd_file.rget_field2("HEX", 3, separator="(", to_hex=True) == [
        Hex("ABC"),
        17,
        20,
    ]
    assert subcmd_file.rget_field2("STRING1", 3, separator=" : ") == [None, -1, -1]
    assert subcmd_file.rget_field2("STRING", 3, separator=" : ", end=20) == [
        "ABC",
        9,
        12,
    ]
    assert subcmd_file.rget_field2("STRING", 3, separator=" : ", start=1, end=40) == [
        "DEF",
        32,
        35,
    ]
