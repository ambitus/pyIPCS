"""
Test suite for Dump exceptions

Tests:
```
    test_not_open_funcs():
        Test running functions while session is not open
```
"""

import pytest
from pyipcs import IpcsSession
from ..conftest import NO_TEST_DUMPS

if NO_TEST_DUMPS:
    pytest.skip("No test z/OS dumps set", allow_module_level=True)


def test_not_open_funcs(opened_session, single_test_dump):
    """
    Object:
        Dump
    Description:
        Test running functions while session is not open
    """
    dump = opened_session.init_dump(single_test_dump)
    opened_session.close()
    with pytest.raises(Exception):
        opened_session.set_dump(dump)

    unopened_session = IpcsSession()
    with pytest.raises(Exception):
        dump = unopened_session.init_dump(single_test_dump)
