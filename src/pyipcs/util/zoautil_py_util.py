"""
pyIPCS zoatuil_py Related Util Functions
"""

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

    Parameters
    ----------
    dsname : str

    Returns
    -------
    zoautil_py.datasets.Dataset|None
        `None` if z/OS dataset does not exist
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

    Parameters
    ----------
    dsname : str

    Returns
    -------
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

    Parameters
    ----------
    dsname : str
        z/OS dataset name

    Returns
    -------
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
