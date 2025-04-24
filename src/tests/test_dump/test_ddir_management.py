"""
Test suite for DDIR management within pyIPCS

Tests:
```
    test_create_ddir_default_session():
        Check regular DDIR creation. IpcsSession with no parameters.

    test_create_ddir_hlq_session():
        Check regular DDIR creation. IpcsSession with hlq parameter set.

    test_ddir_dump_constructor_default_session():
        Check DDIR creation with Dump constructor. IpcsSession with no parameters.

    test_ddir_dump_constructor_hlq_session():
        Check DDIR creation with Dump constructor. 
        IpcsSession with hlq parameter set.

    test_use_cur_ddir_default_session():
        Check DDIR setting with use_cur_ddir parameter. IpcsSession with no parameters.
    
    test_use_cur_ddir_hlq_session():
        Check DDIR setting with use_cur_ddir parameter.
        IpcsSession with hlq parameter set.

    test_temp_ddir_default_session():
        Check temporary DDIR creation. IpcsSession with no parameters.

    test_temp_ddir_hlq_session():
        Check temporary DDIR creation. IpcsSession with hlq parameter set.
```
"""

import pytest
from zoautil_py import datasets
from pyipcs import Subcmd
from ..conftest import NO_TEST_DUMPS, TEST_HLQ

if NO_TEST_DUMPS:
    pytest.skip("No test z/OS dumps set", allow_module_level=True)


def test_create_ddir_default_session(opened_session, all_test_dumps):
    """
    Object:
        IpcsSession
    Description:
        Check regular DDIR creation. IpcsSession with no parameters.
    """
    check_create_ddir(opened_session, all_test_dumps)


def test_create_ddir_hlq_session(opened_session_hlq, all_test_dumps):
    """
    Object:
        IpcsSession
    Description:
        Check regular DDIR creation. IpcsSession with hlq parameter set.
    """
    check_create_ddir(opened_session_hlq, all_test_dumps)


def test_ddir_dump_constructor_default_session(opened_session, single_test_dump):
    """
    Object:
        IpcsSession, Dump
    Description:
        Check DDIR creation with Dump constructor. IpcsSession with no parameters.
    """
    check_ddir_dump_constructor(opened_session, single_test_dump)


def test_ddir_dump_constructor_hlq_session(opened_session_hlq, single_test_dump):
    """
    Object:
        IpcsSession, Dump
    Description:
        Check DDIR creation with Dump constructor.
        IpcsSession with hlq parameter set.
    """
    check_ddir_dump_constructor(opened_session_hlq, single_test_dump)


def test_use_cur_ddir_default_session(opened_session, single_test_dump):
    """
    Object:
        IpcsSession, Dump
    Description:
        Check DDIR setting with use_cur_ddir parameter. IpcsSession with no parameters.
    """
    check_use_cur_ddir(opened_session, single_test_dump)


def test_use_cur_ddir_hlq_session(opened_session_hlq, single_test_dump):
    """
    Object:
        IpcsSession, Dump
    Description:
        Check DDIR setting with use_cur_ddir parameter.
        IpcsSession with hlq parameter set.
    """
    check_use_cur_ddir(opened_session_hlq, single_test_dump)


def test_temp_ddir_default_session(opened_session, all_test_dumps):
    """
    Object:
        Dump
    Description:
        Check temporary DDIR creation. IpcsSession with no parameters.
    """
    check_temp_ddir(opened_session, all_test_dumps)


def test_temp_ddir_hlq_session(opened_session_hlq, all_test_dumps):
    """
    Object:
        Dump
    Description:
        Check temporary DDIR creation. IpcsSession with hlq parameter set.
    """
    check_temp_ddir(opened_session_hlq, all_test_dumps)


# ==================================
# CHECKS
# ==================================


