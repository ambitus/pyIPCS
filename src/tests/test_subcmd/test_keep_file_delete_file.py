"""
Test suite to test the process of keeping and deleting Subcmd output files.

Tests:
```
    test_no_dump_delete_file_default_session():
        Delete subcommand output file with delete_file method. 
        IpcsSession with no parameters. 
        Subcommands not run against a particular dump.

    test_dump_delete_file_default_session():
        Delete subcommand output file with delete_file method. 
        IpcsSession with no parameters. 
        Subcommands ran against z/OS dump

    test_no_dump_delete_file_directory():
        Delete subcommand output file with delete_file method. 
        IpcsSession with directory parameter set. 
        Subcommands not run against a particular dump.

    test_dump_delete_file_directory():
        Delete subcommand output file with delete_file method. 
        IpcsSession with directory parameter set. 
        Subcommands ran against z/OS dumps.

    test_no_dump_keep_file_default_session():
        Create and delete Subcmd with keep_file set to see if file is preserved. 
        IpcsSession with no parameters. 
        Subcommands not run against a particular dump.

    test_dump_keep_file_default_session():
        Create and delete Subcmd with keep_file set to see if file is preserved.
        IpcsSession with no parameters.
        Subcommands ran against z/OS dump.    

    test_no_dump_keep_file_directory():
        Create and delete Subcmd with keep_file set to see if file is preserved. 
        IpcsSession with directory parameter set. 
        Subcommands not run against a particular dump.

    test_dump_keep_file_directory():
        Create and delete Subcmd with keep_file set to see if file is preserved.
        IpcsSession with directory parameter set.
        Subcommands ran against z/OS dump.
```
"""

# pylint: disable=duplicate-code
import os
from pathlib import Path
import pytest
from pyipcs import Subcmd
from ..conftest import NO_TEST_DUMPS

TEST_DUMP_SUBCMDS = [
    "STATUS REGISTERS",
    "IEAVDUMP",
    "SYSTRACE PERFDATA",
    "SUMMARY FORMAT",
    "STATUS FAILDATA",
]

TEST_SESSION_SUBCMDS = ["SETDEF LIST", "LISTDUMP", "OPCODE D203E02C7624"]


def test_no_dump_delete_file_default_session(opened_session):
    """
    Object:
        Subcmd
    Description:
        Delete subcommand output file with delete_file method.
        IpcsSession with no parameters.
        Subcommands not run against a particular dump.
    """
    check_delete_file(opened_session, False)


def test_dump_delete_file_default_session(opened_session, single_test_dump):
    """
    Object:
        Subcmd
    Description:
        Delete subcommand output file with delete_file method.
        IpcsSession with no parameters.
        Subcommands ran against z/OS dump.
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set", allow_module_level=True)
    opened_session.init_dump(single_test_dump)
    check_delete_file(opened_session, True)


def test_no_dump_delete_file_directory(opened_session_directory):
    """
    Object:
        Subcmd
    Description:
        Delete subcommand output file with delete_file method.
        IpcsSession with directory parameter set.
        Subcommands not run against a particular dump.
    """
    check_delete_file(opened_session_directory, False)


def test_dump_delete_file_directory(opened_session_directory, single_test_dump):
    """
    Object:
        Subcmd
    Description:
        Delete subcommand output file with delete_file method.
        IpcsSession with directory parameter set.
        Subcommands ran against z/OS dump.
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set", allow_module_level=True)
    opened_session_directory.init_dump(single_test_dump)
    check_delete_file(opened_session_directory, True)


def test_no_dump_keep_file_default_session(opened_session):
    """
    Object:
        Subcmd
    Description:
        Create and delete Subcmd with keep_file set to see if file is preserved.
        IpcsSession with no parameters.
        Subcommands not run against a particular dump.
    """
    check_keep_file(opened_session, False)


def test_dump_keep_file_default_session(opened_session, single_test_dump):
    """
    Object:
        Subcmd
    Description:
        Create and delete Subcmd with keep_file set to see if file is preserved.
        IpcsSession with no parameters.
        Subcommands ran against z/OS dump.
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set", allow_module_level=True)
    opened_session.init_dump(single_test_dump)
    check_keep_file(opened_session, True)


def test_no_dump_keep_file_directory(opened_session_directory):
    """
    Object:
        Subcmd
    Description:
        Create and delete Subcmd with keep_file set to see if file is preserved.
        IpcsSession with directory parameter set.
        Subcommands not run against a particular dump.
    """
    check_keep_file(opened_session_directory, False)


def test_dump_keep_file_directory(opened_session_directory, single_test_dump):
    """
    Object:
        Subcmd
    Description:
        Create and delete Subcmd with keep_file set to see if file is preserved.
        IpcsSession with directory parameter set.
        Subcommands ran against z/OS dump.
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set", allow_module_level=True)
    opened_session_directory.init_dump(single_test_dump)
    check_delete_file(opened_session_directory, True)


# =======================
# Checks
# =======================


def check_delete_file(test_session, dump_set: bool):
    """
    Object:
        Subcmd
    Check Description:
        Delete subcommand output file with delete_file method.
    """
    test_subcmds = TEST_SESSION_SUBCMDS if dump_set else TEST_DUMP_SUBCMDS

    for test_subcmd in test_subcmds:
        try:
            subcmd = Subcmd(test_session, test_subcmd, outfile=True)
            assert isinstance(subcmd.outfile, str)

            # =======================================
            # Check if file exists
            # =======================================

            outfile_path = Path(subcmd.outfile)

            assert outfile_path.exists() and outfile_path.is_file()

            # ======================================
            # Check if files and directories exist
            # ======================================

            subcmd.delete_file()

            assert not outfile_path.exists()

            assert subcmd.outfile is None

        except AssertionError as e:

            pytest.fail(f"Subcommand: {test_subcmd}, {e}")


def check_keep_file(test_session, dump_set: bool):
    """
    Object:
        Subcmd
    Check Description:
        Create and delete Subcmd with keep_file set to see if file is preserved.
    """
    test_subcmds = TEST_SESSION_SUBCMDS if dump_set else TEST_DUMP_SUBCMDS
    for test_subcmd in test_subcmds:
        try:
            subcmd = Subcmd(test_session, test_subcmd, outfile=True, keep_file=True)
            assert subcmd.keep_file is True
            outfile = subcmd.outfile
            # ======================================
            # Check if file exists
            # ======================================
            del subcmd
            assert os.path.exists(outfile) and os.path.isfile(outfile)
        except AssertionError as e:
            pytest.fail(f"Subcommand: {test_subcmd}, {e}")
