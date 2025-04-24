"""
Test suite for IpcsSesion set_defaults and get_defaults methods

Tests:
```
    test_set_get_defaults_no_dump():
        Check set and get defaults with no particular z/OS dump. 

    test_set_get_defaults_no_dump():
        Check set and get defaults with z/OS dump.      
```
"""

import pytest
from pyipcs import Hex
from ..conftest import NO_TEST_DUMPS


def test_set_get_defaults_no_dump(opened_session):
    """
    Object:
        IpcsSession, SetDef
    Description:
        Check set and get defaults with no particular z/OS dump.
    """
    setdef_set = opened_session.set_defaults(confirm=False, nodsname=True)

    assert setdef_set.data == {
        "confirm": False,
        "dsname": None,
        "asid": None,
        "dspname": None,
    }

    setdef_get = opened_session.get_defaults()

    assert setdef_get.data == {
        "confirm": False,
        "dsname": None,
        "asid": None,
        "dspname": None,
    }


def test_set_get_defaults_dump(opened_session, single_test_dump):
    """
    Object:
        IpcsSession, SetDef
    Description:
        Check set and get defaults with z/OS dump.
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set")

    setdef_set = opened_session.set_defaults(
        confirm=True,
        dsname=single_test_dump,
        asid=Hex("12"),
        dspname="TEST",
    )

    assert setdef_set.data == {
        "confirm": True,
        "dsname": single_test_dump,
        "asid": Hex("12"),
        "dspname": "TEST",
    }

    setdef_get = opened_session.get_defaults()

    assert setdef_get.data == {
        "confirm": True,
        "dsname": single_test_dump,
        "asid": Hex("12"),
        "dspname": "TEST",
    }
