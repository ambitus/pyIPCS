"""
Test suite for opcode util function

Tests
-----
test_util_opcode
    Test opcode util function
"""

import pytest
from pyipcs import Hex
from pyipcs.util import opcode


@pytest.mark.parametrize(
    "test_instruction, test_opcode",
    [
        ("D203E02C7624", "MVC"),
        (Hex("58C0101C"), "L"),
        (Hex("BFF71031").to_int(), "ICM"),
        ("343224242", None),
    ],
)
def test_util_opcode(open_session_default, test_instruction, test_opcode):
    """
    Test opcode util function
    """
    assert opcode(open_session_default, test_instruction) == test_opcode
