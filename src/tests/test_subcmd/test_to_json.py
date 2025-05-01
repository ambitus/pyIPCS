"""
Test suite for the Subcmd method to_json

Tests:
```
    test_no_parameter_no_outfile():
        Run method with no parameters and string Subcmd output

    test_no_parameter_outfile():
        Run method with no parameters and file Subcmd output

    test_hex_conversion():
        Add to values to data dictionary
        Check Hex keys and values are converted to strings
```
"""

from pyipcs import Hex
from ..mock_subcmd import MockSubcmd


def test_no_parameter_no_outfile():
    """
    Object:
        Subcmd
    Method:
        _to_json
    Description:
        Run method with no parameters and string Subcmd output
    """
    subcmd = MockSubcmd("TEST OUTPUT", "YOUR SUBCMD ")

    json_subcmd = subcmd._to_json()

    assert json_subcmd == {
        "subcmd": "YOUR SUBCMD",
        "rc": 0,
        "data": {},
        "outfile": None,
        "output": "TEST OUTPUT",
    }


def test_no_parameter_outfile():
    """
    Object:
        Subcmd
    Method:
        _to_json
    Description:
        Run method with no parameters and file Subcmd output
    """
    subcmd = MockSubcmd("TEST OUTPUT", "YOUR SUBCMD", outfile=True)

    json_subcmd = subcmd._to_json()

    assert json_subcmd == {
        "subcmd": "YOUR SUBCMD",
        "rc": 0,
        "data": {},
        "outfile": subcmd.outfile,
        "output": "TEST OUTPUT",
    }


def test_hex_conversion():
    """
    Object:
        Subcmd
    Method:
        to_json
    Description:
        Add to values to data dictionary
        Check Hex keys and values are converted to strings
    """

    subcmd = MockSubcmd("TEST OUTPUT", "YOUR SUBCMD")

    # ====================================================
    # Add to data dictionary attribute
    # Check Hex keys and values are converted to strings
    # ====================================================

    subcmd.data["field0"] = 0
    subcmd.data["field1"] = Hex(1)
    subcmd.data[Hex(1)] = "field2"
    subcmd.data["field3"] = [Hex(1)]
    subcmd.data["field4"] = {Hex(1): Hex(1)}

    json_subcmd = subcmd._to_json()

    assert json_subcmd == {
        "subcmd": "YOUR SUBCMD",
        "output": "TEST OUTPUT",
        "outfile": None,
        "rc": 0,
        "data": {
            "field0": 0,
            "field1": "1",
            "1": "field2",
            "field3": ["1"],
            "field4": {"1": "1"},
        },
    }
