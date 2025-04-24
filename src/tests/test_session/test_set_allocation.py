"""
Test suite for set_allocation method

Tests:
```
    test_default():
        Run set_allocation method.

    test_hlq():
        Run set_allocation method. hlq is set.

    test_overwrite():
        Run set_allocation method. Focus on overwriting allocations.
```
"""

from pyipcs import IpcsSession
from ..conftest import TEST_HLQ


def test_default():
    """
    Object:
        IpcsSession
    Description:
        Run set_allocation method.
    """
    session = IpcsSession()
    session.set_allocation("SYSEXEC", ["TEST.SYSEXEC"])
    session.set_allocation("TESTDD", ["TEST.DATA.SET1", "TEST.DATA.SET2"])
    session.set_allocation("TESTDD2", "alloc test")
    assert session.get_allocations() == {
        "IPCSPARM": ["SYS1.PARMLIB"],
        "SYSPROC": ["SYS1.SBLSCLI0"],
        "SYSEXEC": ["TEST.SYSEXEC"],
        "TESTDD": ["TEST.DATA.SET1", "TEST.DATA.SET2"],
        "TESTDD2": "alloc test",
    }


def test_hlq():
    """
    Object:
        IpcsSession
    Description:
        Run set_allocation method. hlq is set.
    """

    session = IpcsSession(hlq=TEST_HLQ)
    session.set_allocation("SYSEXEC", ["TEST.SYSEXEC"])
    session.set_allocation("TESTDD", ["TEST.DATA.SET1", "TEST.DATA.SET2"])
    session.set_allocation("TESTDD2", "alloc test")
    assert session.get_allocations() == {
        "IPCSPARM": ["SYS1.PARMLIB"],
        "SYSPROC": ["SYS1.SBLSCLI0"],
        "SYSEXEC": ["TEST.SYSEXEC"],
        "TESTDD": ["TEST.DATA.SET1", "TEST.DATA.SET2"],
        "TESTDD2": "alloc test",
    }


def test_overwrite():
    """
    Object:
        IpcsSession
    Description:
        Run set_allocation method. Focus on overwriting allocations.
    """
    session = IpcsSession()

    session.set_allocation("SYSEXEC", ["TEST.SYSEXEC"])
    session.set_allocation("SYSEXEC", ["TEST2.SYSEXEC"])

    session.set_allocation("TESTDD", ["TEST.DATA.SET1", "TEST.DATA.SET2"])
    session.set_allocation("TESTDD", ["TEST.DATA.SET3"])

    session.set_allocation("TESTDD2", "alloc test")
    session.set_allocation("TESTDD2", "alloc test2")

    session.set_allocation("TESTDD3", ["TEST.DATA.SET1", "TEST.DATA.SET2"])
    session.set_allocation("TESTDD3", "alloc test")

    session.set_allocation("TESTDD4", "alloc test")
    session.set_allocation("TESTDD4", ["TEST.DATA.SET1", "TEST.DATA.SET2"])

    assert session.get_allocations() == {
        "IPCSPARM": ["SYS1.PARMLIB"],
        "SYSPROC": ["SYS1.SBLSCLI0"],
        "SYSEXEC": ["TEST2.SYSEXEC"],
        "TESTDD": ["TEST.DATA.SET3"],
        "TESTDD2": "alloc test2",
        "TESTDD3": "alloc test",
        "TESTDD4": ["TEST.DATA.SET1", "TEST.DATA.SET2"],
    }
