"""
Test suite for opcode util function

Tests:
```
    test_util_opcode():
        Test opcode util function
```
"""

import pytest
from pyipcs import Hex
from pyipcs.util import opcode


@pytest.mark.parametrize(
    "test_instruction, test_opcode",
    [
        ("D203E02C7624", "MVC"),
        (Hex("D203E02C7624"), "MVC"),
        (Hex("D203E02C7624").to_int(), "MVC"),
        ("58C0101C", "L"),
        (Hex("58C0101C"), "L"),
        (Hex("58C0101C").to_int(), "L"),
        ("BFF71031", "ICM"),
        (Hex("BFF71031"), "ICM"),
        (Hex("BFF71031").to_int(), "ICM"),
        ("BFF71031", "ICM"),
        (Hex("BFF71031"), "ICM"),
        (Hex("BFF71031").to_int(), "ICM"),
        ("5090B010", "ST"),
        (Hex("5090B010"), "ST"),
        (Hex("5090B010").to_int(), "ST"),
        ("343224242", None),
    ],
)
def test_util_opcode(opened_session, test_instruction, test_opcode):
    """
    Util Function:
        opcode
    Description:
        Test opcode util function
    """
    assert opcode(opened_session, test_instruction) == test_opcode
