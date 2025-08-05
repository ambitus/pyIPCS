"""
pyIPCS zoatuil_py Related Util Functions
"""

import datetime
from zoautil_py import datasets, zoau_io
from ..error_handling import ArgumentTypeError
from ..hex_obj import Hex
from ..tso_shell import recall

# ===================
# Helper Functions
# ===================


def read_hex(dsname: str, srec: int = 0, count: int = 0) -> Hex:
    """
    Reads hex from raw z/OS dataset
    """
    d_stream = zoau_io.RecordIO(f"//'{dsname}'")
    # change the cursor position
    d_stream.seek(srec, 0)
    # Read n record from cursor position
    records = d_stream.readrecords(count)
    data = b""
    for record in records:  # convert list to byte string
        data = data + record
    return Hex(data.hex())


def get_dataset(dsname: str) -> datasets.Dataset | None:
    """
    Get specific Dataset object from dataset name.

    Will recall dataset if it exists.

    Args:
        dsname (str)
    Returns:
        zoautil_py.datasets.Dataset|None: `None` if z/OS dataset does not exist
    """
    if not isinstance(dsname, str):
        raise ArgumentTypeError("dsname", dsname, str)
    if "*" in dsname:
        raise ValueError("Argument 'dsname' cannot be a pattern (cannot include '*')")

    def zoau_get_dataset(zoau_dsname: str):
        dataset_list = datasets.list_datasets(zoau_dsname)
        for dataset_obj in dataset_list:
            if dataset_obj.name == zoau_dsname:
                return dataset_obj
        return None

    zoau_dataset = zoau_get_dataset(dsname)
    # If dataset wasn't found attempt recall and check again
    if zoau_dataset is None:
        recall(dsname)
        zoau_dataset = zoau_get_dataset(dsname)
    return zoau_dataset


def datasets_recall_exists(dsname: str) -> bool:
    """
    Check if VSAM or non-VSAM dataset exists.

    Will recall dataset if it exists.

    Args:
        dsname (str)
    Returns:
        bool
    """
    if not isinstance(dsname, str):
        raise ArgumentTypeError("dsname", dsname, str)

    def zoau_dataset_exists(zoau_dsname: str) -> bool:
        vsam_dataset_exists = datasets.list_vsam_datasets(zoau_dsname)
        non_vsam_dataset_exists = datasets.exists(zoau_dsname)
        return vsam_dataset_exists or non_vsam_dataset_exists

    zoau_bool = zoau_dataset_exists(dsname)
    # If dataset wasn't found attempt recall and check again
    if not zoau_bool:
        recall(dsname)
        zoau_bool = zoau_dataset_exists(dsname)
    return zoau_bool

# ==========================
# Exposed Util Functions
# ==========================

def is_dump(dsname: str) -> bool:
    """
    Determine whether dataset is a z/OS dump.

    Will recall dataset if it exists.

    Args:
        dsname (str):
            z/OS dataset name
    Returns:
        bool
    """
    if not isinstance(dsname, str):
        raise TypeError(
            f"Argument 'dsname' must be of type str, but got {type(dsname)}"
        )

    dataset = get_dataset(dsname)
    if dataset is None:
        raise ValueError(
            "z/OS dataset specified in argument 'dsname' does not exist or is migrated"
        )

    dump_lrecl = 4160
    if int(dataset.record_length) != dump_lrecl:
        return False

    if int(dataset.block_size) % int(dataset.record_length) != 0:
        return False

    if not read_hex(dataset.name, count=1).to_char_str().startswith("DR2"):
        return False

    return True