def check_create_ddir(test_session, all_test_dumps):
    """
    Object:
        IpcsSession, Dump
    Check Description:
        Check DDIR creation with IpcsSession create_ddir method
    """
    try:
        # ==============================
        # Add all dumps to test DDIR
        # ==============================
        test_ddir = TEST_HLQ + ".TEST.DDIR"
        # ======================================================
        # Check test DDIR doesn't exist already and delete it
        # ======================================================
        if datasets.list_vsam_datasets(test_ddir):
            test_session._delete_ddir(test_ddir)
        assert not datasets.list_vsam_datasets(test_ddir)
        # ==============================================
        # Check if create_ddir creates the VSAM dataset
        # ==============================================
        test_session.create_ddir(test_ddir)
        assert datasets.list_vsam_datasets(test_ddir)
        # ==================================================
        # Check dump is in DDIR after dump object creation
        # ==================================================
        test_session.set_ddir(test_ddir)
        dump_objs = []
        for test_dump in all_test_dumps:
            try:
                assert not test_session.dsname_in_ddir(test_dump)
                dump_objs.append(test_session.init_dump(test_dump, ddir=test_ddir))
                assert test_session.dsname_in_ddir(test_dump)
                # Run subcommand to confirm
                Subcmd(test_session, "STATUS REGISTERS")
            except AssertionError as e:
                pytest.fail(f"Dump: {test_dump}, {e}")
        # ============================================================================
        # Check dumps are still in DDIR after session close and Dump object deletion
        # ============================================================================
        del dump_objs
        test_session.close()
        test_session.open()
        assert datasets.list_vsam_datasets(test_ddir)
        test_session.set_ddir(test_ddir)
        for test_dump in all_test_dumps:
            assert test_session.dsname_in_ddir(test_dump)
    finally:
        if not test_session.active:
            test_session.open()
        test_session._delete_ddir(test_ddir)


def check_ddir_dump_constructor(test_session, single_test_dump):
    """
    Object:
        IpcsSession, Dump
    Check Description:
        Check DDIR creation with Dump constructor
    """
    try:
        # ==============================
        # Add dump to test DDIR
        # ==============================
        test_ddir = TEST_HLQ + ".TEST.DDIR"
        # ======================================================
        # Check test DDIR doesn't exist already and delete it
        # ======================================================
        if datasets.list_vsam_datasets(test_ddir):
            test_session._delete_ddir(test_ddir)
        assert not datasets.list_vsam_datasets(test_ddir)
        # ==================================================
        # Check dump is in DDIR after dump object creation
        # ==================================================
        dump_obj = test_session.init_dump(single_test_dump, ddir=test_ddir)
        assert test_session.dsname_in_ddir(single_test_dump)
        Subcmd(test_session, "STATUS REGISTERS")
        # ============================================================================
        # Check dumps are still in DDIR after session close and Dump object deletion
        # ============================================================================
        del dump_obj
        test_session.close()
        test_session.open()
        test_session.set_ddir(test_ddir)
        assert test_session.dsname_in_ddir(single_test_dump)
    finally:
        if not test_session.active:
            test_session.open()
        test_session._delete_ddir(test_ddir)


def check_use_cur_ddir(test_session, single_test_dump):
    """
    Object:
        IpcsSession, Dump
    Check Description:
        Check DDIR setting with use_cur_ddir parameter
    """
    # ===========================
    # Just use the Default DDIR
    # ===========================
    test_ddir = test_session.ddir
    # ==================================================
    # Check dump is in DDIR after dump object creation
    # ==================================================
    test_session.init_dump(single_test_dump, use_cur_ddir=True)
    assert test_session.ddir == test_ddir
    assert test_session.dsname_in_ddir(single_test_dump)
    Subcmd(test_session, "STATUS REGISTERS")


def check_temp_ddir(test_session, all_test_dumps):
    """
    Object:
        Dump
    Description:
        Check temporary DDIR creation.
    """
    # ====================================================
    # Check 1 temporary ddir per active dump object
    # ====================================================
    dump_objs = []
    ddirs = set()
    for test_dump in all_test_dumps:
        dump_objs.append(test_session.init_dump(test_dump))
        assert dump_objs[-1].ddir not in ddirs, f"Dump: {test_dump}"
        assert datasets.list_vsam_datasets(dump_objs[-1].ddir), f"Dump: {test_dump}"
        ddirs.add(dump_objs[-1].ddir)
        # Check subcommand can be run
        Subcmd(test_session, "STATUS REGISTERS")
    test_session.close()
    # =========================================================
    # Check no temporary ddirs exist after test_session close
    # =========================================================
    for ddir in ddirs:
        assert not datasets.list_vsam_datasets(ddir)
