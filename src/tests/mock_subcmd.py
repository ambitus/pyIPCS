# pylint: disable=unused-argument,unnecessary-pass,super-init-not-called
"""
File for MockSubcmd Object
"""

import os
from pathlib import Path
from pyipcs import Subcmd

class MockSubcmd(Subcmd):
    """
    Mock pyIPCS Subcmd Object

    Mimics Subcmd Object by bypassing IPCS call to forcefully inject output into the object
    """

    def __init__(
        self,
        mock_output: str,
        mock_subcmd: str = "MOCKSUBCMD",
        mock_rc: int = 0,
        mock_directory: str | None = None,
        outfile: bool = False,
        keep_file: bool = False,
        auth: bool = False
    ):
        """
        Constructor for MockSubcmd object

        Parameters
        ----------
        mock_output : str
            Input to inject into MockSubcmd object

        mock_subcmd : str, optional
            Will become `subcmd` attribute. `"MOCKSUBCMD"` by default.

        mock_dsname : str|None, optional
            Will become `dsname` attribute.
            `None` by default (IpcsSession Subcommand).
            Could also be a string to mimic a Dump Subcommand.

        mock_rc : int, optional
            Will become `rc` attribute

        mock_directory : str|None, optional
            Will become the directory for MockIpcsSession object.
            Default is `None` for current working directory.

        outfile : bool, optional
            Default is `False`

        keep_file : bool, optional
            Default is `False`

        Returns
        -------
        None
        """

        # ================================================
        # Set Init Values for Mock Subcommand Attributes
        # ================================================

        self._subcmd = mock_subcmd.upper().strip()
        self._keep_file = keep_file

        self._encoding = "cp1047"
        if mock_directory is None:
            self._session_directory = os.getcwd()
        else:
            self._session_directory = mock_directory

        self._outfile = None
        self._string_output = None
        self._rc = mock_rc

        self.data = {}

        if outfile:

            # Create directory_full

            mock_dir_full_path = Path(self._session_directory)

            mock_dir_full_path = mock_dir_full_path / "mock_pyipcs_directory"

            mock_dir_full_path = mock_dir_full_path / "MOCK_ID.MOCK_TIME"

            mock_dir_full_path = str(mock_dir_full_path)

            filepath = super()._create_outfile_path(mock_dir_full_path)

            Path(filepath).parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, "w", encoding=self._encoding) as outfile_obj:
                outfile_obj.write(mock_output)

            self._outfile = filepath

        else:

            self._string_output = mock_output
