"""
IPLDATA Custom Subcmd Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from ...subcmd import Subcmd

if TYPE_CHECKING:
    from ...session import IpcsSession


class Ipldata(Subcmd):
    """
    IPLDATA Custom Subcmd Object

    Runs IPLDATA to get ASIDs dumped

    Attributes
    ----------
    data : dict
        Keys may not appear if information is unknown or unavailable.

        - **"ipl_date_local"** (str)

        - **"ipl_time_local"** (str)

    Methods
    -------
    __init__(session)
        Constructor for IPLDATA Custom Subcmd Object
    
    """

    def __init__(
        self,
        session: IpcsSession
    ) -> None:
        """
        Constructor for IPLDATA Custom Subcmd Object

        Parameters
        ----------
        session : pyipcs.IpcsSession

        Returns
        -------
        None
        """

        # ==========================
        # Run IPLDATA Subcommand
        # ==========================
        super().__init__(
            session,
            "IPLDATA"
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
