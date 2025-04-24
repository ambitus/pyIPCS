"""
LIST SLIPTRAP Custom Subcmd Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from .subcmd import Subcmd

if TYPE_CHECKING:
    from ..session import IpcsSession


class ListSliptrap(Subcmd):
    """
    LIST SLIPTRAP Custom Subcmd Object

    Runs LIST SLIPTRAP to get SLIPTRAP

    Attributes:
        data (dict):
        ```
            'sliptrap' (str|None):
                SLIPTRAP for dump. `None` if there is no SLIPTRAP
        ```

    Methods:
    ```
        __init__(
            session: IpcsSession,
            outfile: bool = False,
            keep_file: bool = False,
        ) -> None:
            Constructor for LISTDUMP Custom Subcmd Object
    ```
    """

    def __init__(
        self,
        session: IpcsSession,
        outfile: bool = False,
        keep_file: bool = False,
    ) -> None:
        """
        Constructor for LIST SLIPTRAP Custom Subcmd Object

        Args:
            session (pyipcs.IpcsSession)
            outfile (bool):
                Optional. If 'True' stores output in file
                specified in 'outfile' attribute of Subcmd object.
                If 'False' stores output in string
                specified in 'output' attribute of Subcmd object. Default is 'False'.
            keep_file (bool):
                Optional. If 'True' preserves subcommand output file after program execution.
                If 'False' deletes subcommand output file after program execution.
                Default is 'False'.
        Returns:
            None
        """

        # ========================
        # Run LISTDUMP Subcommand
        # ========================
        super().__init__(
            session,
            "LIST SLIPTRAP",
            outfile=outfile,
            keep_file=keep_file,
        )

        sliptrap_lines = self[:].splitlines()

        # If the number of lines is 1 or less there is no SLIPTRAP and return
        if len(sliptrap_lines) <= 1:
            self.data["sliptrap"] = None
            return

        # Remove first 4 lines of subcommand to get to SLIPTRAP
        sliptrap_lines = sliptrap_lines[3:]

        # Parse LIST storage to get sliptrap
        # SLIPTRAP text is between '| ' and ' |'
        self.data["sliptrap"] = ""
        for sliptrap_line in sliptrap_lines:
            self.data["sliptrap"] += sliptrap_line[
                sliptrap_line.find("| ") + len("| ") : len(sliptrap_line) - len(" |")
            ]
