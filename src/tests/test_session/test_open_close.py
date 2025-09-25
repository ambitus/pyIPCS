"""
Test suite for IpcsSesion open and close methods

Tests:
```
    test_open_close_no_params():
        Open and close IpcsSession with no parameters

    test_open_deletion_no_params():
        Open and deltion IpcsSession with no parameters

    test_cleanup_close():
        Check no pyIPCS datasets exist after running test

```
"""

from zoautil_py import datasets
from ..conftest import USERID, TEST_HLQ


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

def test_cleanup_close():
    """
    Object:
        IpcsSession
    Description:
        Check no pyIPCS datasets exist after running tests
    """
    assert not datasets.list_dataset_names(USERID+".PYIPCS", migrated=True)
    assert not datasets.list_vsam_datasets(USERID+".PYIPCS", migrated=True)
    assert not datasets.list_dataset_names(TEST_HLQ+".PYIPCS", migrated=True)
    assert not datasets.list_vsam_datasets(TEST_HLQ+".PYIPCS", migrated=True)

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
    assert datasets.list_dataset_names(
        test_session._session_hlq, migrated=True
    )
    assert datasets.list_dataset_names(
        test_session._ipcsexec_dsname, migrated=True
    )
    assert datasets.list_dataset_names(
        test_session._sysexec_dsname, migrated=True
    )
    # ===============================
    # Check if temporary execs exist
    # ===============================
    # IPCSEXEC
    assert "IPCSRUN" in datasets.list_members(
        test_session._ipcsexec_dsname,
    )
    assert "IPACTIVE" in datasets.list_members(
        test_session._ipcsexec_dsname,
    )
    # SYSEXEC
    assert "IPCSEVAL" in datasets.list_members(
        test_session._sysexec_dsname,
    )
    # ===========================================
    # Check if default temporary DDIR exists
    # ===========================================
    assert datasets.list_vsam_datasets(test_session.ddir.dsname, migrated=True)

    test_ddir = test_session.ddir.dsname
    session_hlq = test_session._session_hlq
    ipcsexec_dsname = test_session._ipcsexec_dsname
    sysexec_dsname = test_session._sysexec_dsname
    assert test_session.active
    test_session.close()
    assert not test_session.active
    assert test_session.ddir.dsname is None

    # ======================================
    # Check temporary datasets don't exist
    # ======================================
    assert not datasets.list_dataset_names(
        session_hlq, migrated=True
    )
    assert not datasets.list_dataset_names(
        ipcsexec_dsname, migrated=True
    )
    assert not datasets.list_dataset_names(
        sysexec_dsname, migrated=True
    )
    # ===============================================
    # Check if default temporary DDIR doesn't exist
    # ===============================================
    assert not datasets.list_vsam_datasets(test_ddir, migrated=True)
