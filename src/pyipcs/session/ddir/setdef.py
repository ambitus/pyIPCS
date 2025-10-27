# pylint: disable=too-many-branches
"""
SetDef Custom Subcmd Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from ...hex_obj import Hex
from ...subcmd.subcmd import Subcmd
from ...error_handling import ArgumentTypeError

if TYPE_CHECKING:
    from .. import IpcsSession


class SetDef(Subcmd):
    """
    SetDef Custom Subcmd Object

    Runs `SETDEF` with `LIST` parameter and other parameters

    https://www.ibm.com/docs/en/zos/3.1.0?topic=subcommands-setdef-subcommand-set-defaults
    https://www.ibm.com/docs/en/zos/3.1.0?topic=parameter-address-processing-parameters

    Only Global Defaults impact the pyIPCS session.

    Attributes
    ----------
    data : dict
        Global Defaults.
        Keys may not appear if information is unknown or unavailable.

        - **"confirm"** (bool)
            `True` for `CONFIRM`. `False` for `NOCONFIRM`.

        - **"dsname"** (str|None)
            String dataset name for parameter `DSNAME`. `None` for `NODSNAME`.

        - **"display"** (list[str]|None)
            List of sub parameters for `DISPLAY` parameter.
            `None` if `DISPLAY` is not in output.
            Possible values in the list can include
            `"MACHINE"`, `"REMARK"`, `"REQUEST"`, `"STORAGE"`, `"SYMBOL"`, `"ALIGN"`,
            `"NOMACHINE"`, `"NOREMARK"`, `"NOREQUEST"`, `"NOSTORAGE"`, `"NOSYMBOL"`, `"NOALIGN"`.

        - **"flag"** (str|None)
            String severity for parameter `FLAG`.
            `None` if `FLAG` is not in output.
            Possible string options include
            `"ERROR"`, `"INFORMATIONAL"`, `"SERIOUS"|"SEVERE"`, `"TERMINATING"`, `"WARNING"`.

        - **"length"** (pyipcs.Hex|None)
            pyipcs.Hex object for parameter `LENGTH`.
            `None` if `LENGTH` is not in output.

        - **"pds"** (bool)
            `True` for `PDS`. `False` for `NOPDS`.

        - **"asid"** (pyipcs.Hex|None)
            pyipcs.Hex object for parameter `ASID`.
            `None` if `ASID` is not in output.

        - **"dspname"** (str|None)
            String dataspace name for parameter `DSPNAME`.
            `None` if `DSPNAME` is not in output.

    Methods
    -------
    __init__(session, outfile=False, keep_file=False, **kwargs)
        Constructor for SetDef Custom Subcmd Object.

    """

    def __init__(
        self,
        session: IpcsSession,
        outfile: bool = False,
        keep_file: bool = False,
        **kwargs,
    ) -> None:
        """
        Constructor for SetDef Custom Subcmd Object.

        Parameters
        ----------
        session : pyipcs.IpcsSession

        outfile : bool, optional
            Default is `False`.

        keep_file : bool, optional
            Default is `False`.

        kwargs: dict, optional
            Additional parameters (see other parameters)

        Other Parameters
        ----------------
        confirm : bool, optional
            `True` for `CONFIRM` parameter. `False` for `NOCONFIRM` parameter.

        dsname : str|None, optional
            String dataset name to be used for `DSNAME` parameter. `None` for `NODSNAME` parameter.

        display : list[str], optional
            List of sub parameters to be used for `DISPLAY` parameter.
            Possible values in the list can include
            `"MACHINE"`, `"REMARK"`, `"REQUEST"`, `"STORAGE"`, `"SYMBOL"`, `"ALIGN"`,
            `"NOMACHINE"`, `"NOREMARK"`, `"NOREQUEST"`, `"NOSTORAGE"`, `"NOSYMBOL"`, `"NOALIGN"`.

        flag : str, optional
            String severity to be used for `FLAG` parameter.
            Possible string options include `ERROR`, `INFORMATIONAL`, `SERIOUS`|`SEVERE`,
            `TERMINATING`, `WARNING`.

        length : pyipcs.Hex|str|int, optional
            pyipcs.Hex object or string or int to be used for `LENGTH` parameter.

        pds : bool, optional
            `True` for `PDS` parameter. `False` for `NOPDS` parameter.

        asid : pyipcs.Hex|str|int, optional
            pyipcs.Hex object or string or int to be used for `ASID` parameter.

        dspname : str, optional
            String dataspace name to be used for `DSPNAME` parameter.

        setdef_params : str, optional
            String of `SETDEF` parameters.
            Write parameters as you would in regular IPCS (ex: `"ACTIVE LENGTH(4)"`).

        Returns
        -------
        None
        """
        # ===================================================
        # Check kwargs contains correct keyword arguments
        # ===================================================
        for key in kwargs:
            if key not in [
                "confirm",
                "dsname",
                "display",
                "flag",
                "length",
                "pds",
                "asid",
                "dspname",
                "setdef_params",
            ]:
                raise ValueError(f"Invalid SETDEF argument '{key}'")

        # =============================
        # Construct SETDEF Subcommand
        # =============================

        setdef_subcmd = "SETDEF LIST"

        # =====================
        # CONFIRM NOCONFIRM
        # =====================

        if "confirm" in kwargs:
            if not isinstance(kwargs["confirm"], bool):
                raise ArgumentTypeError("confirm", kwargs["confirm"], bool)
            if kwargs["confirm"]:
                setdef_subcmd += " CONFIRM"
            else:
                setdef_subcmd += " NOCONFIRM"

        # ======================
        # DSNAME/NODSNAME
        # ======================

        if "dsname" in kwargs:
            if not isinstance(kwargs["dsname"], (str, type(None))):
                raise ArgumentTypeError("dsname", kwargs["dsname"], (str, None))
            if kwargs["dsname"] is None:
                setdef_subcmd += " NODSNAME"
            else:
                setdef_subcmd += f" DSNAME('{kwargs['dsname']}')"

        # ======================
        # DISPLAY
        # ======================

        if "display" in kwargs:
            if not isinstance(kwargs["display"], list) or not all(
                isinstance(sub_parameter, str) for sub_parameter in kwargs["display"]
            ):
                raise ArgumentTypeError("display", kwargs["display"], (list[str]))
            if not all(
                sub_parameter.upper()
                in [
                    "MACHINE", "REMARK", "REQUEST", "STORAGE", "SYMBOL", "ALIGN",
                    "NOMACHINE", "NOREMARK", "NOREQUEST", "NOSTORAGE", "NOSYMBOL", "NOALIGN"
                ]
                for sub_parameter in kwargs["display"]
            ):
                raise ValueError(
                    f"{kwargs["display"]} is not a valid DISPLAY parameter."
                    + " Valid display dictionary keys are:"
                    + " 'MACHINE','REMARK','REQUEST','STORAGE','SYMBOL', 'ALIGN',"
                    + " 'NOMACHINE','NOREMARK','NOREQUEST','NOSTORAGE','NOSYMBOL', 'NOALIGN',"
                )
            # If not empty list
            if kwargs["display"]:
                setdef_subcmd += f" DISPLAY({' '.join(kwargs['display'])})"

        # ======================
        # FLAG
        # ======================

        if "flag" in kwargs:
            if not isinstance(kwargs["flag"], (str)):
                raise ArgumentTypeError("flag", kwargs["flag"], (str))
            if not kwargs["flag"].upper() in [
                "ERROR",
                "INFORMATIONAL",
                "SERIOUS",
                "SEVERE",
                "TERMINATING",
                "WARNING",
            ]:
                raise ValueError(
                    f"{kwargs["flag"]} is not a valid FLAG parameter."
                    + " Valid parameters are:"
                    + " 'ERROR','INFORMATIONAL','SERIOUS','SEVERE','TERMINATING', or 'WARNING'."
                )
            setdef_subcmd += f" FLAG({kwargs['flag']})"

        # =================
        # LENGTH
        # =================

        if "length" in kwargs:
            if not isinstance(kwargs["length"], (str, int, Hex)):
                raise ArgumentTypeError("length", kwargs["length"], (str, int, Hex))
            if isinstance(kwargs["length"], (str, int)):
                setdef_subcmd += f" LENGTH(X'{Hex(kwargs['length'])}')"
            if isinstance(kwargs["length"], Hex):
                setdef_subcmd += f" LENGTH(X'{kwargs['length']}')"

        # =====================
        # PDS NOPDS
        # =====================

        if "pds" in kwargs:
            if not isinstance(kwargs["pds"], bool):
                raise ArgumentTypeError("pds", kwargs["pds"], bool)
            if kwargs["pds"]:
                setdef_subcmd += " PDS"
            else:
                setdef_subcmd += " NOPDS"

        # =================
        # ASID
        # =================

        if "asid" in kwargs:
            if not isinstance(kwargs["asid"], (str, int, Hex)):
                raise ArgumentTypeError("asid", kwargs["asid"], (str, int, Hex))
            if isinstance(kwargs["asid"], (str, int)):
                setdef_subcmd += f" ASID(X'{Hex(kwargs['asid'])}')"
            if isinstance(kwargs["asid"], Hex):
                setdef_subcmd += f" ASID(X'{kwargs['asid']}')"

        # ====================
        # DSPNAME
        # ====================

        if "dspname" in kwargs:
            if not isinstance(kwargs["dspname"], str):
                raise ArgumentTypeError("dspname", kwargs["dspname"], str)
            setdef_subcmd += f" DSPNAME({kwargs['dspname']})"

        # ===================
        # Other Parameters
        # ===================

        if "setdef_params" in kwargs:
            if not isinstance(kwargs["setdef_params"], str):
                raise ArgumentTypeError("setdef_params", kwargs["setdef_params"], str)
            setdef_subcmd += f" {kwargs['setdef_params']}"

        # ========================
        # Run SETDEF Subcommand
        # ========================

        super().__init__(
            session,
            setdef_subcmd,
            outfile=outfile,
            keep_file=keep_file,
        )

        self._parse_defaults()

    def _parse_defaults(self) -> None:
        """
        Parse Defaults and store in data dict.

        Returns
        -------
        None
        """

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

        # ====================
        # DISPLAY
        # ====================

        def get_display_default(defaults_lines):
            display = []
            for line in defaults_lines:
                if "DISPLAY(" in line:
                    display_start = line.find("DISPLAY(") + len("DISPLAY(")
                    arg = line[display_start : line.find(")", display_start)].strip()
                    display.append(arg)
            if not display:
                return None
            return display

        # ====================
        # FLAG
        # ====================

        def get_flag_default(defaults_lines):
            if "FLAG(" in defaults_lines[2]:
                flag_start = defaults_lines[2].find("FLAG(") + len("FLAG(")
                return defaults_lines[2][
                    flag_start : defaults_lines[2].find(")", flag_start)
                ]
            return None

        # =================
        # LENGTH
        # =================

        def get_length_default(defaults_lines):
            if "LENGTH(" in defaults_lines[6]:
                length_start = defaults_lines[6].find("LENGTH(") + len("LENGTH(")
                return defaults_lines[6][
                    length_start : defaults_lines[6].find(")", length_start)
                ]
            return None

        # =====================
        # PDS NOPDS
        # =====================

        def get_pds_default(defaults_lines):
            if "NOPDS" in defaults_lines[1]:
                return False
            return True

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
            self.data["display"] = get_display_default(global_defaults_lines)
            self.data["flag"] = get_flag_default(global_defaults_lines)
            self.data["length"] = get_length_default(global_defaults_lines)
            self.data["pds"] = get_pds_default(global_defaults_lines)
            self.data["asid"] = get_asid_default(global_defaults_lines)
            self.data["dspname"] = get_dspname_default(global_defaults_lines)
