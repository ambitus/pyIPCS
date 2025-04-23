"""
SELECT ALL Custom Subcmd Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from ..hex_obj import Hex
from .subcmd import Subcmd

if TYPE_CHECKING:
    from ..session import IpcsSession


class SelectAll(Subcmd):
    """
    SELECT ALL Custom Subcmd Object

    Runs SELECT ALL to get the correlation between system ASIDs and JOBNAMEs

    Attributes:
        data (dict):
            Keys are the hex ASIDs on the system and values are a dictionary
            containing the string jobname and ASCB address.
        ```
                pyipcs.Hex(ASID) (dict):
                        'jobname' (str)
                        'ascb_addr' (pyipcs.Hex)
        ```

    Methods:
    ```
        __init__(
            session: IpcsSession,
            outfile: bool = False,
            keep_file: bool = False,
        ) -> None:
            Constructor for SELECT ALL Custom Subcmd Object
    ```
    """

    def __init__(
        self,
        session: IpcsSession,
        outfile: bool = False,
        keep_file: bool = False,
    ) -> None:
        """
        Constructor for SELECT ALL Custom Subcmd Object

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
        # Run SELECT ALL Subcommand
        # ==========================
        super().__init__(
            session,
            "SELECT ALL",
            outfile=outfile,
            keep_file=keep_file,
        )

        # Grab only ASID lines from output
        asid_lines = self[
            self.find("ASID JOBNAME  ASCBADDR  SELECTION CRITERIA") :
        ].splitlines()[2:]

        # Parse ASID line into values
        for asid_line in asid_lines:
            asid, jobname, ascb_addr, _ = asid_line.split()

            asid = Hex(asid)
            ascb_addr = Hex(ascb_addr)

            self.data[asid] = {
                "jobname": jobname,
                "ascb_addr": ascb_addr,
            }
