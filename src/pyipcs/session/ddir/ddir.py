"""
DumpDirectory Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import random
import copy
from zoautil_py import datasets, exceptions
from ...tso_shell import tsocmd
from ...error_handling import InvalidReturnCodeError, SessionNotActiveError, ArgumentTypeError
from ...util.zoautil_py_util import datasets_recall_exists
from .setdef import SetDef

if TYPE_CHECKING:
    from ..session import IpcsSession

class DumpDirectory:
    """
    Dump Directory Object
    
    Manages dump directory(DDIR) for IPCS Session

    Attributes
    ----------
    dsname : str|None
        Dataset name of dump directory for your IPCS session. 
        `None` if dump directory is not set.
    
    Methods
    -------
    __init__()
        Constructor for pyIPCS DumpDirectory Object.

    use(dsname)
        Use a different dump directory as your current dump directory for your IPCS session.

    create(dsname, use=True, **kwargs)
        Create dump directory.

    create_tmp(use=True, **kwargs)
        Create temporary dump directory. Will be deleted on IPCS session close.

    presets(**kwargs)
        Presets for dump directory creation.

    defaults(**kwargs)
        Get/Set default values for certain parameters on IPCS subcommands for your IPCS session.
    """

    # Dictionary of all possible DDIR presets from BLSCDDIR params and their types
    _BLSCDDIR_PARAMS = {
        "dataclas": str,
        "mgmtclas": str,
        "ndxcisz": int,
        "records": int,
        "storclas": str,
        "volume": str,
    }

    def __init__(self, session: IpcsSession) -> None:
        """
        Constructor for pyIPCS DumpDirectory Object.

        Parameters
        ----------
        session : pyipcs.IpcsSession

        Returns
        -------
        None
        """
        # Set pyIPCS session
        self._session = session
        # Set initial dump directory to None
        self._dsname = None
        # Empty dictionary for no blscddir presets
        self._presets = {}

    def use(self, dsname: str) -> None:
        """
        Use a different dump directory as your current dump directory for your IPCS session.

        The dump directory must exist and the IPCS session must be active.

        Parameters
        ----------
        dsname : str
            Dump directory will be set as the session's DDIR.

        Returns
        -------
        None
        """
        if not isinstance(dsname, str):
            raise ArgumentTypeError("dsname", dsname, str)
        if not self._session.active:
            raise SessionNotActiveError()
        # If the dsname parameter is the same as the session's dsname attribute - do nothing
        if self.dsname == dsname:
            return
        # Will return False if DDIR does not exist
        if not datasets_recall_exists(dsname):
            raise ValueError("Dump directory dataset 'dsname' does not exist")

        # If none of the previous conditions are met set the current ddir
        self._dsname = dsname

    def create(self, dsname: str, **kwargs) -> None:
        """
        Create dump directory. 
        
        Uses `BLSCDDIR` CLIST to create DDIR.
        Adding additional keyword arguments will override pyIPCS DDIR presets.

        https://www.ibm.com/docs/en/zos/3.1.0?topic=execs-blscddir-clist-create-dump-directory

        Parameters
        ----------
        dsname : str
            Dump directory that will be created.

        kwargs: dict, optional
            Additional parameters (see other parameters)

        Other Parameters
        ----------------
        dataclas : str, optional

        mgmtclas : str, optional

        ndxcisz : int, optional

        records : int, optional

        storclas : str, optional

        volume : str, optional

        blscddir_params : str, optional
            String of `BLSCDDIR` parameters.
            Write parameters as you would in regular IPCS (ex: `'NDXCISZ(4096)'`).

        Returns
        -------
        None
        """

        # BLSCDDIR standard TSO Command
        blscddir_cmd = f"%BLSCDDIR DSNAME({dsname})"

        # ===================================================================
        # Convert keyword args to BLSCDDIR params
        # Use keyword args provided otherwise use preset if it exists
        # ===================================================================

        # Combine kwargs and existing presets
        for param, value in self._presets.items():
            if param not in kwargs:
                kwargs[param] = value

        # Add parameters to BLSCDDIR command
        for param, value in kwargs.items():
            if param in self._BLSCDDIR_PARAMS:
                if not isinstance(value, self._BLSCDDIR_PARAMS[param]):
                    raise ArgumentTypeError(param, value, self._BLSCDDIR_PARAMS[param])
                blscddir_cmd += f" {param}({value})"
            elif param == "blscddir_params":
                if not isinstance(value, str):
                    raise ArgumentTypeError(param, value, str)
                blscddir_cmd += f" {value}"
            else:
                raise ValueError(f"Invalid DDIR preset {param}")

        # Run BLSCDDIR EXEC to create DDIR
        tsocmd(blscddir_cmd, allocations=self._session.aloc.get())


    def create_tmp(self, **kwargs) -> str:
        """
        Create temporary dump directory. Will be deleted on IPCS session close.

        Uses `BLSCDDIR` CLIST to create DDIR.
        Adding additional keyword arguments will override pyIPCS DDIR presets.

        https://www.ibm.com/docs/en/zos/3.1.0?topic=execs-blscddir-clist-create-dump-directory

        Parameters
        ----------
        kwargs: dict, optional
            Additional parameters (see other parameters)

        Other Parameters
        ----------------
        dataclas : str, optional

        mgmtclas : str, optional

        ndxcisz : int, optional

        records : int, optional

        storclas : str, optional

        volume : str, optional

        blscddir_params : str, optional
            String of `BLSCDDIR` parameters.
            Write parameters as you would in regular IPCS (ex: `'NDXCISZ(4096)'`).

        Returns
        -------
        str
            pyIPCS temporary DDIR dataset name
        """
        if not self._session.active:
            raise SessionNotActiveError()

        # Generate a DDIR with a DDIR id until one that does not exist is found
        ddir_id = "".join(random.choices("0123456789", k=5))
        tmp_ddir = f"{self._session.hlq_full}.D{ddir_id}.DDIR"
        while datasets_recall_exists(tmp_ddir):
            ddir_id = "".join(random.choices("0123456789", k=5))
            tmp_ddir = f"{self._session.hlq_full}.D{ddir_id}.DDIR"

        # Create the DDIR
        self.create(tmp_ddir, **kwargs)

        # Attempt to add DDIR to main session dataset for tracking
        datasets_recall_exists(self._session.hlq_full)
        try:
            datasets.write(self._session.hlq_full, content=tmp_ddir, append=True)
        except exceptions.DatasetWriteException as e:
            self._delete(tmp_ddir)
            raise RuntimeError(
                "Dataset Write Error - Tracking pyIPCS Session DDIR\n"
                + f"\nReturn Code: {e.response.rc}\n"
                + f"\nSTDOUT:\n\n {e.response.stdout_response}\n"
                + f"\nSTDERR:\n\n {e.response.stderr_response}\n"
            ) from e

        return tmp_ddir


    def presets(self, **kwargs) -> dict:
        """
        Presets for dump directory creation.

        Parameters that will be added to BLSCDDIR for pyIPCS dump directory creation.
        Input optional parameters to change presets.

        https://www.ibm.com/docs/en/zos/3.1.0?topic=execs-blscddir-clist-create-dump-directory
        
        Parameters
        ----------
        kwargs: dict, optional
            Additional parameters (see other parameters)

        Other Parameters
        ----------------
        dataclas : str, optional
            Specifies the data class for the new directory. 
            If you omit this parameter, there is no data class specified for the new directory.

        mgmtclas : str, optional
            Specifies the management class for the new directory. 
            If you omit this parameter, 
            there is no management class specified for the new directory.

        ndxcisz : int, optional
            Specifies the control interval size for the index portion of the new directory. 
            If you omit this parameter, the IBM-supplied default is 4096 bytes.

        records : int, optional
            Specifies the number of records you want the directory to accommodate. 
            If you omit this parameter, the IBM-supplied default is 5000; 
            your installation's default might vary.

        storclas : str, optional
            Specifies the storage class for the new directory. 
            If you omit this parameter, 
            there is no storage class specified for the new directory.

        volume : str, optional
            Specifies the VSAM volume on which the directory should reside. 
            If you omit DATACLAS, MGMTCLAS, STORCLAS, and VOLUME, 
            the IBM-supplied default is VSAM01. 
            Otherwise, there is no IBM-supplied default.

        blscddir_params : str, optional
            String of `BLSCDDIR` parameters.
            Write parameters as you would in regular IPCS (ex: `'NDXCISZ(4096)'`).
    
        Returns
        -------
        dict
            DDIR presets for dump creation for your IPCS session.
            Returned dictionary could contain the following presets as key-value pairs.
            - 'dataclas' (str)
            - 'mgmtclas' (str)
            - 'ndxcisz' (int)
            - 'records' (int)
            - 'storclas' (str)
            - 'volume' (str)
            - 'blscddir_params' (str)
        """
        # Add to presets if keyword argument was added
        for param, value in kwargs.items():
            if param in self._BLSCDDIR_PARAMS:
                if not isinstance(value, self._BLSCDDIR_PARAMS[param]):
                    raise ArgumentTypeError(param, value, self._BLSCDDIR_PARAMS[param])
                self._presets[param] = value
            elif param == "blscddir_params":
                if not isinstance(value, str):
                    raise ArgumentTypeError(param, value, str)
                self._presets[param] = value
            else:
                raise ValueError(f"Invalid DDIR preset {param}")
        # Return copy of presets to user
        return copy.deepcopy(self._presets)


    def defaults(self, **kwargs) -> SetDef:
        """
        Get/Set default values for certain parameters on IPCS subcommands for your IPCS session.
        Uses the `SETDEF LIST` IPCS subcommand.

        IPCS uses the new default value for both your current session 
        and any subsequent sessions in which you use the same user dump directory,
        until you change the value.
        
        Note that pyIPCS only sets global defaults.

        https://www.ibm.com/docs/en/zos/3.1.0?topic=subcommands-setdef-subcommand-set-defaults

        Parameters
        ----------
        kwargs: dict, optional
            Additional parameters (see other parameters)

        Other Parameters
        ----------------
        confirm : bool, optional
            `True` for `CONFIRM` parameter. `False` for `NOCONFIRM` parameter.

        dsname : str|None, optional
            String dataset name to be used for `DSNAME` parameter. `None` for `NODSNAME` parameter.

        asid : pyipcs.Hex|str|int, optional
            pyipcs.Hex object or string or int to be used for `ASID` parameter.

        dspname : str, optional
            String dataspace name to be used for `DSPNAME` parameter.
            
        setdef_params : str, optional
            String of `SETDEF` parameters. 
            Write parameters as you would in regular IPCS (ex: `'ACTIVE LENGTH(4)'`).
        
        Returns
        -------
        pyipcs.SetDef
            Custom `SETDEF` Subcmd Object.
        """
        setdef_obj = SetDef(self._session, **kwargs)
        if setdef_obj.rc != 0:
            raise InvalidReturnCodeError(
                setdef_obj.subcmd,
                setdef_obj.output,
                setdef_obj.rc,
                0
            )
        return setdef_obj

    @property
    def dsname(self) -> str|None:
        """
        Attribute dsname
        """
        return self._dsname

    def _delete(self, dsname : str) -> None:
        """
        Protected Function.

        Delete DDIR.

        Returns
        -------
        None
        """
        # If DDIR still exists delete
        if datasets_recall_exists(dsname):
            tsocmd(
                f"DELETE '{dsname}'",
                allocations={"IPCSALOC": dsname},
            )

    def _clear(self) -> None:
        """
        Protected Function.

        Clears the currently used DDIR and sets it to None on IPCS session close.

        Returns
        -------
        None
        """
        self._dsname = None
