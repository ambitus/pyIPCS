"""
Test suite for general IpcsSession exceptions

Tests
-----
test_double_open
    Test double open exception/warning

test_double_close
    Test double close warnings

test_hlq_error
    Test hlq ValueError when longer than 16 chars
"""

import pytest
from pyipcs import IpcsSession


def test_double_open(test_allocations):
    """
    Test double open exception/warning
    """
    session = IpcsSession()
    session.update_allocations(test_allocations)
    session.open()

    session2 = IpcsSession()
    session2.update_allocations(test_allocations)
    try:
        with pytest.warns(UserWarning):
            session.open()
    finally:
        session.close()


def test_double_close(test_allocations):
    """
    Test double close warnings
    """
    session = IpcsSession()
    session.update_allocations(test_allocations)
    session.open()
    with pytest.warns(UserWarning):
        session.close()
        session.close()


def test_hlq_error():
    """
    Object:
        IpcsSession
    Description:
        Test hlq ValueError when longer than 16 chars
    """
    with pytest.raises(ValueError):
        IpcsSession(hlq="XXXXX.XXXXX.XXXXX")
