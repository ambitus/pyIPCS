"""
Dump Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import textwrap
from pprint import pformat
import copy
from ..hex_obj import Hex
from ..util import is_dump
from ..error_handling import (
    InvalidReturnCodeError,
    SessionNotActiveError,
)
from ..subcmd import Subcmd
from .dump_subcmds import (
    ListSliptrap,
    ListdumpSelectDsname,
    CbfRtct,
    SelectAll,
    Ipldata,
)
from .dump_header import DumpHeader

if TYPE_CHECKING:
    from ..session import IpcsSession


class Dump:
    """
    Dump Object

    Initializes a z/OS dump and stores general information.

    Can create a Dump object using `pyipcs.IpcsSession.init_dump()`

    Attributes
    ----------
    dsname : str
        Dump dataset name.
        
    ddir : str
        Dump directory when dump was initialized.

    header : pyipcs.DumpHeader
        Custom dictionary object containing information about the dump from the dump header.

    data : dict
        Dictionary containing general information about the dump from various subcommands.
        Editable by user to store additional info about a dump.
        Keys may not appear if information is unknown or unavailable.

        - **"sliptrap"** (str)
            Included in 'data' dictionary if the dump is a SLIP dump.
            Obtained from `LIST SLIPTRAP` subcommand.

        - **"ipl_date_local"** (str)
            Known if CSA is dumped.
            Obtained from `IPLDATA` subcommand.

        - **"ipl_time_local"** (str)
            Known if CSA is dumped.
            Obtained from `IPLDATA` subcommand.

        - **"asids_dumped"** (list[pyipcs.Hex])
            List of ASIDs that were dumped.
            Obtained from `CBF RTCT` subcommand.

        - **"asids_all"** (list[dict])
            Info about all asids on the system at the time of the dump.
            List of dictionaries containing the hex asid, string jobname, and ASCB address.
            Obtained from `SELECT ALL` subcommand.
            Check See Also section for details.

        - **"storage_areas"** (list[dict])
            Info about dumped storage areas. Contains dataspace information.
            Obtained from `LISTDUMP` subcommand with `DSNAME` and `SELECT` parameters.
            Check See Also section for details.

    Methods
    -------
    __init__(session, dsname, ddir="", use_cur_ddir=False)
        Constructor for Dump Object.

    asid_to_jobname(asid)
        Get Jobname from ASID.

    jobname_to_asid(jobname)
        Get ASID from Jobname.

    asid_to_ascb_addr(asid)
        Get ASCB address from ASID.

    See Also
    --------
    data["asids_all"] : list[dicts]

        - **"asid"** (pyipcs.Hex)

        - **"jobname"** (str)

        - **"ascb_addr"** (pyipcs.Hex)

    data["storage_areas"] : list[dict]

        - **"asid"** (pyipcs.Hex)

        - **"total_bytes"** (pyipcs.Hex|None)
            Total number of bytes dumped for ASID in hex.

            None if total_bytes for ASID is not defined in 'LISTDUMP'.
        - **"sumdump"** (pyipcs.Hex)
            Number of SUMMARY DUMP Data bytes dumped in hex.

        - **"dataspaces"** (dict)
            Dictionary where the keys are the string dataspace names.
            Values are `Hex` objects containing the number of bytes dumped for dataspace.
    
    """

    def __init__(
        self,
        session: IpcsSession,
        dsname: str,
        ddir: str = "",
        use_cur_ddir: bool = False,
    ) -> None:
        """
        Constructor for Dump Object

        Sets regular or temporary DDIR for dump
        and parses out general info about dump from various subcommands.

        Initializes/Sets dump `dsname` under dump directory `ddir`.
        Will set IPCS `session` DDIR to `ddir`.
        Will set IPCS default `DSNAME` to `dsname`

        Parameters
        ----------
        session : pyipcs.IpcsSession
            IPCS Session.

        dsname : str
            Dump dataset name.

        ddir : str, optional
            Dump directory.
            If not specified, dump will be initialized under temporary DDIR
            which will be deleted on session close.

        use_cur_ddir : bool, optional
            Use current session DDIR.
            Will use the IpcsSession attribute `ddir` to initialize the dump under.
            This will take precedence over this function's `ddir` parameter.
            Default is `False`
        
        Returns
        -------
        None
        """
        # ==============================
        #  Type/Value Errors Check
        # ==============================

        if not isinstance(dsname, str):
            raise TypeError(
                f"Argument 'dsname' must be of type str, but got {type(dsname)}"
            )
        if not session.active:
            raise SessionNotActiveError()
        if not is_dump(dsname):
            raise ValueError(
                f"z/OS dataset '{dsname}' specified in argument 'dsname' is not a z/OS dump"
            )

        # ===========================
        # Specify Dump Dataset Name
        # ===========================

        self._dsname = dsname

        # ========================================
        # Create/Set Regular or Temporary DDIR
        # ========================================

        # If use_cur_ddir is True - Use the current pyIPCS session DDIR
        if use_cur_ddir:
            self._ddir = session.ddir.dsname
        else:
            # Define DDIR and create/set/initialize dump under DDIR
            if not ddir:
                self._ddir = session.create_session_ddir()
            # BLSCDDIR will not do anything if DDIR already exists so this is fine
            else:
                session.create_ddir(ddir)
                self._ddir = ddir

        # =========================
        # Initialize Setup
        # =========================

        # Set DDIR
        session.set_ddir(self.ddir)

        # Set default DSNAME
        session.set_defaults(dsname=self.dsname)

        # ==========================
        # Initialize Dump
        # ==========================

        # Run STATUS to start initialization
        Subcmd(session, "STATUS")

        # ======================================
        # Process dump header
        # ======================================

        self._header = DumpHeader(dsname)

        # ==================================================
        # Get Data about dump and store in .data attribute
        # ==================================================

        # Note: Any data not found will not be included in data
        self.data = {}

        # If the dump is a SLIP dump include LIST SLIPTRAP data
        if self.header["dump_type"] == "SLIP":
            list_sliptrap = ListSliptrap(session)
            if list_sliptrap.rc != 0:
                raise InvalidReturnCodeError(
                    list_sliptrap.subcmd, list_sliptrap.output, list_sliptrap.rc, 0
                )
            self.data["sliptrap"] = list_sliptrap.data["sliptrap"]

        # Include IPLDATA data
        self.data.update(Ipldata(session).data)

        # Include ASIDS Dumped if not a SAD, SYSM, or TDMP dump
        if self.header["dump_type"] not in ("SAD", "SYSM", "TDMP"):
            cbf_rtct = CbfRtct(session)
            if cbf_rtct.rc != 0:
                raise InvalidReturnCodeError(
                    cbf_rtct.subcmd, cbf_rtct.output, cbf_rtct.rc, 0
                )
            self.data["asids_dumped"] = cbf_rtct.data["asids_dumped"]
        # For SYSM/TDMP dumps the ASID dumped is the home asid
        if self.header["dump_type"] in ("SYSM", "TDMP"):
            self.data["asids_dumped"] = [self.data["home"]]

        # Get all ASIDs on the system at the time of the dump
        # Get their JOBNAMEs and ASCBADDRs
        select_all = SelectAll(session)
        if select_all.rc != 0:
            raise InvalidReturnCodeError(
                select_all.subcmd, select_all.output, select_all.rc, 0
            )
        self.data["asids_all"] = select_all.data["asids_all"]

        # Include LISTDUMP SELECT DSNAME data
        listdump_select_dsname = ListdumpSelectDsname(session, self.dsname)
        if listdump_select_dsname.rc != 0:
            raise InvalidReturnCodeError(
                listdump_select_dsname.subcmd,
                listdump_select_dsname.output,
                listdump_select_dsname.rc,
                0,
            )
        self.data["storage_areas"] = listdump_select_dsname.data["storage_areas"]

    def __pyipcs_json__(self) -> dict:
        """
        Convert Dump object for JSON format

        Returns
        -------
        dict
            Dictionary representing Dump object
            - **"dsname"** (str)
            - **"ddir"** (str)
            - **"header"** (dict)
            - **"data"** (dict)
        """
        return {
            "__ipcs_type__": "Dump",
            "dsname": copy.deepcopy(self.dsname),
            "ddir": copy.deepcopy(self.ddir),
            "header": copy.deepcopy(self.header),
            "data": copy.deepcopy(self.data),
        }

    def __str__(self) -> str:
        return f"Dump(dsname:\'{self.dsname}\', ddir:\'{self.ddir}\')"

    def __repr__(self) -> str:
        return (
            "Dump("
            + f"\n  dsname:\n    \'{self.dsname}\'"
            + f"\n  ddir:\n    \'{self.ddir}\'"
            + f"\n  header:\n{textwrap.indent(pformat(self.header), '    ')}"
            + f"\n  data:\n{textwrap.indent(pformat(self.data), '    ')}"
            + "\n)"
        )

    def asid_to_jobname(self, asid: Hex | str | int) -> str:
        """
        Get Jobname from ASID.

        Obtained info from `SELECT ALL` subcommand

        Parameters
        ----------
        asid : pyipcs.Hex|str|int

        Returns
        -------
        str|None 
            Jobname associated with ASID or `None` if ASID is not found
        """
        if (
            not isinstance(asid, Hex)
            and not isinstance(asid, str)
            and not isinstance(asid, int)
        ):
            raise TypeError(
                f"Argument 'asid' must be of type pyipcs.Hex or str or int, but got {type(asid)}"
            )
        if isinstance(asid, (int, str)):
            asid = Hex(asid)

        for asid_dict in self.data["asids_all"]:
            if asid_dict["asid"] == asid:
                return asid_dict["jobname"]
        return None

    def jobname_to_asid(self, jobname: str) -> Hex:
        """
        Get ASID from Jobname.

        Obtained info from `SELECT ALL` subcommand

        Parameters
        ----------
        jobname : str

        Returns
        --------
        list[pyipcs.Hex]
            List of ASIDs associated with `jobname`
        """
        if not isinstance(jobname, str):
            raise TypeError(
                f"Argument 'jobname' must be of type str, but got {type(jobname)}"
            )

        asid_list = []
        for asid_dict in self.data["asids_all"]:
            if asid_dict["jobname"] == jobname:
                asid_list.append(asid_dict["asid"])
        return asid_list

    def asid_to_ascb_addr(self, asid: Hex | str | int) -> str:
        """
        Get ASCB address from ASID.

        Obtained info from `SELECT ALL` subcommand

        Parameters
        ----------
        asid : pyipcs.Hex|str|int

        Returns
        -------
        pyipcs.Hex|None 
            ASCB address associated with ASID or `None` if ASID is not found
        """
        if (
            not isinstance(asid, Hex)
            and not isinstance(asid, str)
            and not isinstance(asid, int)
        ):
            raise TypeError(
                f"Argument 'asid' must be of type pyipcs.Hex or str or int, but got {type(asid)}"
            )
        if isinstance(asid, (int, str)):
            asid = Hex(asid)

        for asid_dict in self.data["asids_all"]:
            if asid_dict["asid"] == asid:
                return asid_dict["ascb_addr"]
        return None

    @property
    def dsname(self) -> str:
        """
        Attribute dsname
        """
        return self._dsname

    @property
    def ddir(self) -> str:
        """
        Attribute ddir
        """
        return self._ddir

    @property
    def header(self) -> str:
        """
        Attribute header
        """
        return self._header
