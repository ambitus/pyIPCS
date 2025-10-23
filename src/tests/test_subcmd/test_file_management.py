"""
Test suite to test the process of keeping and deleting Subcmd output files.

Tests
-----
test_delete_file_method
    Test delete file using the delete file method.
"""
# pylint: disable=consider-using-enumerate
from pathlib import Path
import pytest
from pyipcs import Subcmd

TEST_NODSNAME_SUBCMDS = ["SETDEF LIST", "LISTDUMP", "OPCODE D203E02C7624"]


@pytest.mark.parametrize(
    "test_session",
    ["open_session_default", "open_session_directory"],
    ids=["default_session", "directory_session"],
    indirect=True,
)
def test_delete_file_method(test_session):
    """
    Test delete file using the delete file method.
    """

    file_subcmds = []

    for nodsname_subcmd in TEST_NODSNAME_SUBCMDS:
        file_subcmds.append(Subcmd(test_session, nodsname_subcmd, outfile=True))

    output_files = [file_subcmd.outfile for file_subcmd in file_subcmds]

    for i in range(len(file_subcmds)):

        file_subcmd = file_subcmds[i]
        output_file_path = Path(output_files[i])

        # Check that file exists

        assert output_file_path.exists() and output_file_path.is_file()

        file_subcmd.delete_file()

        # Check that file was deleted

        assert not output_file_path.exists()

        # Check internal object functionality

        assert file_subcmd.outfile is None

        # pylint: disable=pointless-statement
        with pytest.raises(Exception):
            file_subcmd[1]
        with pytest.raises(Exception):
            file_subcmd[1:5]
        with pytest.raises(Exception):
            file_subcmd.find("TEST")
        with pytest.raises(Exception):
            file_subcmd.rfind("TEST")
        with pytest.raises(Exception):
            len(file_subcmd)
        # pylint: enable=pointless-statement

    # Check directory is deleted

    assert not Path(test_session.directory_full).exists()


@pytest.mark.parametrize(
    "test_session",
    ["open_session_default", "open_session_directory"],
    ids=["default_session", "directory_session"],
    indirect=True,
)
def test_keep_file(test_session):
    """
    Test keep_file attribute
    """

    file_subcmds = []

    for nodsname_subcmd in TEST_NODSNAME_SUBCMDS:
        file_subcmds.append(
            Subcmd(test_session, nodsname_subcmd, outfile=True, keep_file=True)
        )

    output_files = [file_subcmd.outfile for file_subcmd in file_subcmds]

    for i in range(len(file_subcmds)):

        file_subcmd = file_subcmds[i]

        output_file_path = Path(output_files[i])

        # Check keep_file is True

        assert file_subcmd.keep_file

        # Check that file exists

        assert output_file_path.exists() and output_file_path.is_file()

        del file_subcmd

        # Check that file still exists

        assert output_file_path.exists() and output_file_path.is_file()
