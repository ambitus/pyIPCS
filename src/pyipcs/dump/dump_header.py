"""
DumpHeader Object
"""

import datetime
from ..hex_obj import Hex
from ..error_handling import ArgumentTypeError
from ..util.zoautil_py_util import (
    read_hex,
    datasets_recall_exists,
    is_dump,
)

class DumpHeader(dict):
    """
    DumpHeader Object

    Custom Dictionary with info about a dump from the dump header.

    Does not require dump initialization to instantiate object.

    Keys may not appear if information is unknown or unavailable.

    Keys
    ----
    **"dump_type"** (str)
        `"SAD"`, `"SVCD"`, `"TDMP"`, `"SYSM"`, or `"SLIP"`

    **"sysname"** (str)

    **"date_local"** (str)

    **"time_local"** (str)

    **"title"** (str)

    **"original_dump_dsn"** (str)

    **"version"** (int)
        For example z/OS version `3` release `1`
    
    **"release"** (int)
        For example z/OS version `3` release `1`

    **"sdrsn"** (str)

    **"complete_dump"** (bool)

    **"home_jobname"** (str)
        
    **"primary"** (pyipcs.Hex)
        
    **"secondary"** (pyipcs.Hex)
        
    **"home"** (pyipcs.Hex)
        
    **"sdwa_asid"** (pyipcs.Hex)
        
    **"sdwa_address"** (pyipcs.Hex)
        
    **"blocks_allocated_decimal"** (int)
        
    **"remote_sysname"** (str)
        Appears only if `remote_dump=True`
        
    **"remote_dump"** (bool)
        
    **"processor_serial_number"** (str)

    **"processor_model_number"** (str)

    Notes
    -----
    The following keys are unknown or unavailable if `dump_type="SAD"`:
        - **"home_jobname"**
        - **"primary"**
        - **"secondary"**
        - **"home"**
        - **"sdwa_asid"**
        - **"sdwa_address"**
        - **"blocks_allocated_decimal"**
        - **"remote_sysname"**
        - **"remote_dump"**
    
    """

    def __init__(
        self,
        dsname: str
    ) -> None:
        """
        Constructor for DumpHeader Object.

        Parameters
        ----------
        dsname : str
            Dump Dataset Name.

        Returns
        -------
        None
        """

        # ======================================
        # Various Checks for Dump Dataset Name
        # ======================================

        if not isinstance(dsname, str):
            raise ArgumentTypeError("dsname", dsname, str)

        if not datasets_recall_exists(dsname):
            raise ValueError(f"Dataset '{dsname}' does not exist")

        if not is_dump(dsname):
            raise ValueError(f"Dataset '{dsname}' is not a dump dataset")

        # ===================
        # Get Header
        # ===================

        hex_header = read_hex(dsname, count=2)

        char_header = hex_header.to_char_str()

        # ========================================================
        # Get Dump Header Data
        # Uses the PRDINPUT structure within BLSPRD mapping to get various fields from this header
        # https://www.ibm.com/docs/en/zos/3.1.0?topic=iar-blsrprd-information
        # ========================================================

        header_data = {}

        # =============================
        # Store Dump Dataset Name
        # =============================

        self._dsname = dsname

        # ===============================
        # Get Dump Type    PRD64DUMPT
        # Data : dump_type
        # ===============================

        #   Offset x'24' is decimal 36     36*2=72
        #   1 = SAD
        #   2 = SVC Dump
        #   3 = SYSMDUMP (might actually be a TDUMP)
        #   4 = SLIP Dump
        #   Unknown = not recorded

        dump_type_hex = hex_header[72:74]

        if dump_type_hex == Hex("01"):
            header_data["dump_type"] = "SAD"
        elif dump_type_hex == Hex("02"):
            header_data["dump_type"] = "SVCD"
        elif dump_type_hex == Hex("03"):
            # its a SYSMDUMP but is it really a TDUMP?
            prdmodnm = char_header[64:72].upper()
            if prdmodnm == "IEAVTDMP":
                header_data["dump_type"] = "TDMP"
            else:
                header_data["dump_type"] = "SYSM"
        elif dump_type_hex == Hex("04"):
            header_data["dump_type"] = "SLIP"
        else:
            # Don't record dump_type if we can't find it
            pass

        # ==============================
        # Get System Name   PRDSNAME
        # Data : sysname
        # ==============================

        header_data["sysname"] = char_header[204:212].rstrip()

        # =============================
        # Get Dump Time PRDTODVL
        # Data : date_local, time_local
        # =============================

        # Offset x'48' is decimal 72    72*2 gives us 144
        stck_time = hex_header[144:160]
        stck_truncated = stck_time[0:13]
        dec_time = stck_truncated.to_int()
        seconds = dec_time / 1000000

        # Base datetime for IBM System Z time
        base_datetime = datetime.datetime(1900, 1, 1)
        dump_time = base_datetime + datetime.timedelta(seconds=seconds)

        header_data["date_local"] = dump_time.strftime("%m/%d/%y")
        header_data["time_local"] = dump_time.strftime("%H:%M:%S.%f")

        # ==============================
        # Get Dump Title PRDTITLE
        # Data : title
        # ==============================

        # Offset x'58' is decimal 88 (len 100)
        header_data["title"] = char_header[88:188].rstrip()

        # ===========================
        # Get original dump dsn
        # Data : original_dump_dsn
        # ===========================

        header_data["original_dump_dsn"] = char_header[444:488].rstrip()

        # ========================================================================================
        # Get the z/os version and release that took the dump PRDPRODV+PRDPRODR+PRDPRODM+PRDPRODD
        # Data : version, release
        # ========================================================================================

        # Offset x'104' is decimal 260
        header_data["version"] = int(char_header[260:262])
        header_data["release"] = int(char_header[262:264])

        # =============================
        # Get SDRSN PRDSDRSN
        # Data : sdrsn, complete_dump
        # =============================

        # Offset x'E0' is decimal 224    224*2= 448
        header_data["sdrsn"] = hex_header[448:480]
        header_data["complete_dump"] = (
            header_data["sdrsn"].to_str()=="00000000000000000000000000000000"
        )

        # =========================================
        # Get the jobname of this dump PRDHJOBN
        # Data : home_jobname
        # =========================================

        if header_data["dump_type"] != "SAD":
            # Mapping says x'2A0' but it looks to be at x'44C' or 1100
            header_data["home_jobname"] = char_header[1100:1108].rstrip()

        # ============================================================
        # Get PASN , SASN, and HASN (PRDPASID, PRDSASID, PRDHASID)
        # Data : primary, secondary, home
        # ============================================================

        if header_data["dump_type"] != "SAD":
            header_data["primary"] = hex_header[1000:1004]
            header_data["secondary"] = hex_header[1004:1008]
            header_data["home"] = hex_header[1008:1012]

        # ================================
        # Get SDWA ASID and Address
        # Data : sdwa_asid, sdwa_address
        # ================================

        if header_data["dump_type"] != "SAD":
            header_data["sdwa_asid"] = hex_header[1012:1016]
            header_data["sdwa_address"] = hex_header[1016:1024]

        # =================================================================
        # Get number of blocks dynamically allocated for dump PRDSDBLK
        # Data : blocks_allocated_decimal
        # =================================================================

        if header_data["dump_type"] != "SAD":
            # Offset x'F0' is decimal 240  240*2 = 480
            header_data["blocks_allocated_decimal"] = hex_header[480:488].to_int()

        # =============================================
        # Get name of system requesting this dump
        # Data : remote_sysname, remote_dump
        # =============================================

        if header_data["dump_type"] != "SAD":
            header_data["remote_sysname"] = char_header[1644:1652].rstrip()
            header_data["remote_dump"] = (
                header_data["remote_sysname"] != header_data["sysname"]
            )
            if not header_data["remote_sysname"]:
                del header_data["remote_sysname"]

        # ===============================================
        # Get Serial number of this system PRDPSERL
        # Data : processor_serial_number
        # ===============================================

        # Offset x'51' is decimal 81  81*2 is 162
        header_data["processor_serial_number"] = hex_header[162:168].to_str()

        # =============================================
        # Get Processor model number PRDPMODL
        # =============================================

        # Offset x'54' is decimal 84    84*2 is 168
        header_data["processor_model_number"] = hex_header[168:172].to_str()

        # =============================================
        # FINAL: Create Dictionary with Header Data
        # =============================================

        super().__init__(header_data)
