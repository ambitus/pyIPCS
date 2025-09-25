"""
Test suite to validate that subcommands can still be run with various IpcsSession parameters set

Check with with IPCS job output.

Tests:
```
    test_no_dump_subcmd_hlq():
        IpcsSession with hlq parameter set. 
        Check IPCS subcommand output with IPCS job output. 
        Subcommands not run against a particular dump. 

    test_dump_subcmd_hlq():
        IpcsSession with hlq parameter set. 
        Check IPCS subcommand output with IPCS job output. 
        Subcommands ran against z/OS dumps.

    test_no_dump_subcmd_directory():
        IpcsSession with directory parameter set. 
        Check IPCS subcommand output with IPCS job output. 
        Subcommands not run against a particular dump. 

    test_dump_subcmd_directory():
        IpcsSession with directory parameter set. 
        Check IPCS subcommand output with IPCS job output. 
        Subcommands ran against z/OS dumps.
```
"""

# pylint: disable=duplicate-code
import pytest
from pyipcs import Subcmd
from ..mock_subcmd_jcl import jcl_to_mock_subcmd
from ..conftest import NO_TEST_DUMPS

TEST_DUMP_SUBCMDS = [
    "STATUS REGISTERS",
    "IEAVDUMP",
    "SUMMARY FORMAT",
    "STATUS FAILDATA",
]

TEST_SESSION_SUBCMDS = ["SETDEF LIST", "LISTDUMP", "OPCODE D203E02C7624"]


def test_no_dump_subcmd_hlq(opened_session_hlq):
    """
    Object:
        IpcsSession, Subcmd
    Description:
        IpcsSession with hlq parameter set.
        Check IPCS subcommand output with IPCS job output.
        Subcommands not run against a particular dump.
    """

    mock_subcmds = jcl_to_mock_subcmd(
        TEST_SESSION_SUBCMDS,
        opened_session_hlq.get_allocations(),
        opened_session_hlq.ddir.dsname,
    )
    check_subcmd_output(opened_session_hlq, mock_subcmds)


def test_dump_subcmd_hlq(opened_session_hlq, single_test_dump):
    """
    Object:
        IpcsSession, Subcmd
    Description:
        IpcsSession with hlq parameter set.
        Check IPCS subcommand output with IPCS job output.
        Subcommands ran against z/OS dumps.
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set", allow_module_level=True)
    dump = opened_session_hlq.init_dump(single_test_dump)
    mock_subcmds = jcl_to_mock_subcmd(
        TEST_SESSION_SUBCMDS,
        opened_session_hlq.get_allocations(),
        dump.ddir,
        test_dsname=single_test_dump,
    )
    check_subcmd_output(opened_session_hlq, mock_subcmds)


def test_no_dump_subcmd_directory(opened_session_directory):
    """
    Object:
        IpcsSession, Subcmd
    Description:
        IpcsSession with directory parameter set.
        Check IPCS subcommand output with IPCS job output.
        Subcommands not run against a particular dump.
    """
    mock_subcmds = jcl_to_mock_subcmd(
        TEST_SESSION_SUBCMDS,
        opened_session_directory.get_allocations(),
        opened_session_directory.ddir.dsname,
    )
    check_subcmd_output(opened_session_directory, mock_subcmds)


def test_dump_subcmd_directory(opened_session_directory, single_test_dump):
    """
    Object:
        IpcsSession, Subcmd
    Description:
        IpcsSession with directory parameter set.
        Check IPCS subcommand output with IPCS job output.
        Subcommands ran against z/OS dumps.
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set", allow_module_level=True)
    dump = opened_session_directory.init_dump(single_test_dump)
    mock_subcmds = jcl_to_mock_subcmd(
        TEST_SESSION_SUBCMDS,
        opened_session_directory.get_allocations(),
        dump.ddir,
        test_dsname=single_test_dump,
    )
    check_subcmd_output(opened_session_directory, mock_subcmds)


# ================
# Checks
# =================


def check_subcmd_output(test_session, mock_subcmds):
    """
    Object:
        Subcmd
    Description:
        Check subcommand output. String and file output.
    """
    for mock_subcmd in mock_subcmds:
        try:
            subcmd_string = Subcmd(test_session, mock_subcmd.subcmd)
            assert subcmd_string.output == mock_subcmd.output
            assert subcmd_string[0] == mock_subcmd[0]
            assert subcmd_string[:] == mock_subcmd[:]
            assert (
                subcmd_string[: len(subcmd_string) // 2]
                == mock_subcmd[: len(subcmd_string) // 2]
            )

            subcmd_file = Subcmd(test_session, mock_subcmd.subcmd, outfile=True)
            assert subcmd_file[0] == mock_subcmd[0]
            assert subcmd_file[:] == mock_subcmd[:]
            assert (
                subcmd_file[: len(subcmd_file) // 2]
                == mock_subcmd[: len(subcmd_file) // 2]
            )
        except AssertionError as e:
            pytest.fail(f"Subcommand: {mock_subcmd.subcmd}, {e}")
