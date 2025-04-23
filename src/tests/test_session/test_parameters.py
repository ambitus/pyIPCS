"""
Test suite for setting IpcsSesion parameters

Tests:
```
    test_no_parameters():
        Construct IpcsSession object with no parameters and check attributes

    test_set_hlq():
        Construct IpcsSession object, set hlq parameter, and check attributes

    test_set_directory():
        Construct IpcsSession object, set directory parameter, and check attributes

    test_set_allocations():
        Construct IpcsSession object, set allocations parameter, and check attributes.
```
"""

import os
from pyipcs import IpcsSession
from ..conftest import USERID, TEST_HLQ, TEST_DIRECTORY


def test_no_parameters():
    """
    Object:
        IpcsSession
    Description:
        Construct IpcsSession object with no parameters and check attributes
    """
    session = IpcsSession()

    # =================================================================================
    # IpcsSession Attributes:
    # userid = current z/OS system userid
    # hlq = '[userid]' by default
    # directory = '[current working directory]' by default
    # active = False because open method has not been used
    # ==================================================================================
    assert session.userid == USERID
    assert session.hlq == USERID
    assert session.directory == os.getcwd()
    assert session.active is False

    # ===================================================================
    # Allocations should be equal to allocations set in constructor
    # ===================================================================
    assert session.get_allocations() == {
        "IPCSPARM": ["SYS1.PARMLIB"],
        "SYSPROC": ["SYS1.SBLSCLI0"],
    }


def test_set_hlq():
    """
    Object:
        IpcsSession
    Description:
        Construct IpcsSession object, set hlq parameter, and check attributes.
    """

    session = IpcsSession(hlq=TEST_HLQ)

    # ====================================================================
    # Check:
    # hlq = '[hlq parameter]'
    # ====================================================================
    assert session.hlq == TEST_HLQ


def test_set_directory():
    """
    Object:
        IpcsSession
    Description:
        Construct IpcsSession object, set directory parameter, and check attributes.
    """
    session = IpcsSession(directory=os.path.join(os.getcwd(), TEST_DIRECTORY))

    # ====================================================================================
    # Check:
    # directory = '/[directory parameter]'
    # ====================================================================================
    assert session.directory == os.path.join(os.getcwd(), TEST_DIRECTORY)


def test_set_allocations():
    """
    Object:
        IpcsSession
    Attribute:
        allocations
    Description:
        Construct IpcsSession object, set allocations parameter, and check attributes.
    """
    session = IpcsSession(
        allocations={
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
