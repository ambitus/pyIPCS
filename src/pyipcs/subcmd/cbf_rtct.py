"""
CBF RTCT Custom Subcmd Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from ..hex_obj import Hex
from .subcmd import Subcmd

if TYPE_CHECKING:
    from ..session import IpcsSession


class CbfRtct(Subcmd):
    """
    CBF RTCT Custom Subcmd Object

    Runs CBF RTCT to get ASIDs dumped

    Attributes:
        data (dict):
        ```
            'asids_dumped' (list[pyipcs.Hex]):
                List of dumped ASIDs
        ```

    Methods:
    ```
        __init__(
            session: IpcsSession,
            outfile: bool = False,
            keep_file: bool = False,
        ) -> None:
            Constructor for CBF RTCT Custom Subcmd Object
    ```
    """

    def __init__(
        self,
        session: IpcsSession,
        outfile: bool = False,
        keep_file: bool = False,
    ) -> None:
        """
        Constructor for CBF RTCT Custom Subcmd Object

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
        # Run CBF RTCT Subcommand
        # ==========================
        super().__init__(
            session,
            "CBF RTCT",
            outfile=outfile,
            keep_file=keep_file,
        )

        # Grab only ASID lines from output
        asid_lines = self[self.find("SDAS  SDF4  SDF5") :].splitlines()[2:18]

        # Parse ASID line into values
        self.data["asids_dumped"] = []
        for asid_line in asid_lines:
            _, asid, _, _ = asid_line.split()
            if asid == "0000":
                break
            self.data["asids_dumped"].append(Hex(asid))
