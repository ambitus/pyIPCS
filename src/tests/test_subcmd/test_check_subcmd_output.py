"""
Test suite for Subcmd output. Validate with with IPCS job output.

Tests:
```
    test_check_subcmd_output_no_dump_string():
        Check Subcmd object output with IPCS job output. 
        Subcommands not run against a particular dump. 
        String output.

    test_check_subcmd_output_no_dump_file():
        Check Subcmd object output with IPCS job output. 
        Subcommands not run against a particular dump. 
        File output.

    test_check_subcmd_output_dump_string():
        Check Subcmd object output with IPCS job output. 
        Subcommands ran against z/OS dumps.
        String output.

    test_check_subcmd_output_dump_file()
        Check Subcmd object output with IPCS job output. 
        Subcommands ran against z/OS dumps.
        File output.
```
"""

import pytest
from pyipcs import Subcmd
from ..mock_subcmd_jcl import jcl_to_mock_subcmd
from ..conftest import NO_TEST_DUMPS


TEST_DUMP_SUBCMDS = [
    "STATUS REGISTERS",
    "IEAVDUMP",
    "SYSTRACE PERFDATA",
    "SUMMARY FORMAT",
    "STATUS FAILDATA",
]

TEST_SESSION_SUBCMDS = ["SETDEF LIST", "LISTDUMP", "OPCODE D203E02C7624"]


def test_check_subcmd_output_no_dump_string(opened_session):
    """
    Object:
        Subcmd
    Description:
        Check Subcmd object output with IPCS job output.
        Subcommands not run against a particular dump.
        String output.
    """

    mock_subcmds = jcl_to_mock_subcmd(
        TEST_SESSION_SUBCMDS,
        opened_session.get_allocations(),
        opened_session.ddir,
    )
    check_subcmd_output_string(opened_session, mock_subcmds)


def test_check_subcmd_output_no_dump_file(opened_session):
    """
    Object:
        Subcmd
    Description:
        Check Subcmd object output with IPCS job output.
        Subcommands not run against a particular dump.
        File output.
    """
    mock_subcmds = jcl_to_mock_subcmd(
        TEST_SESSION_SUBCMDS,
        opened_session.get_allocations(),
        opened_session.ddir,
    )
    check_subcmd_output_file(opened_session, mock_subcmds)


def test_check_subcmd_output_dump_string(opened_session, test_dump):
    """
    Object:
        Subcmd
    Description:
        Check Subcmd object output with IPCS job output.
        Subcommands ran against z/OS dumps.
        String output.
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set")
    dump = opened_session.init_dump(test_dump)
    mock_subcmds = jcl_to_mock_subcmd(
        TEST_SESSION_SUBCMDS,
        opened_session.get_allocations(),
        dump.ddir,
        test_dsname=test_dump,
    )
    check_subcmd_output_string(opened_session, mock_subcmds)


def test_check_subcmd_output_dump_file(opened_session, test_dump):
    """
    Object:
        Subcmd
    Description:
        Check Subcmd object output with IPCS job output.
        Subcommands ran against z/OS dumps.
        File output.
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set")
    dump = opened_session.init_dump(test_dump)
    mock_subcmds = jcl_to_mock_subcmd(
        TEST_SESSION_SUBCMDS,
        opened_session.get_allocations(),
        dump.ddir,
        test_dsname=test_dump,
    )
    check_subcmd_output_file(opened_session, mock_subcmds)


# ======================
# Checks
# ======================


def check_subcmd_output_string(test_session, mock_subcmds):
    """
    Object:
        Subcmd
    Description:
        Check subcommand output. String output.
    """
    for mock_subcmd in mock_subcmds:
        try:
            subcmd_string = Subcmd(test_session, mock_subcmd.subcmd)

            assert subcmd_string.subcmd == mock_subcmd.subcmd
            assert subcmd_string.outfile is None
            assert subcmd_string.keep_file is False
            assert isinstance(subcmd_string.rc, int)
            assert not subcmd_string.data

            assert subcmd_string.output == mock_subcmd.output

            assert subcmd_string[0] == mock_subcmd[0]
            assert subcmd_string[:] == mock_subcmd[:]
            assert (
                subcmd_string[: len(subcmd_string) // 2]
                == mock_subcmd[: len(subcmd_string) // 2]
            )

        except AssertionError as e:
            pytest.fail(f"Subcommand: {mock_subcmd.subcmd}, {e}")


def check_subcmd_output_file(test_session, mock_subcmds):
    """
    Object:
        Subcmd
    Description:
        Check subcommand output. File output.
    """
    for mock_subcmd in mock_subcmds:
        try:
            subcmd_file = Subcmd(test_session, mock_subcmd.subcmd, outfile=True)

            assert subcmd_file.subcmd == mock_subcmd.subcmd
            assert isinstance(subcmd_file.outfile, str)
            assert subcmd_file.keep_file is False
            assert isinstance(subcmd_file.rc, int)
            assert not subcmd_file.data

            assert subcmd_file.output == mock_subcmd.output

            assert subcmd_file[0] == mock_subcmd[0]
            assert subcmd_file[:] == mock_subcmd[:]
            assert (
                subcmd_file[: len(subcmd_file) // 2]
                == mock_subcmd[: len(subcmd_file) // 2]
            )
        except AssertionError as e:
            pytest.fail(f"Subcommand: {mock_subcmd.subcmd}, {e}")
