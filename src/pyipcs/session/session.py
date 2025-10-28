"""
IpcsSession Object
"""

import os
import atexit
import random
import warnings
from datetime import datetime
from pathlib import Path
from zoautil_py import datasets
from zoautil_py import exceptions
from ..hex_obj import Hex
from ..dump import Dump
from ..subcmd import Subcmd
from ..error_handling import InvalidReturnCodeError, SessionNotActiveError, ArgumentTypeError
from ..tso_shell import tsocmd
from ..util.zoautil_py_util import datasets_recall_exists
from .allocations import IpcsAllocations
from .ddir import DumpDirectory
from .dataset_content import IPCSRUN, IPCSEVAL, IPACTIVE

class IpcsSession:
    """
    IPCS Session Object

    Manages TSO allocations, session EXECs and DDIRs, and controls settings for IPCS Session.

    Attributes
    ----------
    userid : str
        z/OS system userid for current user.

    hlq : str
        High level qualifier where opened pyIPCS session is or will be under.
        pyIPCS session includes z/OS MVS datasets for pyIPCS EXECs and DDIRs.

    directory : str
        File system directory where IPCS session directories and files will be placed.
        These include subcommand output files and other logs.

    active : bool
        `True` if IPCS session is active, `False` if not active.

    aloc : pyipcs.IpcsAllocations
        Manages TSO allocations for your IPCS session.

    ddir : pyipcs.DumpDirectory
        Manages dump directory(DDIR) functionality for your IPCS session.

    uid : str | None
        Unique ID for open pyIPCS session. `None` if pyIPCS session is not active.

    hlq_full : str | None
        Full high level qualifier for open pyIPCS session. `None` if pyIPCS session is not active.

    directory_full : str | None
        Full directory where pyIPCS files for the open session will be placed.
        `None` if pyIPCS session is not active.
        
    Methods
    -------
    __init__(
        hlq=None, 
        directory=None, 
        allocations={
            "IPCSPARM": ["SYS1.PARMLIB"],
            "SYSPROC": ["SYS1.SBLSCLI0"],
        }
    )
        Constructor for pyIPCS IpcsSession Object.

    open()
        Opens IPCS/TSO Session.

    close()
        Closes IPCS/TSO Session.

    init_dump(dsname, ddir="", use_cur_ddir=False)
        Initialize/Set dump `dsname` under dump directory `ddir` and return Dump object.
        Will set IPCS session DDIR to `ddir`.
        Will set IPCS default DSNAME to `dsname`.

    set_dump(dump)
        Set IPCS session DDIR to Dump object DDIR.
        Set IPCS default DSNAME to Dump object dataset name.

    dsname_in_ddir(dsname)
        Check if dataset a source described in the current session DDIR.
        
    evaluate(hex_address, dec_offset, dec_length)
        Read data from dump. Similar to EVALUATE subcommand in REXX.
    """

    def __init__(
        self,
        hlq: str | None = None,
        directory: str | None = None,
        allocations: dict[str, str | list[str]] = {
            "IPCSPARM": ["SYS1.PARMLIB"],
            "SYSPROC": ["SYS1.SBLSCLI0"],
        },
    ) -> None:
        """
        Constructor for pyIPCS IpcsSession Object.

        Sets TSO initial allocations and set z/OS locations for pyIPCS temporary EXECs and DDIRs.

        Parameters
        ----------
        hlq : str|None, optional
            High level qualifier where opened pyIPCS session is or will be under.
            pyIPCS session includes z/OS MVS datasets for pyIPCS EXECs and DDIRs.
            High level qualifier has a max length of 16 characters excluding `"."`.
            By default is `None` which will set the high level qualifier as your userid.
        
        directory : str|None, optional
            File system directory where IPCS session directories and files will be placed.
            By default is `None`
            which will set the directory as the current working directory of executed file.
        
        allocations : dict[str,str|list[str]], optional
            Dictionary of allocations where keys are DD names
            and values are string data set allocation requests or lists of cataloged datasets.
            The default allocations are dataset SYS1.PARMLIB for DD name IPCSPARM
            and dataset SYS1.SBLSCLI0 for DD name SYSPROC.
        
        Returns
        -------
        None
        """
        # ID for opened session. Initially `None` when session is not open
        self.__uid = None
        # Time that session was opened. `None` when session is not open
        self.__time_opened = None
        # Setup cleanup
        atexit.register(self.__cleanup__)

        # ===========================
        # Argument Type Checking
        # ===========================

        if not isinstance(hlq, (str, type(None))):
            raise ArgumentTypeError("hlq", hlq, (str, type(None)))
        if not isinstance(directory, (str, type(None))):
            raise ArgumentTypeError("directory", directory, (str, type(None)))
        if not isinstance(allocations, dict):
            raise ArgumentTypeError("allocations", allocations, dict)

        # =================================================================================
        # Store values in private variables to prevent variable editing without mangling
        # =================================================================================

        # Attribute hlq
        self.__hlq = self.userid if hlq is None else hlq
        if len(self.hlq) > 16:
            raise ValueError(
                "Argument 'hlq' must have a length of 16 characters or less"
            )
        # Attribute directory
        self.__directory = os.getcwd() if directory is None else directory
        # Set initial allocations
        self._aloc = IpcsAllocations(allocations)
        # Set up DumpDirectory object
        self._ddir = DumpDirectory(self)

    def open(self) -> None:
        """
        Opens IPCS/TSO Session.

        Create pyIPCS temporary datasets necessary for pyIPCS operations.

        Returns
        -------
        None
        """
        # Check session is not already opened
        if self.active:
            warnings.warn("Current IPCS session is already active/open", UserWarning)
            return

        # Generate session id until you find one that does not exist
        # Session HLQ is dependent on the id
        self.__uid = "S" + "".join(random.choices("0123456789", k=5))
        while datasets_recall_exists(self.hlq_full):
            self.__uid = "S" + "".join(random.choices("0123456789", k=5))

        # Mark the time the session was opened
        self.__time_opened = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

        # Create Initial Session DDIR
        init_ddir = f"{self.hlq_full}.INIT.DDIR"
        self.ddir.create(init_ddir)
        # Create session datasets
        try:
            self.__create_session_datasets(init_ddir)
        except exceptions.DatasetWriteException:
            self.ddir._delete(init_ddir)
        # Set init ddir
        self.ddir.use(init_ddir)


    def close(self) -> None:
        """
        Closes IPCS/TSO Session.

        Deletes pyIPCS temporary EXECs and temporary DDIRs.

        Returns
        -------
        None
        """
        # Check session is not already closed
        if not self.active:
            warnings.warn(
                "Current IPCS session is already not active/closed", UserWarning
            )
            return

        # Delete temporary datasets
        self.__delete_session_datasets()

        # Set _time_opened, ddir, and id back to `None`
        self.ddir._clear()
        self.__time_opened = None
        self.__uid = None


    def init_dump(
        self, dsname: str, ddir: str = "", use_cur_ddir: bool = False
    ) -> Dump:
        """
        Initialize/Set dump `dsname` under dump directory `ddir` and return Dump object.

        Will set IPCS session DDIR to `ddir`.

        Will set IPCS default `DSNAME` to `dsname`

        Parameters
        ----------
        dsname : str
            Dump dataset name.
        
        ddir : str, optional
            Dump directory.
            If an empty string, dump will be initialized under temporary DDIR.

        use_cur_ddir : bool, optional
            Use current session DDIR.
            Will use the IpcsSession attribute `ddir` to initialize the dump under.
            This will take precedence over this function's `ddir` parameter.
            Default is `False`.
        
        Returns
        -------
        pyipcs.Dump
        """
        if not self.active:
            raise SessionNotActiveError()

        return Dump(self, dsname, ddir=ddir, use_cur_ddir=use_cur_ddir)

    def set_dump(self, dump: Dump) -> None:
        """
        Set IPCS session DDIR to Dump object DDIR.

        Set IPCS default `DSNAME` to Dump object dataset name.

        Parameters
        ----------
        dump : pyipcs.Dump
        
        Returns
        -------
        None
        """
        if not self.active:
            raise SessionNotActiveError()

        # Set DDIR
        self.ddir.use(dump.ddir)

        # Check that dump is still initialized under DDIR
        if dump.dsname not in self.ddir.sources():
            raise RuntimeError(
                f"Dump {dump.dsname} is not initialized under dump directory {dump.ddir}"
            )

        # Set default DSNAME
        self.ddir.defaults(dsname=dump.dsname)

        # Run STATUS to finish setup
        Subcmd(self, "STATUS")


    def evaluate(
        self,
        hex_address: Hex | str | int,
        dec_offset: int,
        dec_length: int,
    ) -> Hex:
        """
        Read data from dump. Similar to EVALUATE subcommand in REXX.

        Make sure to set correct defaults `DSNAME`, `ASID`, and `DSPNAME`
        prior to calling this method.

        https://www.ibm.com/docs/en/zos/3.1.0?topic=instruction-evaluate-subcommand

        Parameters
        ----------
        hex_address : pyipcs.Hex|str|int
            Starting hex address to read from.

        dec_offset : int
            Byte offset from the starting address in decimal.

        dec_length : int
            Byte length of data to access in decimal.
        
        Returns
        -------
        pyipcs.Hex
            Hex object representing the data at the specified address.
        """
        if not self.active:
            raise SessionNotActiveError()

        if not isinstance(hex_address, (Hex, str, int)):
            raise ArgumentTypeError("hex_address", hex_address, (Hex, str, int))
        if not isinstance(dec_offset, int):
            raise ArgumentTypeError("dec_offset", dec_offset, int)
        if not isinstance(dec_length, int):
            raise ArgumentTypeError("dec_length", dec_length, int)

        ipcseval = Subcmd(self, f"IPCSEVAL {hex_address} {dec_offset} {dec_length}")

        if ipcseval.rc != 0:
            raise InvalidReturnCodeError(
                ipcseval.subcmd + " - pyIPCS Temporary EXEC",
                ipcseval.output,
                ipcseval.rc,
                0,
            )

        return Hex(ipcseval.output)

    @property
    def userid(self) -> str:
        """
        Attribute userid
        """
        return datasets.get_hlq() if datasets.get_hlq() else os.getenv("USER", "TEMP")

    @property
    def hlq(self) -> str:
        """
        Attribute hlq
        """
        return self.__hlq

    @property
    def directory(self) -> str:
        """
        Attribute directory
        """
        return self.__directory

    @property
    def active(self) -> bool:
        """
        Attribute active
        """
        # If id and time opened are not set then the session is not active
        if self.uid is None and self._time_opened is None:
            return False
        # If only one is set the session is corrupted
        if self.uid is None:
            raise RuntimeError("Potential pyIPCS Session Corruption - Exiting")
        if self._time_opened is None:
            raise RuntimeError(
                "Potential pyIPCS Session Corruption"
                + f" - Please manually delete all datasets with the pattern '{self.hlq_full}*'"
            )
        # Check if IPACTIVE output matches intended output
        completed_tsocmd = tsocmd(
            f"ex \'{self._ipcsexec_execs['IPACTIVE']}\'",
            allocations={"IPCSEXEC": self._ipcsexec_dsname}
        )
        if (
            f"USERID: {self.userid}" in completed_tsocmd["output"]
            and f"TIME OPENED: {self._time_opened}" in completed_tsocmd["output"]
        ):
            return True
        # If output does not match session has become corrupted
        raise RuntimeError(
            "Potential pyIPCS Session Corruption"
            + f" - Please manually delete all datasets with the pattern '{self.hlq_full}*'"
        )

    @property
    def aloc(self) -> IpcsAllocations:
        """
        Attribute aloc
        """
        return self._aloc

    @property
    def ddir(self) -> DumpDirectory:
        """
        Attribute ddir
        """
        return self._ddir

    @property
    def uid(self) -> str|None:
        """
        Attribute uid
        """
        return self.__uid

    @property
    def hlq_full(self) -> str | None:
        """
        Attribute hlq_full
        """
        if not self.uid:
            return None
        return f"{self.hlq}.PYIPCS.{self.uid}"

    @property
    def directory_full(self) -> str | None:
        """
        Attribute directory_full
        """
        if not self.uid:
            return None
        directory_full_path = Path(self.directory) / "pyipcs_directory"
        directory_full_path = directory_full_path / f"{self.uid}.{self._time_opened}"
        return str(directory_full_path)

    @property
    def _time_opened(self) -> str | None:
        """
        Protected Attribute _time_opened

        Time that current instance of pyIPCS session was opened. `None` if session is not open.
        """
        return self.__time_opened

    @property
    def _ipcsexec_dsname(self) -> str:
        """
        Protected Attribute _ipcsexec_dsname

        Dataset name for dataset that contains pyIPCS IPCSEXEC execs
        """
        return f"{self.hlq_full}.IPCSEXEC"

    @property
    def _ipcsexec_execs(self) -> dict[str, str]:
        """
        Protected Attribute _ipcsexec_execs

        IPCSEXEC execs that map from exec name to the fully qualified member name
        """
        return {
            "IPACTIVE": f"{self._ipcsexec_dsname}(IPACTIVE)",
            "IPCSRUN": f"{self._ipcsexec_dsname}(IPCSRUN)",
        }

    @property
    def _sysexec_dsname(self) -> str:
        """
        Protected Attribute _sysexec_dsname

        Dataset name for dataset that contains pyIPCS SYSEXEC execs
        """
        return f"{self.hlq_full}.SYSEXEC"

    @property
    def _sysexec_execs(self) -> dict[str, str]:
        """
        Protected Attribute _sysexec_execs

        SYSEXEC execs that map from exec name to the fully qualified member name
        """
        return {
            "IPCSEVAL": f"{self._sysexec_dsname}(IPCSEVAL)"
        }

    def __create_session_datasets(self, init_ddir: str) -> None:
        """
        Private Function __create_session_datasets Create pyIPCS session datasets/execs.

        Parameters
        ----------
        init_ddir : str
            Initial DDIR for the pyIPCS session.

        Returns
        -------
        None
        """
        try:
            # Main Session Dataset
            # Write Initial DDIR to dataset
            datasets.create(self.hlq_full, dataset_type="SEQ")
            datasets.write(self.hlq_full, content=init_ddir)
            # All IPCSEXEC execs
            datasets.create(f"{self.hlq_full}.IPCSEXEC", dataset_type="PDSE")
            datasets.write(
                self._ipcsexec_execs["IPACTIVE"],
                content=IPACTIVE.format(
                    userid=self.userid,
                    time_opened=self._time_opened
                )
            )
            datasets.write(
                self._ipcsexec_execs["IPCSRUN"],
                content=IPCSRUN
            )
            # All SYSEXEC execs
            datasets.create(f"{self.hlq_full}.SYSEXEC", dataset_type="PDSE")
            datasets.write(
                self._sysexec_execs["IPCSEVAL"],
                content=IPCSEVAL
            )
        except exceptions.DatasetWriteException as e:
            raise RuntimeError(
                "Dataset Write Error - Creation Of IPCS Session Datasets\n"
                + f"\nReturn Code: {e.response.rc}\n"
                + f"\nSTDOUT:\n\n {e.response.stdout_response}\n"
                + f"\nSTDERR:\n\n {e.response.stderr_response}\n"
            ) from e

    def __delete_session_datasets(self) -> None:
        """
        Private Function __delete_temp_datasets Delete pyIPCS temporary datasets.

        Returns
        -------
        None
        """
        def delete_session_dataset(non_vsam_dsname: str) -> None:
            if not datasets_recall_exists(non_vsam_dsname):
                warnings.warn(
                    "Potential pyIPCS Session Corruption - Please manually delete all datasets"
                    + f" with the pattern '{self.hlq_full}*'",
                    UserWarning
                )
            rc = datasets.delete(non_vsam_dsname)
            if rc != 0:
                warnings.warn(
                    "Potential pyIPCS Session Corruption - Please manually delete all datasets"
                    + f" with the pattern '{self.hlq_full}*'",
                    UserWarning
                )

        def delete_ddir_session_dataset(ddir_dsname: str) -> None:
            if not datasets_recall_exists(ddir_dsname):
                warnings.warn(
                    "Potential pyIPCS Session Corruption - Please manually delete all datasets"
                    + f" with the pattern '{self.hlq_full}*'",
                    UserWarning
                )
            self.ddir._delete(ddir_dsname)
            if datasets_recall_exists(ddir_dsname):
                warnings.warn(
                    "Potential pyIPCS Session Corruption - Please manually delete all datasets"
                    + f" with the pattern '{self.hlq_full}*'",
                    UserWarning
                )

        # Delete all DDIRs in the main session dataset
        if datasets_recall_exists(self.hlq_full):
            try:
                ddirs = datasets.read(self.hlq_full).splitlines()
            except exceptions.DatasetFetchException:
                warnings.warn(
                    "Potential pyIPCS Session Corruption - Please manually delete all datasets"
                    + f" with the pattern '{self.hlq_full}*'",
                    UserWarning
                )
            for ddir in ddirs:
                delete_ddir_session_dataset(ddir.strip())
        else:
            warnings.warn(
                "Potential pyIPCS Session Corruption - Please manually delete all datasets"
                + f" with the pattern '{self.hlq_full}*'",
                UserWarning
            )
        delete_session_dataset(self._ipcsexec_dsname)
        delete_session_dataset(self._sysexec_dsname)
        delete_session_dataset(self.hlq_full)

    def __cleanup__(self) -> None:
        """
        Cleanup for pyIPCS session. Closes IPCS/TSO session if active.

        Returns
        -------
        None
        """
        if self.active:
            self.close()

    def __del__(self) -> None:
        """
        Destructor for pyIPCS IpcsSession object. Closes IPCS/TSO session if active.

        Returns
        -------
        None
        """
        self.__cleanup__()
