"""
LISTDUMP with parameters SELECT and DSNAME Custom Subcmd Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from ..hex_obj import Hex
from .subcmd import Subcmd

if TYPE_CHECKING:
    from ..session import IpcsSession


class ListdumpSelectDsname(Subcmd):
    """
    LISTDUMP with parameters SELECT and DSNAME Custom Subcmd Object

    Runs LISTDUMP with parameters SELECT and DSNAME
    to obtain data about storage areas included in the dump

    Attributes:
        data (dict):
        ```
            'storage_areas' (list[dict]):
                Info about storage areas included in the dump.
                    'asid' (pyipcs.Hex)
                    'total_bytes' (pyipcs.Hex|None) :
                        Total number of bytes dumped for ASID in hex.
                        None if total_bytes for ASID is not defined in 'LISTDUMP'.
                        Does not include dataspace or sumdump bytes.
                    'sumdump' (pyipcs.Hex):
                        Number of SUMMARY DUMP Data bytes dumped in hex.
                    'dataspaces' (dict):
                        {
                            str(Dataspace Name)
                            :
                            Hex(Number of bytes dumped for dataspace in hex)
                        }
        ```

    Methods:
    ```
        __init__(
            session: IpcsSession,
            dsname: str,
            outfile: bool = False,
            keep_file: bool = False,
        ) -> None:
            Constructor for LISTDUMP Custom Subcmd Object
    ```
    """

    def __init__(
        self,
        session: IpcsSession,
        dsname: str,
        outfile: bool = False,
        keep_file: bool = False,
    ) -> None:
        """
        Constructor for LISTDUMP with parameters SELECT and DSNAME Custom Subcmd Object

        Args:
            session (pyipcs.IpcsSession)
            dsname (str):
                Dataset name for DSNAME parameter.
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

        # ====================================================================
        # Run LISTDUMP LISTDUMP with parameters SELECT and DSNAME subcommand
        # ====================================================================
        super().__init__(
            session,
            f"LISTDUMP SELECT DSNAME('{dsname}')",
            outfile=outfile,
            keep_file=keep_file,
        )

        self.data["storage_areas"] = []

        # =================================================================
        # Get data about storage areas from various summaries in LISTDUMP
        # =================================================================

        # Every storage area is summarized by 'bytes described in
        storage_summary_index = self.find("bytes described in")

        # While there are summaries to add to storage_areas
        while storage_summary_index != -1:

            # Get full summary line
            storage_summary_line = self[
                self.rfind("\n", 0, storage_summary_index)
                + 1 : self.find("\n", storage_summary_index)
            ]

            # If this summarizes some ASID
            if "ASID" in storage_summary_line:

                # Get bytes described
                bytes_described = Hex(
                    storage_summary_line[
                        storage_summary_line.find("X'")
                        + len("X'") : storage_summary_line.find("' bytes described in")
                    ].replace("_", "")
                )

                # Get ASID
                asid_start = storage_summary_line.find("ASID(X'") + len("ASID(X'")
                asid_end = storage_summary_line.find("')", asid_start)
                asid = Hex(storage_summary_line[asid_start:asid_end].replace("_", ""))

                # Add standard ASID dictionary if it is not in data
                if not any(area["asid"] == asid for area in self.data["storage_areas"]):
                    self.data["storage_areas"].append({
                        "asid": asid,
                        "total_bytes": None,
                        "sumdump": Hex("0"),
                        "dataspaces": {},
                    })

                for area in self.data["storage_areas"]:
                    if area["asid"] == asid:
                        # Get DSPNAME if it is included
                        if "DSPNAME" in storage_summary_line:
                            dspname_start = storage_summary_line.find("DSPNAME(") + len(
                                "DSPNAME("
                            )
                            dspname_end = storage_summary_line.find(")", dspname_start)
                            dspname = storage_summary_line[dspname_start:dspname_end].replace(
                                "_", ""
                            )
                            area["dataspaces"][
                                dspname
                            ] = bytes_described
                        # If this is SUMMARY DUMP bytes
                        elif "SUMDUMP" in storage_summary_line:
                            area["sumdump"] = bytes_described
                        # Else just regular ASID total_bytes
                        else:
                            area["total_bytes"] = bytes_described
                        break

            # Repeat find and loop
            storage_summary_index = self.find(
                "bytes described in", storage_summary_index + 1
            )
