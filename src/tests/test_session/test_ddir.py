"""
Test suite for DumpDirectory object

Tests
-----
test_init_ddir
    Checks initial temporary DDIR logic

test_create_tmp_ddir
    Checks temporary DDIR logic using DumpDirectory.create_tmp

test_create_ddir
    Checks DDIR logic using DumpDirectory.create

test_sources
    Test DumpDirectory.sources method

test_ddir_defaults
    Test some DDIR defaults
"""

import pytest
from zoautil_py import datasets
from pyipcs import Hex

@pytest.mark.parametrize(
    "test_session",
    ["open_session_default", "open_session_hlq"],
    ids=["default_session", "hlq_session"],
    indirect=True,
)
def test_init_ddir(test_session):
    """
    Checks initial temporary DDIR logic
    """
    assert datasets.list_vsam_datasets(test_session.ddir.dsname, migrated=True)

    init_ddir = test_session.ddir.dsname

    test_session.close()

    assert test_session.ddir.dsname is None

    assert not datasets.list_vsam_datasets(init_ddir, migrated=True)


@pytest.mark.parametrize(
    "test_session",
    ["open_session_default", "open_session_hlq"],
    ids=["default_session", "hlq_session"],
    indirect=True,
)
def test_create_tmp_ddir(test_session):
    """
    Checks temporary DDIR logic using DumpDirectory.create_tmp
    """
    # ==============================
    # Initial temporary DDIR
    # ==============================

    assert datasets.list_vsam_datasets(test_session.ddir.dsname, migrated=True)

    init_ddir = test_session.ddir.dsname

    # ==============================
    # Temporary DDIR
    # ==============================

    temp_ddir = test_session.ddir.create_tmp()

    assert datasets.list_vsam_datasets(temp_ddir, migrated=True)

    # =================================
    # Close session and check deletion
    # =================================

    test_session.close()

    assert test_session.ddir.dsname is None

    assert not datasets.list_vsam_datasets(init_ddir, migrated=True)
    assert not datasets.list_vsam_datasets(temp_ddir, migrated=True)


@pytest.mark.parametrize(
    "test_session",
    ["open_session_default", "open_session_hlq"],
    ids=["default_session", "hlq_session"],
    indirect=True,
)
def test_create_ddir(test_session, test_hlq):
    """
    Checks DDIR logic using DumpDirectory.create
    """
    # ==============================
    # Create DDIRs and check
    # One use=True other use=False
    # ==============================

    test_ddir1 = test_hlq + ".TEST1.DDIR"
    test_ddir2 = test_hlq + ".TEST2.DDIR"

    try:
        test_session.ddir.create(test_ddir1)

        test_session.ddir.create(test_ddir2)

        # ==================================
        # Check DDIRs exist
        # ==================================

        assert datasets.list_vsam_datasets(test_ddir1, migrated=True)
        assert datasets.list_vsam_datasets(test_ddir2, migrated=True)

        # ==================================
        # Check DDIRs exist after close
        # ==================================

        test_session.close()

        assert datasets.list_vsam_datasets(test_ddir1, migrated=True)
        assert datasets.list_vsam_datasets(test_ddir2, migrated=True)

    finally:

        # ==================================
        # Delete DDIRs if they still exist
        # ==================================

        if datasets.list_vsam_datasets(test_ddir1, migrated=True):
            test_session.ddir._delete(test_ddir1)
        if datasets.list_vsam_datasets(test_ddir2, migrated=True):
            test_session.ddir._delete(test_ddir2)

def test_sources(open_session_default, test_dump_list):
    """
    Test DumpDirectory.sources method
    """

    test_ddir = open_session_default.ddir.create_tmp()
    # open_session_default.ddir.use(test_ddir)

    test_dumps_3_max = test_dump_list[:3]

    # Initialize dumps
    print()
    for test_dump in test_dumps_3_max:
        print(f"START DUMP INITIALIZATION - '{test_dump}'")
        open_session_default.init_dump(test_dump, ddir=test_ddir)
        print(f"END DUMP INITIALIZATION - '{test_dump}'")

    test_sources_list = open_session_default.ddir.sources()

    # Check dump is in sources

    for test_dump in test_dumps_3_max:
        assert test_dump in test_sources_list, f"Test Dump: '{test_dump}'"

def test_ddir_defaults(open_session_default, test_dump_single):
    """
    Test some DDIR defaults
    """

    setdef_subcmd = open_session_default.ddir.defaults(
        confirm=True,
        dsname=test_dump_single,
        asid=Hex("12"),
        dspname="TEST",
    )

    assert setdef_subcmd.data["confirm"]
    assert setdef_subcmd.data["dsname"] == test_dump_single
    assert setdef_subcmd.data["asid"] == Hex("12")
    assert setdef_subcmd.data["dspname"] == "TEST"

    setdef_subcmd = open_session_default.ddir.defaults(
        confirm=False,
        dsname=None
    )

    assert not setdef_subcmd.data["confirm"]
    assert setdef_subcmd.data["dsname"] is None
