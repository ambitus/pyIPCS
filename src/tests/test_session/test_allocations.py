"""
Test suite for IpcsSession allocation logic

Tests
-----
test_allocations_parameter
    Test IpcsSession attribute allocation parameter

test_aloc
    Test IpcsAllocations object which is the aloc attribute of IpcsSession
"""

from pyipcs import IpcsSession


def test_allocations_parameter():
    """
    Test IpcsSession attribute allocation parameter
    """
    test_allocations = {
        "SYSEXEC": ["TEST.SYSEXEC"],
        "TESTDD": ["TEST.DATA.SET1", "TEST.DATA.SET2"],
        "TESTDD2": "test",
    }

    test_session = IpcsSession(allocations=test_allocations)

    assert test_session.aloc.get() == test_allocations


def test_aloc():
    """
    Test IpcsAllocations object which is the aloc attribute of IpcsSession
    """
    test_session = IpcsSession()

    assert test_session.aloc.get() == {
        "IPCSPARM": ["SYS1.PARMLIB"],
        "SYSPROC": ["SYS1.SBLSCLI0"],
    }

    test_session.aloc.clear()

    assert test_session.aloc.get() == {}

    # ===============================
    # Test IpcsAllocations.set()
    # ===============================

    test_session.aloc.set("TESTDD1", ["TEST.DATA1", "TEST.DATA2"])

    assert test_session.aloc.get() == {"TESTDD1": ["TEST.DATA1", "TEST.DATA2"]}

    test_session.aloc.set("TESTDD2", "TEST")

    assert test_session.aloc.get() == {
        "TESTDD1": ["TEST.DATA1", "TEST.DATA2"],
        "TESTDD2": "TEST",
    }

    test_session.aloc.set("TESTDD1", ["TEST.DATA3"], extend=True)

    assert test_session.aloc.get() == {
        "TESTDD1": ["TEST.DATA1", "TEST.DATA2", "TEST.DATA3"],
        "TESTDD2": "TEST",
    }

    test_session.aloc.set("TESTDD1", ["TEST.DATA4"])

    assert test_session.aloc.get() == {"TESTDD1": ["TEST.DATA4"], "TESTDD2": "TEST"}

    test_session.aloc.clear()

    assert test_session.aloc.get() == {}

    # ===============================
    # Test IpcsAllocations.update()
    # ===============================

    test_session.aloc.update(
        {"TESTDD1": ["TEST.DATA1", "TEST.DATA2"], "TESTDD2": "TEST"}
    )

    assert test_session.aloc.get() == {
        "TESTDD1": ["TEST.DATA1", "TEST.DATA2"],
        "TESTDD2": "TEST",
    }

    test_session.aloc.update(
        {"TESTDD1": ["TEST.DATA3"], "TESTDD3": "TEST"}, clear=False
    )

    assert test_session.aloc.get() == {
        "TESTDD1": ["TEST.DATA3"],
        "TESTDD2": "TEST",
        "TESTDD3": "TEST",
    }

    test_session.aloc.update({"TESTDD1": ["TEST.DATA4"]}, clear=False, extend=True)

    assert test_session.aloc.get() == {
        "TESTDD1": ["TEST.DATA3", "TEST.DATA4"],
        "TESTDD2": "TEST",
        "TESTDD3": "TEST",
    }

    test_session.aloc.clear()

    assert test_session.aloc.get() == {}

    # ===============================
    # Test IpcsAllocations.drop()
    # ===============================

    test_session.aloc.set("TESTDD1", ["TEST.DATA1", "TEST.DATA2"])

    assert test_session.aloc.get() == {"TESTDD1": ["TEST.DATA1", "TEST.DATA2"]}

    test_session.aloc.drop("TESTDD1")

    assert test_session.aloc.get() == {}
