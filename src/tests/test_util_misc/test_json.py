"""
Test suite for converting pyIPCS objects to json

Tests
-----
test_json_hex
    Use IpcsJsonEncoder to convert Hex object to json

test_json_dump
    Use IpcsJsonEncoder to convert Dump object to json

test_json_subcmd
    Use IpcsJsonEncoder to convert Subcmd object to json

"""

import json
from pyipcs import Hex
from pyipcs.util import IpcsJsonEncoder
from ..mock_subcmd import MockSubcmd

def test_json_hex():
    """
    Use IpcsJsonEncoder to convert Hex object to json
    """

    hex_obj = Hex("1")

    hex_obj_json = json.loads(json.dumps(hex_obj, cls=IpcsJsonEncoder))

    assert hex_obj_json == {
        "__ipcs_type__": "Hex",
        "value": "1"
    }

    hex_dict = {
        "2": Hex(2), 
        "3": [Hex(3), Hex(3)], 
        "4": {"4": Hex(4)},
    }

    hex_dict_json = json.loads(json.dumps(hex_dict, cls=IpcsJsonEncoder))

    assert hex_dict_json == {
        "2": {
            "__ipcs_type__": "Hex",
            "value": "2"
        },
        "3": [
            {
                "__ipcs_type__": "Hex",
                "value": "3"
            },
            {
                "__ipcs_type__": "Hex",
                "value": "3"
            },
        ],
        "4": {
            "4": {
                "__ipcs_type__": "Hex",
                "value": "4"
            },
        }
    }


def test_json_dump(open_session_default, test_dump_single):
    """
    Use IpcsJsonEncoder to convert Dump object to json
    """
    dump = open_session_default.init_dump(test_dump_single)

    dump.data["field1"] = Hex(1)

    dump_json = json.loads(json.dumps(dump, cls=IpcsJsonEncoder))

    assert dump_json["__ipcs_type__"] == "Dump"

    assert dump_json["dsname"] == dump.dsname
    assert dump_json["ddir"] == dump.ddir

    assert isinstance(dump_json["header"], dict)

    dump_json["data"] = {
        "field1": {
            "__ipcs_type__": "Hex",
            "value": "1"
        }
    }


def test_json_subcmd():
    """
    Use IpcsJsonEncoder to convert Subcmd object to json
    """

    # =====================
    # String output
    # =====================

    subcmd = MockSubcmd("TEST OUTPUT", "YOUR SUBCMD")

    subcmd.data["field1"] = Hex(1)

    subcmd_json = json.loads(json.dumps(subcmd, cls=IpcsJsonEncoder))

    assert subcmd_json == {
        "__ipcs_type__": "Subcmd",
        "subcmd": "YOUR SUBCMD",
        "output": "TEST OUTPUT",
        "outfile": None,
        "rc": 0,
        "data": {
            "field1": {
                "__ipcs_type__": "Hex",
                "value": "1"
            }
        },
        "keep_file": False,
    }

    # =====================
    # File output
    # =====================

    subcmd = MockSubcmd("TEST OUTPUT", "YOUR SUBCMD", outfile=True)

    subcmd_json = json.loads(json.dumps(subcmd, cls=IpcsJsonEncoder))

    assert subcmd_json == {
        "__ipcs_type__": "Subcmd",
        "subcmd": "YOUR SUBCMD",
        "rc": 0,
        "data": {},
        "outfile": subcmd.outfile,
        "output": "TEST OUTPUT",
        "keep_file": False,
    }
