"""
Test suite for IpcsSesion open and close methods

Tests:
```
    test_open_close_no_params():
        Open and close IpcsSession with no parameters

    test_open_deletion_no_params():
        Open and deltion IpcsSession with no parameters

    test_open_close_hlq():
        Open and close IpcsSession with set hlq parameter

    test_open_deletion_hlq():
        Open and deletion IpcsSession with set hlq parameter
```
"""

from zoautil_py import datasets
from pyipcs import IpcsSession
from ..conftest import TEST_HLQ


def test_open_close_default_session(opened_session):
    """
    Object:
        IpcsSession
    Description:
        Open and close. IpcsSession with no parameters
    """
    check_open_close(opened_session)


def test_open_close_hlq_session(
    opened_session_hlq,
):
    """
    Object:
        IpcsSession
    Description:
        Open and close. IpcsSession with set hlq parameter
    """
    check_open_close(opened_session_hlq)


def test_open_deletion_default_session():
    """
    Object:
        IpcsSession
    Description:
        Open and deletion. IpcsSession with no parameters
    """
    check_open_deletion(None)


def test_open_deletion_hlq_session():
    """
    Object:
        IpcsSession
    Description:
        Open and deletion. IpcsSession with set hlq parameter
    """
    check_open_deletion(TEST_HLQ)


# ==================
# CHECKS
# ==================


def check_open_close(test_session):
    """
    Object:
        IpcsSession
    Check Description:
        Open and close IpcsSession
    """
    # ================================
    # Check temporary datasets exist
    # ================================
    assert datasets.list_dataset_names(f"{test_session.hlq}.PYIPCS.EXEC", migrated=True)
    assert datasets.list_dataset_names(
        f"{test_session.hlq}.PYIPCS.SYSEXEC", migrated=True
    )
    # ===============================
    # Check if temporary execs exist
    # ===============================
    assert "IPCSCMD" in datasets.list_members(
        f"{test_session.hlq}.PYIPCS.EXEC",
    )
    assert "PYIPEVAL" in datasets.list_members(
        f"{test_session.hlq}.PYIPCS.SYSEXEC",
    )
    # ===========================================
    # Check if default temporary DDIR exists
    # ===========================================
    assert datasets.list_vsam_datasets(test_session.ddir, migrated=True)

    test_ddir = test_session.ddir
    test_session.close()
    assert not test_session.active
    assert test_session.ddir is None

    # ======================================
    # Check temporary datasets don't exist
    # ======================================
    assert not datasets.list_dataset_names(
        f"{test_session.hlq}.PYIPCS.EXEC", migrated=True
    )
    assert not datasets.list_dataset_names(
        f"{test_session.hlq}.PYIPCS.SYSEXEC", migrated=True
    )
    # ===============================================
    # Check if default temporary DDIR doesn't exist
    # ===============================================
    assert not datasets.list_vsam_datasets(test_ddir, migrated=True)


def check_open_deletion(param_hlq):
    """
    Object:
        IpcsSession
    Check Description:
        Open and deletion
    """
    if param_hlq:
        test_session = IpcsSession(hlq=TEST_HLQ)
    else:
        test_session = IpcsSession()
    test_session.open()
    test_hlq = test_session.hlq
    test_ddir = test_session.ddir
    del test_session
    # ====================================================
    # Check temporary datasets don't exist after deletion
    # ====================================================
    assert not datasets.list_dataset_names(f"{test_hlq}.PYIPCS.EXEC", migrated=True)
    assert not datasets.list_dataset_names(f"{test_hlq}.PYIPCS.SYSEXEC", migrated=True)
    # ===============================================
    # Check if default temporary DDIR doesn't exist
    # ===============================================
    assert not datasets.list_vsam_datasets(test_ddir, migrated=True)
