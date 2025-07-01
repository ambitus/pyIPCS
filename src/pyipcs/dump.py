"""
Dump Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import textwrap
from pprint import pformat
import copy
from .hex_obj import Hex
from .util import is_dump, dump_header_data
from .error_handling import (
    InvalidReturnCodeError,
    SessionNotActiveError,
)
from .subcmd import (
    Subcmd,
    ListSliptrap,
    ListdumpSelectDsname,
    CbfRtct,
    SelectAll,
    Ipldata,
)

if TYPE_CHECKING:
    from .session import IpcsSession


class Dump:
    """
    Dump Object

    Initializes a z/OS dump and stores general information.

    Can create a Dump object using `pyipcs.IpcsSession.init_dump()`

    Attributes:
        dsname (str):
            Dump dataset name.
        ddir (str|None):
            Dump directory when dump was initialized.
        data (dict):
            Dictionary containing general data about the dump.
            Editable by user to store additional info about a dump.
            **If Dump object cannot find or parse one of the `data` dictionary items below,
            the item will not be included in the `data` dictionary.**
        ```
                'dump_type' (str):
                    'SAD', 'SVCD', 'TDMP', 'SYSM', or 'SLIP'
                'sysname' (str)
                'date_local' (str)
                'time_local' (str)
                'title' (str)
                'original_dump_dsn' (str)
                'version' (int):
                    For example z/OS version `3` release `1`
                'release' (int):
                    For example z/OS version `3` release `1`
                'sdrsn' (str)
                'complete_dump' (bool)
                'home_jobname' (str):
                    Not included if 'dump_type'=='SAD'.
                'primary' (pyipcs.Hex):
                    Not included if 'dump_type'=='SAD'.
                'secondary' (pyipcs.Hex):
                    Not included if 'dump_type'=='SAD'.
                'home' (pyipcs.Hex):
                    Not included if 'dump_type'=='SAD'.
                'sdwa_asid' (pyipcs.Hex):
                    Not included if 'dump_type'=='SAD'.
                'sdwa_address' (pyipcs.Hex):
                    Not included if 'dump_type'=='SAD'.
                'blocks_allocated_decimal' (int):
                    Not included if 'dump_type'=='SAD'.
                'remote_sysname' (str):
                    Included only if 'remote_dump'==True.
                    Not included if 'dump_type'=='SAD'.
                'remote_dump' (bool):
                    Not included if 'dump_type'=='SAD'.
                'processor_serial_number' (str)
                'processor_model_number' (str)
                'sliptrap' (str):
                    Included in 'data' dictionary if 'dump_type'=='SLIP'.
                    Obtained from 'LIST SLIPTRAP' subcommand.
                'ipl_date_local' (str):
                    Included in 'data' dictionary if CSA is dumped.
                    Obtained from 'IPLDATA' subcommand.
                'ipl_time_local' (str):
                    Included in 'data' dictionary if CSA is dumped.
                    Obtained from 'IPLDATA' subcommand.
                'asids_dumped' (list[pyipcs.Hex]):
                    list of ASIDs that were dumped.
                    Obtained from 'CBF RTCT' subcommand.
                'asids_all' (list[dict]):
                    Info about all asids on the system at the time of the dump.
                    Keys are the hex ASIDs on the system and values are a dictionary
                    containing the string jobname and ASCB address.
                    Obtained from 'SELECT ALL' subcommand:
                        'asid' (pyipcs.Hex)
                        'jobname' (str)
                        'ascb_addr' (pyipcs.Hex)
                'storage_areas' (list[dict]):
                    Info about dumped storage areas.
                    Obtained from 'LISTDUMP' subcommand with parameters 'DSNAME' and 'SELECT':
                        'asid' (pyipcs.Hex)
                        'total_bytes' (pyipcs.Hex|None) :
                            Total number of bytes dumped for ASID in hex.
                            None if total_bytes for ASID is not defined in 'LISTDUMP'.
                        'sumdump' (pyipcs.Hex):
                            Number of SUMMARY DUMP Data bytes dumped in hex.
                        'dataspaces' (dict):
                            {
                                str(Dataspace Name) :
                                pyipcs.Hex(Number of bytes dumped for dataspace in hex)
                            }
        ```
    Methods:
    ```
        __init__(session:IpcsSession, dsname:str, ddir:str="") -> None:
            Constructor for Dump Object.

        asid_to_jobname(asid:Hex|str|int) -> str|None:
            Get Jobname from ASID.

        jobname_to_asid(jobname:str) -> pyipcs.Hex|None:
            Get ASID from Jobname.

        asid_to_ascb_addr(asid:Hex|str|int) -> pyipcs.Hex|None:
            Get ASCB address from ASID.
    ```
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
        and parses out general info about dump from various subcommands

        Initializes/Sets dump `dsname` under dump directory `ddir`.
        Will set IPCS `session` DDIR to `ddir`.
        Will set IPCS default `DSNAME` to `dsname`

        Args:
            session (pyipcs.IpcsSession):
                IPCS Session.
            dsname (str):
                Dump dataset name.
            ddir (str):
                Optional. Dump directory.
                If not specified, dump will be initialized under temporary DDIR
                which will be deleted on session close.
            use_cur_ddir (bool):
                Optional. Use current session DDIR.
                Will use the IpcsSession attribute `ddir` to initialize the dump under.
                This will take precedence over this function's `ddir` parameter.
                Default is `False`
        Returns:
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

        self.__dsname = dsname

        # ========================================
        # Create/Set Regular or Temporary DDIR
        # ========================================

        # If use_cur_ddir is True - Use the current pyIPCS session DDIR
        if use_cur_ddir:
            self.__ddir = session.ddir
        else:
            # Define DDIR and create/set/initialize dump under DDIR
            if not ddir:
                self.__ddir = session.create_temp_ddir()
            # BLSCDDIR will not do anything if DDIR already exists so this is fine
            else:
                session.create_ddir(ddir)
                self.__ddir = ddir

        # =========================
        # Initialize Setup
        # =========================

        # Set DDIR
        session.set_ddir(self.ddir)

        # Set default DSNAME
        session.set_defaults(dsname=self.dsname)

        # =================================
        # Log Start Initialize Dump
        # =================================

        session.logger.log(
            "DUMP",
            "START INITIALIZE DUMP",
            extra={"dsname": self.dsname, "ddir": self.ddir},
        )

        # ==========================
        # Initialize Dump
        # ==========================

        # Run STATUS to start initialization
        Subcmd(session, "STATUS")

        # ============================
        # Log Finish Initialize Dump
        # ============================

        session.logger.log(
            "DUMP",
            "FINISH INITIALIZE DUMP",
            extra={"dsname": self.dsname, "ddir": self.ddir},
        )

        # ==================================================
        # Get Data about dump and store in .data attribute
        # ==================================================

        # Note: Any data not found will not be included in data
        self.data = {}

        # Add data from dump header
        self.data.update(dump_header_data(dsname))

        # ===========================================
        # Log Start Running Dump Object Subcommands
        # ===========================================

        session.logger.log(
            "DUMP",
            "RUNNING DUMP OBJECT SUBCMDS",
            extra={"dsname": self.dsname, "ddir": self.ddir},
        )

        # If the dump is a SLIP dump include LIST SLIPTRAP data
        if self.data["dump_type"] == "SLIP":
            list_sliptrap = ListSliptrap(session)
            if list_sliptrap.rc != 0:
                raise InvalidReturnCodeError(
                    list_sliptrap.subcmd, list_sliptrap.output, list_sliptrap.rc, 0
                )
            self.data["sliptrap"] = list_sliptrap.data["sliptrap"]

        # Include IPLDATA data
        self.data.update(Ipldata(session).data)

        # Include ASIDS Dumped if not a SAD, SYSM, or TDMP dump
        if self.data["dump_type"] not in ("SAD", "SYSM", "TDMP"):
            cbf_rtct = CbfRtct(session)
            if cbf_rtct.rc != 0:
                raise InvalidReturnCodeError(
                    cbf_rtct.subcmd, cbf_rtct.output, cbf_rtct.rc, 0
                )
            self.data["asids_dumped"] = cbf_rtct.data["asids_dumped"]
        # For SYSM/TDMP dumps the ASID dumped is the home asid
        if self.data["dump_type"] in ("SYSM", "TDMP"):
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

        session.logger.log(
            "DUMP",
            "CREATED DUMP OBJECT",
            extra={"dsname": self.dsname, "ddir": self.ddir},
        )

    def __pyipcs_json__(self) -> dict:
        """
        Convert Dump object for JSON format

        Returns:
            dict: Dictionary representing Dump object
            ```
                'dsname' (str)
                'ddir' (str)
                'data' (dict)
            ```
        """
        return {
            "dsname": copy.deepcopy(self.dsname),
            "ddir": copy.deepcopy(self.ddir),
            "data": copy.deepcopy(self.data),
        }

    def __str__(self) -> str:
        return f"Dump(dsname:'{self.dsname}', ddir:'{self.ddir}')"

    def __repr__(self) -> str:
        return (
            "Dump("
            + f"\n  dsname:\n    '{self.dsname}'"
            + f"\n  ddir:\n    '{self.ddir}'"
            + f"\n  data:\n{textwrap.indent(pformat(self.data), '    ')}"
            + "\n)"
        )

    def asid_to_jobname(self, asid: Hex | str | int) -> str:
        """
        Get Jobname from ASID.

        Obtained info from `SELECT ALL` subcommand

        Args:
            asid (pyipcs.Hex|str|int)
        Returns:
            str|None : Jobname associated with ASID or `None` if ASID is not found
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

        Args:
            jobname (str)
        Returns:
            list[pyipcs.Hex]: List of ASIDs associated with `jobname`
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

        Args:
            asid (pyipcs.Hex|str|int)
        Returns:
            pyipcs.Hex|None : ASCB address associated with ASID or `None` if ASID is not found
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
        return self.__dsname

    @property
    def ddir(self) -> str:
        """
        Attribute ddir
        """
        return self.__ddir
