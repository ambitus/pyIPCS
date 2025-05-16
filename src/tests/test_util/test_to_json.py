"""
Test suite for converting pyIPCS objects to json

Tests:
```
    test_to_json_hex():
         Use IpcsJsonEncoder to convert Hex object to json
    
    test_to_json_dump():
        Use IpcsJsonEncoder to convert Dump object to json
    
    test_to_json_subcmd():
        Use IpcsJsonEncoder to convert Subcmd object to json    
```
"""

import json
import pytest
from pyipcs import Hex
from pyipcs.util import IpcsJsonEncoder
from ..conftest import NO_TEST_DUMPS
from ..mock_subcmd import MockSubcmd

if NO_TEST_DUMPS:
    pytest.skip("No test z/OS dumps set", allow_module_level=True)


def test_to_json_hex():
    """
    Object:
        Hex
    Description:
        Use IpcsJsonEncoder to convert Hex object to json
    """
    hex_dict = {Hex(1): Hex(2), Hex(3): [Hex(4), Hex(5)], Hex(6): {Hex(7): Hex(8)}}
    hex_json = json.loads(json.dumps(hex_dict, cls=IpcsJsonEncoder))
    assert hex_json == {"1": "2", "3": ["4", "5"], "6": {"7": "8"}}


def test_to_json_dump(opened_session, single_test_dump):
    """
    Object:
        Dump
    Description:
        Use IpcsJsonEncoder to convert Dump object to json
    """
    dump = opened_session.init_dump(single_test_dump)

    dump_json = json.loads(json.dumps(dump, cls=IpcsJsonEncoder))
    assert len(dump_json.keys()) == 3
    assert dump_json["dsname"] == dump.dsname
    assert dump_json["ddir"] == dump.ddir
    assert isinstance(dump_json["data"], dict)

    dump.data["field0"] = 0
    dump.data["field1"] = Hex(1)
    dump.data[Hex(1)] = "field2"
    dump.data["field3"] = [Hex(1)]
    dump.data["field4"] = {Hex(1): Hex(1)}

    dump_json = json.loads(json.dumps(dump, cls=IpcsJsonEncoder))
    assert len(dump_json.keys()) == 3
    assert dump_json["dsname"] == dump.dsname
    assert dump_json["ddir"] == dump.ddir
    assert isinstance(dump_json["data"], dict)

    assert dump_json["data"]["field0"] == 0
    assert dump_json["data"]["field1"] == "1"
    assert dump_json["data"]["1"] == "field2"
    assert dump_json["data"]["field3"] == ["1"]
    assert dump_json["data"]["field4"] == {"1": "1"}


def test_to_json_subcmd():
    """
    Object:
        Subcmd
    Description:
        Use IpcsJsonEncoder to convert Subcmd object to json
    """
    subcmd = MockSubcmd("TEST OUTPUT", "YOUR SUBCMD")
    subcmd_json = json.loads(json.dumps(subcmd, cls=IpcsJsonEncoder))
    assert subcmd_json == {
        "subcmd": "YOUR SUBCMD",
        "rc": 0,
        "data": {},
        "outfile": None,
        "output": "TEST OUTPUT",
        "keep_file": False,
    }

    subcmd.data["field0"] = 0
    subcmd.data["field1"] = Hex(1)
    subcmd.data[Hex(1)] = "field2"
    subcmd.data["field3"] = [Hex(1)]
    subcmd.data["field4"] = {Hex(1): Hex(1)}
    subcmd_json = json.loads(json.dumps(subcmd, cls=IpcsJsonEncoder))
    assert subcmd_json == {
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
        "keep_file": False,
    }

    subcmd = MockSubcmd("TEST OUTPUT", "YOUR SUBCMD", outfile=True)
    subcmd_json = json.loads(json.dumps(subcmd, cls=IpcsJsonEncoder))
    assert subcmd_json == {
        "subcmd": "YOUR SUBCMD",
        "rc": 0,
        "data": {},
        "outfile": subcmd.outfile,
        "output": "TEST OUTPUT",
        "keep_file": False,
    }
