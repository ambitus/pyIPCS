"""
Test suite for the Dump method to_json

Tests:
```
    test_to_json():
        Run to_json method
```
"""

import pytest
from pyipcs import Hex
from ..conftest import NO_TEST_DUMPS

if NO_TEST_DUMPS:
    pytest.skip("No test z/OS dumps set", allow_module_level=True)


def test_to_json(opened_session, single_test_dump):
    """
    Object:
        Dump
    Method:
        _to_json
    Description:
        Run _to_json method
    """
    dump_obj = opened_session.init_dump(single_test_dump)

    dump_json = dump_obj._to_json()
    assert len(dump_json.keys()) == 3
    assert dump_json["dsname"] == dump_obj.dsname
    assert dump_json["ddir"] == dump_obj.ddir
    assert isinstance(dump_json["data"], dict)

    dump_obj.data["field0"] = 0
    dump_obj.data["field1"] = Hex(1)
    dump_obj.data[Hex(1)] = "field2"
    dump_obj.data["field3"] = [Hex(1)]
    dump_obj.data["field4"] = {Hex(1): Hex(1)}

    dump_json = dump_obj._to_json()
    assert len(dump_json.keys()) == 3
    assert dump_json["dsname"] == dump_obj.dsname
    assert dump_json["ddir"] == dump_obj.ddir
    assert isinstance(dump_json["data"], dict)

    assert dump_json["data"]["field0"] == 0
    assert dump_json["data"]["field1"] == "1"
    assert dump_json["data"]["1"] == "field2"
    assert dump_json["data"]["field3"] == ["1"]
    assert dump_json["data"]["field4"] == {"1": "1"}
