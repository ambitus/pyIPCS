"""
IpcsSession Object
"""

import os
import copy
import warnings
from datetime import datetime
from zoautil_py import datasets
from zoautil_py import exceptions
from ..hex_obj import Hex
from ..dump import Dump
from ..subcmd import Subcmd, SetDef
from ..pyipcs_logging import PyIPCSLogger
from ..error_handling import InvalidReturnCodeError, SessionNotActiveError
from .tso_cmd import tso_cmd, hrecall

from .exec_contents import IPCSRUN, PYIPEVAL


class IpcsSession:
    """
    IPCS Session Object

    Manages TSO allocations, temporary EXECs and DDIRs, and controls settings for IPCS Session.

    Attributes:
        userid (str):
            z/OS system userid for current user.
        hlq (str):
            High level qualifier used for temporary z/OS MVS datasets for pyIPCS EXECs and DDIRs.
        directory (str):
            File system directory where IPCS session directories and files will be placed.
            These include subcommand output files and other logs.
        active (bool):
            `True` if IPCS session is active, `False` if not active.
        ddir (str|None):
            DDIR that IPCS will use to run subcommands. `None` if session is not active.
        logger (pyipcs.PyIPCSLogger):
            Manages logging for the pyIPCS session.

    Methods:
    ```
        def __init__(
            hlq: str | None = None,
            directory: str | None = None,
            allocations: dict[str, str | list[str]] = {
                "IPCSPARM": ["SYS1.PARMLIB"],
                "SYSPROC": ["SYS1.SBLSCLI0"],
            },
        ) -> None:
            Constructor for pyIPCS IpcsSession Object.

        open() -> None:
            Opens IPCS/TSO Session.

        close() -> None:
            Closes IPCS/TSO Session.

        get_allocations() -> dict[str, str | list[str]]:
            Get allocations for your TSO environment.

        set_allocation(dd_name:str, specification:str|list[str]) -> None:
            Set a TSO allocation.

        update_allocations(
            new_allocations:dict[str,str|list[str]],
            clear_old_allocations:bool=True
        ) -> None:
            Update multiple TSO allocations.

        create_ddir(ddir: str) -> None:
            Create dump directory.

        create_temp_ddir() -> str:
            Create temporary dump directory. Will be deleted on session close.

        set_ddir(ddir: str) -> None:
            Set `ddir` as the current dump directory for the session.

        get_defaults() -> pyipcs.SetDef:
            Run SETDEF LIST to get IPCS defaults

        set_defaults(
            confirm: bool | None = None,
            dsname: str | None = None,
            nodsname: bool = False,
            asid: Hex | str | int | None = None,
            dspname: str | None = None,
            other: str | None = None,
        ) -> SetDef:
            Runs SETDEF with LIST parameter and other parameters to set IPCS defaults

        init_dump(dsname: str, ddir: str = "", use_cur_ddir: bool = False) -> Dump:
            Initialize/Set dump `dsname` under dump directory `ddir` and return Dump object.
            Will set IPCS session DDIR to `ddir`.
            Will set IPCS default DSNAME to `dsname`

        set_dump(dump: Dump) -> None:
            Set IPCS session DDIR to Dump object DDIR.
            Set IPCS default DSNAME to Dump object dataset name.

        dsname_in_ddir(dsname: str) -> bool:
            Check if dataset a source described in the current session DDIR.

        def evaluate(
            hex_address: Hex | str | int,
            dec_offset: int,
            dec_length: int,
        ) -> Hex:
            Read data from dump. Similar to EVALUATE subcommand in REXX.
    ```
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

        Args:
            hlq (str|None):
                Optional.
                High level qualifier used
                for temporary z/OS MVS datasets for pyIPCS EXECs and DDIRs.
                By default `None` is specified
                which will set the high level qualifier as your userid.
            directory (str|None):
                Optional.
                File system directory where IPCS session directories and files will be placed.
                By default `None` is specified
                which will set the directory as the current working directory of executed file.
            allocations (dict[str,str|list[str]]):
                Optional. Dictionary of allocations where keys are DD names
                and values are string data set allocation requests or lists of cataloged datasets.
                The default allocations are dataset SYS1.PARMLIB for DD name IPCSPARM
                and dataset SYS1.SBLSCLI0 for DD name SYSPROC.
        Returns:
            None
        """
        # ==============================
        #  Type Errors Check
        # ==============================

        if not isinstance(hlq, str) and not isinstance(hlq, type(None)):
            raise TypeError(f"Argument 'hlq' must be of type str, but got {type(hlq)}")
        if not isinstance(directory, str) and not isinstance(directory, type(None)):
            raise TypeError(
                f"Argument 'directory' must be of type str, but got {type(directory)}"
            )
        if not isinstance(allocations, dict):
            raise TypeError(
                f"Argument 'allocations' must be of type dict, but got {type(allocations)}\n"
            )

        # =================================================================================
        # Store values in private variables to prevent variable editing without mangling
        # =================================================================================

        # Attribute userid is managed by the property

        # Set attribute logger
        self.__logger = PyIPCSLogger()

        # Attribute hlq
        if hlq is None:
            self.__hlq = self.userid
        else:
            self.__hlq = hlq

        # Attribute directory
        if directory is None:
            self.__directory = os.getcwd()
        else:
            self.__directory = directory

        # Attribute active is managed by the property

        # Time that session was opened initially `None`
        # Either a string datetime or `None`
        # Will be used to determine whether the current session
        # At the hlq is the session for this object
        self.__time_opened = None

        # pyIPCS Temporary Datasets
        self.__temporary_active_dsname = f"{self.hlq}.PYIPCS.ACTIVE"
        self.__temporary_exec_dsname = f"{self.hlq}.PYIPCS.EXEC"
        self.__temporary_sysexec_dsname = f"{self.hlq}.PYIPCS.SYSEXEC"

        # Set allocations
        self.__allocations = {}
        self.update_allocations(allocations)

        # Set number of temporary DDIRs to 0
        self.__num_temp_ddirs = 0
        # Set current DDIR to None because session is not active
        self.__ddir = None

    def open(self) -> None:
        """
        Opens IPCS/TSO Session.

        Create pyIPCS temporary datasets necessary for pyIPCS operations.

        Returns:
            None
        """
        # Check session is not already opened
        if self.active:
            warnings.warn("Current IPCS session is already active/open", UserWarning)
            return

        # If there is already a session open at this hlq then throw an error
        if datasets.exists(self._temporary_active_dsname):
            raise RuntimeError(
                f"Another IPCS session is already active under high level qualifier '{self.hlq}'"
                + "\nEither close the other session or delete all pyIPCS temporary datasets"
                + " under this high level qualifier"
                + f"\nPattern for pyIPCS temporary datasets is '{self.hlq}.PYIPCS*'"
            )

        # Mark the time the session was opened
        self.__time_opened = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

        # Open logging
        self.logger._open_logging(self)

        # Create temporary datasets
        self.__create_temp_datasets()

        # Set the first dump directory to a temporary dump directory
        self.__ddir = self.create_temp_ddir()

    def close(self) -> None:
        """
        Closes IPCS/TSO Session.

        Deletes pyIPCS temporary EXECs and temporary DDIRs.

        Returns:
            None
        """
        # Check session is not already closed
        if not self.active:
            warnings.warn(
                "Current IPCS session is already not active/closed", UserWarning
            )
            return

        # Delete temporary dump directories
        self.__delete_temp_ddirs()

        # Delete temporary datasets
        self.__delete_temp_datasets()

        # Set _time_opened and ddir back to `None`
        self.__ddir = None
        self.__time_opened = None

        # Close logging
        self.logger._close_logging()

    def get_allocations(self) -> dict[str, str | list[str]]:
        """
        Get allocations for your TSO environment.

        Returns:
            dict[str,str|list[str]]: Returns dictionary of all allocations where keys are DD names
                and values are string data set allocation requests or lists of cataloged datasets
        """
        return self._allocations

    def set_allocation(self, dd_name: str, specification: str | list[str]) -> None:
        """
        Set a TSO allocation.

        If the specification is an empty list or empty string,
        will remove or not include DD name-specification pair within allocations

        Args:
            dd_name (str)
            specifications (str|list[str]):
                string data set allocation request or list of cataloged datasets
        Returns:
            None
        """
        if not isinstance(dd_name, str):
            raise TypeError(
                f"Argument 'dd_name' must be of type str, but got {type(dd_name)}\n"
            )

        if not isinstance(specification, str):
            if not isinstance(specification, list):
                raise TypeError(
                    f"Specification for {dd_name} "
                    + f"must be of type list or str, but got {type(specification)}\n"
                )
            if not all(isinstance(dsname, str) for dsname in specification):
                raise TypeError(
                    f"Specification for {dd_name} list items should all be of type str\n"
                )

        # Log Set Allocation
        self.logger.log(
            "SESSION",
            "SET ALLOCATION",
            extra={"dd_name": dd_name, "specification": copy.deepcopy(specification)},
        )

        # Create copy to pass list by value if type(specification) == list
        specification = copy.deepcopy(specification)
        self.__allocations[dd_name] = specification

        # If specification is empty remove DD name-specification pair from allocations
        if (
            isinstance(self.__allocations[dd_name], str)
            and self.__allocations[dd_name].strip() == ""
        ) or (
            isinstance(self.__allocations[dd_name], list)
            and self.__allocations[dd_name] == []
        ):
            del self.__allocations[dd_name]

    def update_allocations(
        self,
        new_allocations: dict[str, str | list[str]],
        clear_old_allocations: bool = True,
    ) -> None:
        """
        Update multiple TSO allocations.

        Args:
            new_allocations (dict[str,str|list[str]]):
                Dictionary of allocations where keys are DD names
                and values are string data set allocation requests or lists of cataloged datasets.
            clear_old_allocations (bool):
                Optional. If `True`, will clear all old allocations before setting new allocations.
                Default is `True`.
        Returns:
            None
        """
        if not isinstance(new_allocations, dict):
            raise TypeError(
                f"new_allocations must be of type dict, but got {type(new_allocations)}\n"
            )
        if not isinstance(clear_old_allocations, bool):
            raise TypeError(
                "clear_old_allocations "
                + f"must be of type bool, but got {type(clear_old_allocations)}\n"
            )

        if clear_old_allocations:
            self.__allocations = {}

        for dd_name, specification in new_allocations.items():
            self.set_allocation(dd_name, specification)

    def create_ddir(self, ddir: str) -> None:
        """
        Create dump directory.

        Args:
            ddir (str):
                Dump directory that will be created
        Returns:
            None
        """
        if not isinstance(ddir, str):
            raise TypeError(
                f"Argument 'ddir' must be of type str, but got {type(ddir)}"
            )

        # Log Create DDIR
        self.logger.log(
            "SESSION",
            "CREATE DDIR",
            extra={
                "ddir": ddir,
            },
        )

        # Run BLSCDDIR EXEC to create DDIR
        tso_cmd(f"%blscddir dsn({ddir})", allocations=self._allocations)

    def create_temp_ddir(self) -> str:
        """
        Create temporary dump directory. Will be deleted on session close.

        Returns:
            str: Temporary DDIR dataset name
        """
        if not self.active:
            raise SessionNotActiveError()
        temp_ddir = f"{self.hlq}.PYIPCS.TEMPDDIR.N{self.__num_temp_ddirs}.DDIR"
        self.create_ddir(temp_ddir)
        self.__num_temp_ddirs += 1
        return temp_ddir

    def set_ddir(self, ddir: str) -> None:
        """
        Set `ddir` as the current dump directory for the session.

        Args:
            ddir (str):
                Dump directory will be set as the sessions DDIR
        Returns:
            None
        """
        if not isinstance(ddir, str):
            raise TypeError(
                f"Argument 'ddir' must be of type str, but got {type(ddir)}"
            )
        if not self.active:
            raise SessionNotActiveError()
        # If the DDIR parameter is the same as the session's DDIR attribute - do nothing
        if self.ddir == ddir:
            return
        # Will return empty list if DDIR does not exist
        if not datasets.list_vsam_datasets(ddir):
            # If dataset does not exist check that it is not migrated
            hrecall(ddir, allocations=self._allocations)
            if not datasets.list_vsam_datasets(ddir):
                raise ValueError("Dump directory dataset 'ddir' does not exist")

        # Log Set DDIR
        self.logger.log(
            "SESSION",
            "SET DDIR",
            extra={
                "ddir": ddir,
            },
        )

        # If none of the previous conditions are met set the current ddir
        self.__ddir = ddir

    def get_defaults(self) -> SetDef:
        """
        Run `SETDEF LIST` to get IPCS defaults.

        Returns:
            pyipcs.SetDef : Custom `SETDEF` Subcmd Object.
                `outfile` parameter is set to `False` for string output.
        """
        setdef_obj = SetDef(self)
        if setdef_obj.rc != 0:
            raise InvalidReturnCodeError(
                setdef_obj.subcmd,
                setdef_obj.output,
                setdef_obj.rc,
                0,
            )
        return setdef_obj

    def set_defaults(
        self,
        confirm: bool | None = None,
        dsname: str | None = None,
        nodsname: bool = False,
        asid: Hex | str | int | None = None,
        dspname: str | None = None,
        other: str | None = None,
    ) -> SetDef:
        """
        Runs `SETDEF` with `LIST` parameter and other parameters to set IPCS defaults

        https://www.ibm.com/docs/en/zos/3.1.0?topic=subcommands-setdef-subcommand-set-defaults
        https://www.ibm.com/docs/en/zos/3.1.0?topic=parameter-address-processing-parameters

        Only Global Defaults impact the pyIPCS session.
        Args:
            confirm (bool|None):
                Optional.
                `True` for `CONFIRM` parameter.
                `False` for `NOCONFIRM` parameter.
                Default is `None` to not include parameter in subcommand.
            dsname (str|None):
                Optional.
                String dataset name to be used for `DSNAME` parameter.
                Default is `None` to not include parameter in subcommand.
            nodsname (bool):
                Optional.
                `True` for `NODSNAME` parameter.
                Default is `False` to not include parameter in subcommand.
            asid (pyipcs.Hex|str|int|None):
                Optional.
                pyipcs.Hex object or string or int to be used for `ASID` parameter.
                Default is `None` to not include parameter in subcommand.
            dspname (str|None):
                Optional.
                String dataspace name to be used for `DSPNAME` parameter.
                Default is `None` to not include parameter in subcommand.
            other (str|None):
                Optional.
                String of other parameters to include in `SETDEF`.
                Write other parameters as you would in regular IPCS (ex: `'ACTIVE LENGTH(4)'`).
                Default is `None` to not include in subcommand.
        Returns:
            pyipcs.SetDef : Custom `SETDEF` Subcmd Object.
                `outfile` parameter is set to `False` for string output.
        """
        setdef_obj = SetDef(
            self,
            confirm=confirm,
            dsname=dsname,
            nodsname=nodsname,
            asid=asid,
            dspname=dspname,
            other=other,
        )
        if setdef_obj.rc != 0:
            raise InvalidReturnCodeError(
                setdef_obj.subcmd,
                setdef_obj.output,
                setdef_obj.rc,
                0,
            )
        return setdef_obj

    def init_dump(
        self, dsname: str, ddir: str = "", use_cur_ddir: bool = False
    ) -> Dump:
        """
        Initialize/Set dump `dsname` under dump directory `ddir` and return Dump object.
        Will set IPCS session DDIR to `ddir`.
        Will set IPCS default `DSNAME` to `dsname`

        Args:
            dsname (str):
                Dump dataset name.
            ddir (str):
                Optional. Dump directory.
                If not specified, dump will be initialized under temporary DDIR.
            use_cur_ddir (bool):
                Optional. Use current session DDIR.
                Will use the IpcsSession attribute `ddir` to initialize the dump under.
                This will take precedence over this function's `ddir` parameter.
                Default is `False`.
        Returns:
            pyipcs.Dump
        """
        if not self.active:
            raise SessionNotActiveError()

        return Dump(self, dsname, ddir=ddir, use_cur_ddir=use_cur_ddir)

    def set_dump(self, dump: Dump) -> None:
        """
        Set IPCS session DDIR to Dump object DDIR.
        Set IPCS default `DSNAME` to Dump object dataset name.

        Args:
            dump (pyipcs.Dump)
        Returns:
            None
        """
        if not self.active:
            raise SessionNotActiveError()

        # Log Set Dump
        self.logger.log(
            "DUMP", "SET DUMP", extra={"dsname": dump.dsname, "ddir": dump.ddir}
        )

        # Set DDIR
        self.set_ddir(dump.ddir)

        # Check that dump is still initialized under DDIR
        if not self.dsname_in_ddir(dump.dsname):
            raise RuntimeError(
                f"Dump {dump.dsname} is not initialized under dump directory {dump.ddir}"
            )

        # Set default DSNAME
        self.set_defaults(dsname=dump.dsname)

        # Run STATUS to finish setup
        Subcmd(self, "STATUS")

    def dsname_in_ddir(self, dsname: str) -> bool:
        """
        Check if dataset is a source described in the current session DDIR.

        Used to check if a dump dataset was initialized under the current DDIR.

        Args:
            dsname (str):
                Dataset name.
        Returns:
            bool: `True` if dataset name a source described in the current DDIR, `False` if not.
        """
        if not isinstance(dsname, str):
            raise TypeError(
                f"Argument 'dsname' must be of type str, but got {type(dsname)}"
            )
        if not self.active:
            raise SessionNotActiveError()
        listdump = Subcmd(self, "LISTDUMP")
        if listdump.rc != 0:
            raise InvalidReturnCodeError(
                listdump.subcmd, listdump.output, listdump.rc, 0
            )
        return f"DSNAME('{dsname}')" in listdump.output

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

        Args:
            hex_address (pyipcs.Hex|str|int):
                Starting hex address to read from
            dec_offset (int):
                Byte offset from the starting address in decimal
            dec_length (int):
                Byte length of data to access in decimal
        Returns:
            pyipcs.Hex: Hex object representing the data at the specified address
        """
        if not self.active:
            raise SessionNotActiveError()

        if not isinstance(hex_address, (Hex, str, int)):
            raise TypeError(
                "Argument 'hex_address' "
                + f"must be of type pyipcs.Hex or str or int, but got {type(hex_address)}"
            )
        if not isinstance(dec_offset, int):
            raise TypeError(
                f"Argument 'dec_offset' must be of type int, but got {type(dec_offset)}"
            )
        if not isinstance(dec_length, int):
            raise TypeError(
                f"Argument 'dec_length' must be of type int, but got {type(dec_length)}"
            )

        pyipeval = Subcmd(self, f"PYIPEVAL {hex_address} {dec_offset} {dec_length}")

        if pyipeval.rc != 0:
            raise InvalidReturnCodeError(
                pyipeval.subcmd + " - pyIPCS Temporary EXEC",
                pyipeval.output,
                pyipeval.rc,
                0,
            )

        return Hex(pyipeval.output)

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
        if not datasets.exists(self._temporary_active_dsname):
            # Recall dataset just in case it is migrated
            hrecall(
                self._temporary_active_dsname,
                allocations=self._allocations,
            )
            if not datasets.exists(self._temporary_active_dsname):
                # If dataset still doesn't exist return False
                # If for some reason _time_opened is not None we have an error in this case
                if self._time_opened is not None:
                    raise RuntimeError(
                        "IpcsSession Python object indicates session is open"
                        + " but pyIPCS temporary datasets do not exist"
                    )
                return False
        # If _time_opened is `None` its a different session open
        if self._time_opened is None:
            return False
        # If _time_opened does not match we have an error
        if not datasets.read(self._temporary_active_dsname) == self._time_opened:
            raise RuntimeError(
                "IpcsSession Python object indicates session is open"
                + " but pyIPCS temporary datasets indicate they were opened by another session"
            )
        # Return True if previous conditions are not met
        return True

    @property
    def ddir(self) -> str | None:
        """
        Attribute ddir
        """
        return self.__ddir

    @property
    def logger(self) -> PyIPCSLogger:
        """
        Attribute logger
        """
        return self.__logger

    @property
    def _allocations(self) -> dict:
        """
        Protected Attribute _allocations
        """
        return self.__allocations

    @property
    def _time_opened(self) -> str | None:
        """
        Protected Attribute _time_opened

        Time that current instance of pyIPCS session was opened
        """
        return self.__time_opened

    @property
    def _temporary_active_dsname(self) -> str:
        """
        Protected Attribute _temporary_active_dsname

        Dataset that indicated pyIPCS session is open. Contains datetime to match _time_opened.
        """
        return self.__temporary_active_dsname

    @property
    def _temporary_exec_dsname(self) -> str:
        """
        Protected Attribute _temporary_exec_dsname

        Dataset to hold temporary EXECs that should not be in SYSEXEC.
        For example the EXEC that runs the IPCS Subcommands
        """
        return self.__temporary_exec_dsname

    @property
    def _temporary_sysexec_dsname(self) -> str:
        """
        Protected Attribute _temporary_sysexec_dsname

        Dataset to hold temporary EXECs that should be included in SYSEXEC.
        """
        return self.__temporary_sysexec_dsname

    @property
    def _ipcs_subcmd_exec_name(self) -> str:
        """
        Protected Attribute _ipcs_subcmd_exec_name

        Name for EXEC that runs IPCS subcommands
        """
        # return "IPCSCMD"
        return "IPCSRUN"

    @property
    def _evaluate_exec_name(self) -> str:
        """
        Protected Attribute _evaluate_exec_name

        Name for EXEC that runs evaluate
        """
        return "PYIPEVAL"

    @property
    def _session_directory_name(self) -> str:
        """
        Protected Attribute _session_directory_name

        Name for session directory
        """
        return "pyipcs_session"

    def _delete_ddir(self, ddir: str) -> None:
        """
        Protected Function _delete_ddir. Delete DDIR.

        Args:
            ddir (str) DDIR to delete.
        Returns:
            None
        """
        # ===============================================
        # Check if DDIR exists and if recall to be sure
        # ===============================================
        if not datasets.list_vsam_datasets(ddir):
            hrecall(ddir, allocations=self._allocations)

        # ==================================
        # If DDIR still exists delete
        # ==================================
        if datasets.list_vsam_datasets(ddir):
            tso_cmd(
                f"DELETE '{ddir}'",
                allocations={},
            )

    def __delete_temp_ddirs(self) -> None:
        """
        Private Function __delete_temp_ddirs. Delete all temporary DDIRs.

        Returns:
            None
        """
        for i in range(self.__num_temp_ddirs):
            self._delete_ddir(f"{self.hlq}.PYIPCS.TEMPDDIR.N{i}.DDIR")
        self.__num_temp_ddirs = 0

    def __create_temp_datasets(self) -> None:
        """
        Private Function __create_temp_datasets Create pyIPCS temporary datasets.

        Returns:
            None
        """
        try:
            # PYIPCS.ACTIVE
            datasets.write(self._temporary_active_dsname, content=self._time_opened)
            # PYIPCS.EXEC
            datasets.write(
                f"{self._temporary_exec_dsname}({self._ipcs_subcmd_exec_name})",
                # content=IPCSCMD,
                content=IPCSRUN,
            )
            # PYIPCS.SYSEXEC
            datasets.write(
                f"{self._temporary_sysexec_dsname}({self._evaluate_exec_name})",
                content=PYIPEVAL,
            )
        except exceptions.DatasetWriteException as e:
            raise RuntimeError(
                "Dataset Write Error - Creation Of pyIPCS Temporary Datasets\n"
                + f"\nReturn Code: {e.response.rc}\n"
                + f"\nSTDOUT:\n\n {e.response.stdout_response}\n"
                + f"\nSTDERR:\n\n {e.response.stderr_response}\n"
            ) from e

    def __delete_temp_datasets(self) -> None:
        """
        Private Function __delete_temp_datasets Delete pyIPCS temporary datasets.

        Returns:
            None
        """
        active_delete_rc = datasets.delete(self._temporary_active_dsname)
        exec_delete_rc = datasets.delete(self._temporary_exec_dsname)
        sysexec_delete_rc = datasets.delete(self._temporary_sysexec_dsname)

        # If a delete dataset error occurred display warning
        if active_delete_rc != 0 or sysexec_delete_rc != 0 or exec_delete_rc != 0:
            delete_error = (
                "Dataset Delete Error: Deletion Of pyIPCS Temporary Datasets\n"
            )
            if active_delete_rc != 0:
                delete_error += (
                    f"Delete {self._temporary_active_dsname}"
                    + f" Return Code: {active_delete_rc}\n"
                )
            if exec_delete_rc != 0:
                delete_error += (
                    f"Delete {self._temporary_exec_dsname}"
                    + f" Return Code: {exec_delete_rc}\n"
                )
            if sysexec_delete_rc != 0:
                delete_error += (
                    f"Delete {self._temporary_sysexec_dsname}"
                    + f" Return Code: {sysexec_delete_rc}\n"
                )
            warnings.warn(delete_error, UserWarning)

    def __del__(self) -> None:
        """
        Destructor for pyIPCS IpcsSession object. Closes IPCS/TSO session if active.

        Returns:
            None
        """
        if (
            hasattr(self, "_temporary_active_dsname")
            and hasattr(self, "_allocations")
            and hasattr(self, "_time_opened")
            and self.active
        ):
            self.close()
