"""
Test suite for checking Subcmd logic for running IPCS subcommands.
Tests Subcmd output against JCL output.

Tests
-----
test_run_subcmd_nodsname
    Test running subcommands against no dump

test_run_subcmd_dsname
    Test running subcommands against a dump
"""
# pylint: disable=redefined-outer-name
import pytest
from pyipcs import IpcsSession, Subcmd
from ..conftest import TEST_ALLOCATIONS, TEST_DUMPS
from ..mock_subcmd_jcl import mock_subcmd_jcl

# ====================================
# Run Subcommands and Store Output
# ====================================

TEST_DSNAME_SUBCMDS = [
    "STATUS REGISTERS",
    "IEAVDUMP",
    "SYSTRACE PERFDATA",
    "SUMMARY FORMAT",
    "STATUS FAILDATA",
]

TEST_NODSNAME_SUBCMDS = ["SETDEF LIST", "LISTDUMP", "OPCODE D203E02C7624"]

@pytest.fixture(scope="session")
def mock_subcmd_list_nodsname():
    """
    Returns list[MockSubcmd]
    """
    jcl_session = IpcsSession(allocations=TEST_ALLOCATIONS)
    jcl_session.open()

    print()
    print("GENERATE JCL MOCK SUBMCDS - NODSNAME")

    mock_subcmd_list = mock_subcmd_jcl(
        test_ddir=jcl_session.ddir.dsname,
        test_allocations=TEST_ALLOCATIONS,
        test_subcmds=TEST_NODSNAME_SUBCMDS,
    )

    jcl_session.close()

    return mock_subcmd_list

@pytest.fixture(scope="session")
def mock_subcmd_dict_dsname():
    """
    Returns Dictionary where { str(Dump dsname) or "NODSNAME" : list[MockSubcmd]}
    """
    jcl_session = IpcsSession(allocations=TEST_ALLOCATIONS)
    jcl_session.open()

    mock_subcmd_dict = {}

    for jcl_dump in TEST_DUMPS:

        print()
        print(f"GENERATE JCL MOCK SUBCMDS - '{jcl_dump}'")

        jcl_session.init_dump(jcl_dump)

        mock_subcmd_dict[jcl_dump] = mock_subcmd_jcl(
            test_ddir=jcl_session.ddir.dsname,
            test_allocations=TEST_ALLOCATIONS,
            test_subcmds=TEST_DSNAME_SUBCMDS,
            test_dsname=jcl_dump,
        )

    jcl_session.close()

    return mock_subcmd_dict


@pytest.mark.parametrize("outfile", [False, True], ids=["string_output", "file_output"])
def test_run_subcmd_nodsname(open_session_default, mock_subcmd_list_nodsname, outfile):
    """
    Test running subcommands against no dump
    """

    print(f"\nTEST SUBCMD OUTPUT - NODSNAME, OUTFILE={outfile} ", end="")

    for mock_subcmd in mock_subcmd_list_nodsname:
        try:
            nodsname_subcmd = Subcmd(
                open_session_default, mock_subcmd.subcmd, outfile=outfile
            )

            assert nodsname_subcmd.output == mock_subcmd.output

            assert isinstance(nodsname_subcmd.rc, int)

            if outfile:
                assert isinstance(nodsname_subcmd.outfile, str)
            else:
                assert nodsname_subcmd.outfile is None

        except AssertionError as e:
            pytest.fail(f"Subcommand: {mock_subcmd.subcmd}, {e}")


@pytest.mark.parametrize("outfile", [False, True], ids=["string_output", "file_output"])
def test_run_subcmd_dsname(open_session_default, test_dump, mock_subcmd_dict_dsname, outfile):
    """
    Test running subcommands against a dump
    """

    print(f"\nTEST SUBCMD OUTPUT - '{test_dump}', OUTFILE={outfile} ", end="")

    open_session_default.init_dump(test_dump)

    for mock_subcmd in mock_subcmd_dict_dsname[test_dump]:
        try:
            dsname_subcmd = Subcmd(
                open_session_default, mock_subcmd.subcmd, outfile=outfile
            )

            assert dsname_subcmd.output == mock_subcmd.output

            assert isinstance(dsname_subcmd.rc, int)

            if outfile:
                assert isinstance(dsname_subcmd.outfile, str)
            else:
                assert dsname_subcmd.outfile is None

        except AssertionError as e:
            pytest.fail(f"Subcommand: {mock_subcmd.subcmd}, {e}")
