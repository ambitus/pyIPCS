"""
SELECT ALL Custom Subcmd Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from ...hex_obj import Hex
from ...subcmd import Subcmd

if TYPE_CHECKING:
    from ...session import IpcsSession


class SelectAll(Subcmd):
    """
    SELECT ALL Custom Subcmd Object

    Runs SELECT ALL to get the correlation between system ASIDs and JOBNAMEs

    Attributes
    ----------
    data : dict
        - **"asids_all"** (list[dict])
            Info about all asids on the system at the time of the dump.
            List of dictionaries containing the hex asid, string jobname, and ASCB address.
            Check See Also section for details.
            
    Methods
    -------
    __init__(session)
        Constructor for SELECT ALL Custom Subcmd Object

    See Also
    --------
    data["asids_all"] : list[dicts]
        - **"asid"** (pyipcs.Hex)
        - **"jobname"** (str)
        - **"ascb_addr"** (pyipcs.Hex)
    """

    def __init__(
        self,
        session: IpcsSession
    ) -> None:
        """
        Constructor for SELECT ALL Custom Subcmd Object

        Parameters
        ----------
        session : pyipcs.IpcsSession

        Returns
        -------
        None
        """

        # ==========================
        # Run SELECT ALL Subcommand
        # ==========================
        super().__init__(
            session,
            "SELECT ALL"
        )

        # Grab only ASID lines from output
        asid_lines = self[
            self.find("ASID JOBNAME  ASCBADDR  SELECTION CRITERIA") :
        ].splitlines()[2:]

        self.data["asids_all"] = []

        # Parse ASID line into values
        for asid_line in asid_lines:
            asid = asid_line[1:5].strip()
            jobname = asid_line[6:14].strip()
            ascb_addr = asid_line[15:24].strip()
            if len(jobname) == 0:
                jobname = None

            asid = Hex(asid)
            ascb_addr = Hex(ascb_addr)

            self.data["asids_all"].append({
                "asid": asid,
                "jobname": jobname,
                "ascb_addr": ascb_addr,
            })
