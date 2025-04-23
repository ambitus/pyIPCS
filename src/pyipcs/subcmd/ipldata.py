"""
IPLDATA Custom Subcmd Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from .subcmd import Subcmd

if TYPE_CHECKING:
    from ..session import IpcsSession


class Ipldata(Subcmd):
    """
    IPLDATA Custom Subcmd Object

    Runs IPLDATA to get ASIDs dumped

    Attributes:
        **If Subcmd object cannot find or parse one of the 'data' dictionary items below,
        the item will not be included in the 'data' dictionary.**
        data (dict):
        ```
            'ipl_date_local' (str)
            'ipl_time_local' (str)
        ```

    Methods:
    ```
        __init__(
            session: IpcsSession,
            outfile: bool = False,
            keep_file: bool = False,
        ) -> None:
            Constructor for IPLDATA Custom Subcmd Object
    ```
    """

    def __init__(
        self,
        session: IpcsSession,
        outfile: bool = False,
        keep_file: bool = False,
    ) -> None:
        """
        Constructor for IPLDATA Custom Subcmd Object

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

        # ==========================
        # Run IPLDATA Subcommand
        # ==========================
        super().__init__(
            session,
            "IPLDATA",
            outfile=outfile,
            keep_file=keep_file,
        )

        # =========================================================
        # Check to see IPL date and time is included in the output
        # =========================================================
        system_ipled_at = self.find("System IPLed at ")

        if system_ipled_at != -1:
            system_ipled_at += len("System IPLed at ")
            system_ipled_at_endline = self.find("\n", system_ipled_at)
            self.data["ipl_time_local"], self.data["ipl_date_local"] = (
                self[system_ipled_at:system_ipled_at_endline].strip().split(" on ")
            )
