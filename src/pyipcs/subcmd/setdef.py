"""
SetDef Custom Subcmd Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from ..hex_obj import Hex
from .subcmd import Subcmd

if TYPE_CHECKING:
    from ..session import IpcsSession


class SetDef(Subcmd):
    """
    SetDef Custom Subcmd Object

    Runs SETDEF with LIST parameter and other parameters

    https://www.ibm.com/docs/en/zos/3.1.0?topic=subcommands-setdef-subcommand-set-defaults
    https://www.ibm.com/docs/en/zos/3.1.0?topic=parameter-address-processing-parameters

    Can create a pyipcs.SetDef object using
    `pyipcs.IpcsSession.get_defaults()` and `pyipcs.IpcsSession.set_defaults()`.

    Only Global Defaults impact the pyIPCS session.

    Attributes:
        data (dict):
            Global Defaults.
            If Global Defaults are not found in the output the `data` dictionary will be empty.
        ```
            'confirm' (bool):
                `True` for parameter `CONFIRM`. `False` for parameter `NOCONFIRM`.
            'dsname' (str|None):
                String dataset name for parameter `DSNAME`. `None` for parameter `NODSNAME`.
            'asid' (pyipcs.Hex|None):
                pyipcs.Hex object for parameter `ASID`.
                `None` if parameter `ASID` is not included.
            'dspname' (str|None):
                String dataspace name for parameter `DSPNAME`.
                `None` if parameter `DSPNAME` is not included.
        ```

    Methods:
    ```
        __init__(
            session: IpcsSession,
            confirm: bool | None = None,
            dsname: str | None = None,
            nodsname: bool | None = None,
            asid: Hex | str | int | None = None,
            dspname: str | None = None,
            setdef_params: str | None = None,
            outfile: bool = False,
            keep_file: bool = False,
        ) -> None:
            Constructor for SetDef Custom Subcmd Object
    ```
    """

    def __init__(
        self,
        session: IpcsSession,
        confirm: bool | None = None,
        dsname: str | None = None,
        nodsname: bool = False,
        asid: Hex | str | int | None = None,
        dspname: str | None = None,
        setdef_params: str | None = None,
        outfile: bool = False,
        keep_file: bool = False,
    ) -> None:
        """
        Constructor for SetDef Custom Subcmd Object

        Args:
            session (pyipcs.IpcsSession)
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
            setdef_params (str|None):
                Optional.
                String of `SETDEF` parameters. 
                Write parameters as you would in regular IPCS (ex: `'ACTIVE LENGTH(4)'`). 
                Default is `None` to not include in subcommand.
            outfile (bool):
                Optional. If `True` stores output in file
                specified in `outfile` attribute of Subcmd object.
                If `False` stores output in string
                specified in `output` attribute of Subcmd object. Default is `False`.
            keep_file (bool):
                Optional. If `True` preserves subcommand output file after program execution.
                If `False` deletes subcommand output file after program execution.
                Default is `False`.
        Returns:
            None
        """
        # =============================
        # Construct SETDEF Subcommand
        # =============================
        setdef_subcmd = "SETDEF LIST"

        # =====================
        # CONFIRM NOCONFIRM
        # =====================
        if isinstance(confirm, bool) and confirm:
            setdef_subcmd += " CONFIRM"
        if isinstance(confirm, bool) and not confirm:
            setdef_subcmd += " NOCONFIRM"

        # ======================
        # DSNAME
        # ======================
        if isinstance(dsname, str):
            dsname = dsname.upper().strip()
            setdef_subcmd += f" DSN('{dsname}')"

        # =======================
        # NODSNAME
        # =======================
        if isinstance(nodsname, bool) and nodsname:
            setdef_subcmd += " NODSNAME"

        # =================
        # ASID
        # =================
        if isinstance(asid, (str, int)):
            setdef_subcmd += f" ASID(X'{Hex(asid)}')"
        if isinstance(asid, Hex):
            setdef_subcmd += f" ASID(X'{asid}')"

        # ====================
        # DSPNAME
        # ====================
        if isinstance(dspname, str):
            dspname = dspname.upper().strip()
            setdef_subcmd += f" DSPNAME({dspname})"

        # ===================
        # Other Parameters
        # ===================
        if isinstance(setdef_params, str):
            setdef_params = setdef_params.upper().strip()
            setdef_subcmd += f" {setdef_params}"

        # ========================
        # Run SETDEF Subcommand
        # ========================
        super().__init__(
            session,
            setdef_subcmd,
            outfile=outfile,
            keep_file=keep_file,
        )

        # =======================================
        # Parse Defaults and store in data dict
        # =======================================

        # =====================
        # CONFIRM NOCONFIRM
        # =====================
        def get_confirm_default(defaults_lines):
            if "NOCONFIRM" in defaults_lines[3]:
                return False
            return True

        # ======================
        # NODSNAME DSNAME
        # ======================
        def get_dsname_default(defaults_lines):
            if "DSNAME('" in defaults_lines[5]:
                return defaults_lines[5][
                    defaults_lines[5].find("DSNAME('")
                    + len("DSNAME('") : defaults_lines[5].find("')")
                ]
            return None

        # =================
        # ASID
        # =================
        def get_asid_default(defaults_lines):
            if "ASID(X'" in defaults_lines[-1]:
                return Hex(
                    defaults_lines[-1][
                        defaults_lines[-1].find("ASID(X'")
                        + len("ASID(X'") : defaults_lines[-1].find("')")
                    ]
                )
            return None

        # ====================
        # DSPNAME
        # ====================
        def get_dspname_default(defaults_lines):
            if "DSPNAME(" in defaults_lines[-1]:
                dspname_start = defaults_lines[-1].find("DSPNAME(") + len("DSPNAME(")
                return defaults_lines[-1][
                    dspname_start : defaults_lines[-1].find(")", dspname_start)
                ]
            return None

        # ======================================
        # Get index of Global Defaults
        # ======================================

        global_defaults_index = self.find(
            "/*--------------- Global Default Values for IPCS Subcommands ---------------*/"
        )

        local_defaults_index = self.find(
            "/*---------------- Local Default Values for IPCS Subcommands ---------------*/"
        )

        # ======================
        # Parse Global Defaults
        # ======================

        # Only include if global defaults are included
        if global_defaults_index != -1:

            if local_defaults_index == -1:
                global_defaults_lines = self[global_defaults_index:]
            else:
                global_defaults_lines = self[
                    global_defaults_index:local_defaults_index
                ].splitlines()[:-1]

            self.data["confirm"] = get_confirm_default(global_defaults_lines)
            self.data["dsname"] = get_dsname_default(global_defaults_lines)
            self.data["asid"] = get_asid_default(global_defaults_lines)
            self.data["dspname"] = get_dspname_default(global_defaults_lines)
