# pylint: disable=unused-argument,unnecessary-pass
"""
File for MockSubcmd Object
"""

import os
from unittest.mock import patch
from pyipcs import Subcmd

# =======================================================================
# !!! IMPORTANT !!!
# ---
#   MockSubcmd CAN BE RUN INDEPENDENTLY TO RUN MOCK SUBCOMMANDS
# ---
#   MockIpcsAllocations, AND MockIpcsSession ARE MERELY HELPER OBJECTS
# ---
#   AGAIN MockSubcmd CAN BE RUN WITHOUT CREATING OTHER OBJECTS
# =======================================================================


# =============================================================
# MockDumpDirectory, and MockIpcsSession Object
# =============================================================
class MockIpcsAllocations:
    """
    Mock pyIPCS IpcsAllocations object

    Used as helper to add needed variables and functions
    for MockSubcmd to bypass IPCS functionality and inject output into MockSubcmd
    """

    def get(self):
        """
        Mock Method
        """
        return {"MOCKDD": "MOCKSPEC"}

    def set(self, dd_name: str, specification: str | list[str], extend: bool = False):
        """
        Mock Method
        """
        pass

    def update(
        self,
        new_allocations: dict[str, str | list[str]],
        clear: bool = True,
        extend: bool = False
    ):
        """
        Mock Method
        """
        pass

class MockDumpDirectory:
    """
    Mock pyIPCS DumpDirectory object

    Used as helper to add needed variables and functions
    for MockSubcmd to bypass IPCS functionality and inject output into MockSubcmd
    """

    def __init__(self):
        """
        Mock Constructor
        """
        self.dsname = "MOCK.DDIR"

class MockIpcsSession:
    """
    Mock pyIPCS IpcsSession object

    Used as helper to add needed variables and functions
    for MockSubcmd to bypass IPCS functionality and inject output into MockSubcmd
    """

    def __init__(self, mock_directory):
        """
        Mock constructor
        """
        self.active = True
        self.directory = mock_directory
        self.ddir = MockDumpDirectory()
        self._session_directory_name = "mock_pyipcs_session"
        self._time_opened = "mock_time_opened"
        self.aloc = MockIpcsAllocations()

        self.mock_subcmd_output = None
        self.mock_rc = None

    def mock_set_output(self, mock_output, mock_rc):
        """
        Addtional method to inject output and return code
        """
        self.mock_subcmd_output = mock_output
        self.mock_rc = mock_rc


# ================================================================
# Mock run_ipcs_subcommand and mock run_ipcs_subcommand_outfile
# ================================================================


def run_ipcs_subcmd(session: MockIpcsSession, ipcs_subcmd: str, auth: bool) -> dict:
    """
    Mock Function
    """
    return {"rc": session.mock_rc, "output": session.mock_subcmd_output}


def run_ipcs_subcmd_outfile(
    session: MockIpcsSession,
    ipcs_subcmd: str,
    filepath: str,
    auth: bool,
    encoding: str = "cp1047",
) -> dict:
    """
    Mock Function
    """
    with open(filepath, "w", encoding=encoding) as outfile_obj:
        outfile_obj.write(session.mock_subcmd_output)
    return {"rc": session.mock_rc, "filepath": filepath}


# ====================================
# MockSubcmd Object
# ====================================


class MockSubcmd(Subcmd):
    """
    Mock pyIPCS Subcmd Object

    Mimics Subcmd Object by bypassing IPCS call to forcefully inject output into the object

    Used to test:
        subcmd output file creation/deletion,
        indexing,
        finds and get fields,
        using JCL output for comparison
    """

    def __init__(
        self,
        mock_output: str,
        mock_subcmd: str = "MOCKSUBCMD",
        mock_rc: int = 0,
        mock_directory: str | None = None,
        outfile: bool = False,
        keep_file: bool = False,
        auth: bool = False,
    ):
        """
        Constructor for MockSubcmd object

        Args:
            mock_output (str):
                Input to inject into MockSubcmd object
            mock_subcmd (str):
                Optional. Will become 'subcmd' attribute. 'MOCKSUBCMD' by default.
            mock_dsname (str|None):
                Optional. Will become 'dsname' attribute.
                None by default (IpcsSession Subcommand).
                Could also be a string to mimic a Dump Subcommand.
            mock_rc (int):
                Optional. Will become 'rc' attribute
            mock_directory (str|None):
                Optional. Will become the directory for MockIpcsSession object.
                Default is None for current working directory.
            outfile (bool):
                Optional. Default is False
            keep_file (bool):
                Optional. Default is False
        Returns:
            None
        """

        if mock_directory is None:
            mock_directory = os.getcwd()

        mock_session = MockIpcsSession(mock_directory)
        mock_session.mock_set_output(mock_output, mock_rc)

        with patch("pyipcs.subcmd.subcmd.run_ipcs_subcmd", run_ipcs_subcmd):
            with patch(
                "pyipcs.subcmd.subcmd.run_ipcs_subcmd_outfile", run_ipcs_subcmd_outfile
            ):
                super().__init__(mock_session, mock_subcmd, outfile, keep_file)
