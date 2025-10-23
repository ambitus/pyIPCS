"""
Test suite for IpcsSession open and close logic

Tests
-----
test_temp_datasets
    Checks temporary datasets on session open and close

test_cleanup
    Make sure no temporary datasets are left over after previous tests
"""

import pytest
from zoautil_py import datasets
from pyipcs import IpcsSession


@pytest.mark.parametrize(
    "use_test_hlq", [False, True], ids=["default_session", "hlq_session"]
)
def test_temp_datasets(use_test_hlq, test_hlq):
    """
    Checks temporary datasets on session open and close
    """
    # ================================
    # Create IpcsSession and open
    # ================================

    test_session = None
    if use_test_hlq:
        test_session = IpcsSession(hlq=test_hlq)
    else:
        test_session = IpcsSession()

    assert not test_session.active

    assert not test_session.ddir.dsname

    test_session.open()

    # ================================
    # Check if datasets exists
    # ================================

    assert datasets.list_dataset_names(test_session.hlq_full + ".*", migrated=True)

    session_hlq = test_session.hlq_full

    # ====================================================
    # Close session and check active is working properly
    # ====================================================

    assert test_session.active

    test_session.close()

    assert not test_session.active

    # ================================
    # Check if datasets were deleted
    # ================================

    assert not datasets.list_dataset_names(session_hlq + ".*", migrated=True)


def test_cleanup(userid, test_hlq):
    """
    Make sure no temporary datasets are left over after previous tests
    """
    assert not datasets.list_dataset_names(userid + ".PYIPCS.*", migrated=True)
    assert not datasets.list_vsam_datasets(userid + ".PYIPCS.*", migrated=True)
    assert not datasets.list_dataset_names(test_hlq + ".PYIPCS.*", migrated=True)
    assert not datasets.list_vsam_datasets(test_hlq + ".PYIPCS.*", migrated=True)
