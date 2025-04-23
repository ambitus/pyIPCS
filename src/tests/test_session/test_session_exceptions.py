"""
Test suite for IpcsSession exceptions

Tests:
```
    test_double_open():
        Test double open exception/warning

    test_double_close():
        Test double close warnings

    test_not_open_funcs():
        Test running functions while session is not open

    test_allocation_execeptions():
        Test allocation TypeErrors
```
"""

import pytest
from pyipcs import IpcsSession
from ..conftest import TEST_ALLOCATIONS


def test_double_open():
    """
    Object:
        IpcsSession
    Description:
        Test double open exception/warning
    """
    session = IpcsSession()
    session.update_allocations(TEST_ALLOCATIONS)
    session.open()

    session2 = IpcsSession()
    session2.update_allocations(TEST_ALLOCATIONS)
    try:
        with pytest.raises(Exception):
            session2.open()
        with pytest.warns(UserWarning):
            session.open()
    finally:
        session.close()


def test_double_close():
    """
    Object:
        IpcsSession
    Description:
        Test double close warnings
    """
    session = IpcsSession()
    session.update_allocations(TEST_ALLOCATIONS)
    session.open()
    with pytest.warns(UserWarning):
        session.close()
        session.close()


def test_not_open_funcs():
    """
    Object:
        IpcsSession
    Description:
        Test running functions while session is not open
    """
    session = IpcsSession()
    with pytest.raises(Exception):
        session.dsname_in_ddir("TEST.DSNAME")
    with pytest.raises(Exception):
        session.create_temp_ddir()
    with pytest.raises(Exception):
        session.get_defaults()
    with pytest.raises(Exception):
        session.set_defaults()


def test_allocation_execeptions():
    """
    Object:
        IpcsSession
    Description:
        Test allocation TypeErrors
    """
    # ===============
    # constructor
    # ===============

    with pytest.raises(TypeError):
        session = IpcsSession(allocations=0)
    with pytest.raises(TypeError):
        session = IpcsSession(allocations={0: ["TEST.DATA.SET1"]})
    with pytest.raises(TypeError):
        session = IpcsSession(allocations={"TESTDD": 0})
    with pytest.raises(TypeError):
        session = IpcsSession(allocations={"TESTDD": [0]})

    # =================
    # set_allocation
    # =================

    with pytest.raises(TypeError):
        session = IpcsSession()
        session.set_allocation(0, "alloc test")
    with pytest.raises(TypeError):
        session = IpcsSession()
        session.set_allocation("TESTDD", 0)
    with pytest.raises(TypeError):
        session = IpcsSession()
        session.set_allocation("TESTDD", [0])

    # ===================
    # update_allocations
    # ===================

    with pytest.raises(TypeError):
        session = IpcsSession()
        session.update_allocations(0)
    with pytest.raises(TypeError):
        session = IpcsSession()
        session.update_allocations({0: ["TEST.DATA.SET1"]})
    with pytest.raises(TypeError):
        session = IpcsSession()
        session.update_allocations({"TESTDD": 0})
    with pytest.raises(TypeError):
        session = IpcsSession()
        session.update_allocations({"TESTDD": [0]})
    with pytest.raises(TypeError):
        session = IpcsSession()
        session.update_allocations(
            {"TESTDD": ["TEST.DATA.SET1", "TEST.DATA.SET2"]},
            clear_old_allocations=0,
        )
