"""
Test suite for update_allocations method

Tests:
```
    test_default():
        Run update_allocations method.

    test_hlq():
        Run update_allocations method. hlq is set.

    test_clear_old_allocations():
        Run update_allocations method. set clear_old_allocations to False.
```
"""

# pylint: disable=duplicate-code
from pyipcs import IpcsSession
from ..conftest import TEST_HLQ


def test_default():
    """
    Object:
        IpcsSession
    Description:
        Run update_allocations method.
    """
    session = IpcsSession()
    session.update_allocations(
        {
            "SYSEXEC": ["TEST.SYSEXEC"],
            "TESTDD": ["TEST.DATA.SET1", "TEST.DATA.SET2"],
            "TESTDD2": "alloc test",
        }
    )
    assert session.get_allocations() == {
        "SYSEXEC": ["TEST.SYSEXEC"],
        "TESTDD": ["TEST.DATA.SET1", "TEST.DATA.SET2"],
        "TESTDD2": "alloc test",
    }


def test_hlq():
    """
    Object:
        IpcsSession
    Description:
        Run update_allocations method. hlq is set.
    """
    session = IpcsSession(hlq=TEST_HLQ)
    session.update_allocations(
        {
            "SYSEXEC": ["TEST.SYSEXEC"],
            "TESTDD": ["TEST.DATA.SET1", "TEST.DATA.SET2"],
            "TESTDD2": "alloc test",
        }
    )
    assert session.get_allocations() == {
        "SYSEXEC": ["TEST.SYSEXEC"],
        "TESTDD": ["TEST.DATA.SET1", "TEST.DATA.SET2"],
        "TESTDD2": "alloc test",
    }


def test_clear_old_allocations():
    """
    Object:
        IpcsSession
    Description:
        Run update_allocations method. set clear_old_allocations to False.
    """
    session = IpcsSession()
    session.update_allocations(
        {
            "SYSEXEC": ["TEST.SYSEXEC"],
            "IPCSPARM": ["SYS1.PARMLIB"],
            "SYSPROC": ["SYS1.SBLSCLI0"],
        },
        False,
    )
    assert session.get_allocations() == {
        "IPCSPARM": ["SYS1.PARMLIB"],
        "SYSPROC": ["SYS1.SBLSCLI0"],
        "SYSEXEC": ["TEST.SYSEXEC"],
    }
