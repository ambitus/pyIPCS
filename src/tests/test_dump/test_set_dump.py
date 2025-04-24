"""
Test suite for set_dump method

Tests:
```
    test_set_dump():
        Test set_dump method.
```
"""

import pytest
from pyipcs import Subcmd
from ..conftest import NO_TEST_DUMPS, TEST_HLQ

if NO_TEST_DUMPS:
    pytest.skip("No test z/OS dumps set", allow_module_level=True)


def test_set_dump(opened_session, single_test_dump):
    """
    Object:
        IpcsSession, Dump
    Description:
        Test set_dump method.
    """
    try:
        # ================================================
        # Create Dump Object and unset defaults for DDIR
        # ================================================
        test_ddir = TEST_HLQ + ".TEST.DDIR"
        opened_session.create_ddir(test_ddir)
        dump = opened_session.init_dump(single_test_dump, ddir=test_ddir)
        assert opened_session.set_defaults(nodsname=True).data["dsname"] is None

        # =====================
        # Close and open DDIR
        # =====================
        opened_session.close()
        opened_session.open()

        # ===================================================
        # Set dump and run subcommand to check for no errors
        # ===================================================
        opened_session.set_dump(dump)
        assert opened_session.ddir == test_ddir == dump.ddir
        assert opened_session.get_defaults().data["dsname"] == single_test_dump
        Subcmd(opened_session, "STATUS REGISTERS")

    finally:
        if not opened_session.active:
            opened_session.open()
        opened_session._delete_ddir(test_ddir)
