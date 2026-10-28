"""
Internal Utility Functions
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from zoautil_py import datasets, zoau_io  # pylint: disable=import-error
from ._tso_cmd import tso_cmd
from .exceptions import TsoError

if TYPE_CHECKING:
    from .dump import IpcsDump


def tso_profile_prefix() -> str:
    """
    Return the TSO profile prefix (high-level qualifier).

    Returns:
        str: TSO profile prefix, or the ``USER`` environment variable if
        unavailable, or ``"TEMP"`` as a last resort.
    """
    return datasets.get_hlq() if datasets.get_hlq() else os.getenv("USER", "TEMP")


def attempt_recall(dsname: str) -> None:
    """
    Use automatic recall to attempt to recall a data set.

    Args:
        dsname: Data set name to recall.
    """
    tso_cmd(
        "TIME",
        allocations={"PYIPCS": dsname},
    )


def get_dataset(dsname: str) -> datasets.Dataset | None:
    """
    Get a specific :class:`~zoautil_py.datasets.Dataset` object by data set name.

    Will attempt to recall the data set if it exists.

    Args:
        dsname: Data set name.

    Returns:
        zoautil_py.datasets.Dataset | None: Data set object, or ``None`` if the
        data set does not exist.

    Raises:
        ValueError: If the data set name contains a wildcard (``*``), or if the
            data set does not exist.
    """
    if "*" in dsname:
        raise ValueError(
            f"Data set name {dsname} cannot be a pattern (cannot include '*')"
        )

    attempt_recall(dsname)
    dataset_list = datasets.list_datasets(dsname.strip())

    for dataset_obj in dataset_list:
        if dataset_obj.name == dsname.strip():
            return dataset_obj

    # If the data set is not found in the list it does not exist
    raise ValueError(f"Data set {dsname} does not exist")


def check_dataset_exists(dsname: str) -> bool:
    """
    Attempt recall and check if a data set exists.

    Args:
        dsname: Data set name.

    Returns:
        bool: ``True`` if the data set exists, ``False`` otherwise.

    Raises:
        ValueError: If the data set name contains a wildcard (``*``).
    """
    if "*" in dsname:
        raise ValueError(
            f"Data set name {dsname} cannot be a pattern (cannot include '*')"
        )
    attempt_recall(dsname)
    return datasets.exists(dsname)


def assert_dataset_exists(dsname: str) -> None:
    """
    Attempt recall and raise an error if the data set does not exist.

    Args:
        dsname: Data set name.

    Raises:
        ValueError: If the data set name contains a wildcard (``*``).
        TsoError: If the data set does not exist.
    """
    if "*" in dsname:
        raise ValueError(
            f"Data set name {dsname} cannot be a pattern (cannot include '*')"
        )
    attempt_recall(dsname)
    if not datasets.exists(dsname):
        raise TsoError(f"Data set {dsname} does not exist")


def get_header_record(dump: IpcsDump) -> bytes | None:
    """
    Get the first z/OS dump header record in the dump data set.

    Args:
        dump: :class:`~pyipcs.IpcsDump` instance.

    Returns:
        bytes | None: First header record as a bytes object, or ``None`` if the
        header record was not found.
    """
    io = zoau_io.RecordIO(f"//'{dump.dsname}'")
    first_record = io.readrecord()
    second_record = io.readrecord()
    # PRDAST - Address space type code
    # X'C840' / H = Header
    if first_record[4:6].hex() == "C840":
        return first_record
    if second_record[4:6].hex() == "C840":
        return second_record
    return None