def dump_header_data(dsname: str) -> dict:
    """
    Obtain info about z/OS dump from dump header without the need to create a Dump object

    Args:
        dsname (str):
            z/OS dataset name

    Returns:
        dict:
            Info about z/OS dump obtained from dump header
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
        ```
    """
    if not isinstance(dsname, str):
        raise TypeError(
            f"Argument 'dsname' must be of type str, but got {type(dsname)}"
        )

    dataset = get_dataset(dsname)
    if not is_dump(dsname):
        raise ValueError(
            "z/OS dataset specified in argument 'dsname' is not a z/OS dump"
        )

    header_data = {}
    hex_header = read_hex(dataset.name, count=2)
    if hex_header[:10] != Hex("C4D9F240C8"):  # DR2 H signifies this is the dump header
        # First block is not the dr2 h header, try the second page
        hex_header = hex_header[8320:]
    if hex_header[:10] != Hex("C4D9F240C8"):  # DR2 H signifies this is the dump header
        # Second block isnt a valid dr2 h header either
        raise RuntimeError(
            f"{dataset.name} doesnt contain dr2 h on first or second page"
        )

    # Now we have the dump header in hex string and text string
    char_header = hex_header.to_char_str()

    # Will use the PRDINPUT structure within BLSPRD mapping to get various fields from this header
    # https://www.ibm.com/docs/en/zos/3.1.0?topic=iar-blsrprd-information

    # ===============================
    # 1 - Get Dump Type    PRD64DUMPT
    # Data : dump_type
    # ===============================

    #   Offset x'24' is decimal 36     36*2=72
    #   1 = SAD
    #   2 = SVC Dump
    #   3 = SYSMDUMP (might actually be a TDUMP)
    #   4 = SLIP Dump
    #   Other = Not recorded
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
    # 2 - Get System Name   PRDSNAME
    # Data : sysname
    # ==============================

    header_data["sysname"] = char_header[204:212].rstrip()

    # =============================
    # 3 - Get Dump Time PRDTODVL
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
    # 4 - Get Dump Title PRDTITLE
    # Data : title
    # ==============================

    # Offset x'58' is decimal 88 (len 100)
    header_data["title"] = char_header[88:188].rstrip()

    # ===========================
    # 5 - Get original dump dsn
    # Data : original_dump_dsn
    # ===========================

    header_data["original_dump_dsn"] = char_header[444:488].rstrip()

    # =============================================================================================
    # 6 - Get the z/os version and release that took the dump PRDPRODV+PRDPRODR+PRDPRODM+PRDPRODD
    # Data : version, release
    # =============================================================================================

    # Offset x'104' is decimal 260
    header_data["version"] = int(char_header[260:262])
    header_data["release"] = int(char_header[262:264])

    # =============================
    # 7 - Get SDRSN PRDSDRSN
    # Data : sdrsn, complete_dump
    # =============================

    # Offset x'E0' is decimal 224    224*2= 448
    header_data["sdrsn"] = hex_header[448:480]
    header_data["complete_dump"] = header_data["sdrsn"].to_str()=="00000000000000000000000000000000"

    # =========================================
    # Do not add below if it is not an SAD
    # =========================================
    if header_data["dump_type"] != "SAD":
        # =========================================
        # 8 - Get the jobname of this dump PRDHJOBN
        # Data : home_jobname
        # =========================================

        # Mapping says x'2A0' but it looks to be at x'44C' or 1100
        header_data["home_jobname"] = char_header[1100:1108].rstrip()

        # ============================================================
        # 9 - Get PASN , SASN, and HASN (PRDPASID, PRDSASID, PRDHASID)
        # Data : primary, secondary, home
        # ============================================================

        header_data["primary"] = hex_header[1000:1004]
        header_data["secondary"] = hex_header[1004:1008]
        header_data["home"] = hex_header[1008:1012]

        # ================================
        # 10 - Get SDWA ASID and Address
        # Data : sdwa_asid, sdwa_address
        # ================================

        header_data["sdwa_asid"] = hex_header[1012:1016]
        header_data["sdwa_address"] = hex_header[1016:1024]

        # =================================================================
        # 11 - Get number of blocks dynamically allocated for dump PRDSDBLK
        # Data : blocks_allocated_decimal
        # =================================================================

        # Offset x'F0' is decimal 240  240*2 = 480
        header_data["blocks_allocated_decimal"] = hex_header[480:488].to_int()

        # =============================================
        # 12 - Get name of system requesting this dump
        # Data : remote_sysname, remote_dump
        # =============================================

        header_data["remote_sysname"] = char_header[1644:1652].rstrip()
        header_data["remote_dump"] = (
            header_data["remote_sysname"] != header_data["sysname"]
        )
        if not header_data["remote_sysname"]:
            del header_data["remote_sysname"]

    # ===============================================
    # 13 - Get Serial number of this system PRDPSERL
    # Data : processor_serial_number
    # ===============================================

    # Offset x'51' is decimal 81  81*2 is 162
    header_data["processor_serial_number"] = hex_header[162:168].to_str()

    # =============================================
    # 14 - Get Processor model number PRDPMODL

    # Offset x'54' is decimal 84    84*2 is 168
    header_data["processor_model_number"] = hex_header[168:172].to_str()

    return header_data
