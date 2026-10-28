"""
Driver Functions
"""

from zoautil_py import datasets, exceptions  # pylint: disable=import-error
from pyipcs.exceptions import TsoError
from ._execs import IPCSVERS, IPCSRUN, IPCSSRC, IPCSEVAL
from ._util import check_dataset_exists, tso_profile_prefix
from ._version import __version__

_DRIVER_MEMBERS = {
    "IPCSVERS": IPCSVERS,
    "IPCSRUN": IPCSRUN,
    "IPCSSRC": IPCSSRC,
    "IPCSEVAL": IPCSEVAL,
}


def default_driver_dsname() -> str:
    """
    Return the default pyIPCS driver data set name.

    The name is derived as ``<TSO_profile_prefix>.PYIPCS.V<pyIPCS_version>``.

    Returns:
        str: Default driver data set name.
    """
    # Start with TSO prefix:
    dsname = tso_profile_prefix()
    # Add .PYIPCS.V<pyIPCS_version>:
    dsname += ".PYIPCS.V"
    dsname += "".join(part.zfill(2) for part in __version__.split("."))
    return dsname


def create_driver(dsname: str) -> None:
    """
    Create a pyIPCS driver data set.

    Args:
        dsname: Name of the pyIPCS driver data set to create and populate.

    Raises:
        ValueError: If the data set already exists.
        TsoError: If the data set could not be written.
    """
    if check_dataset_exists(dsname):
        raise ValueError(f"Data set {dsname} already exists")
    try:
        datasets.create(dsname, dataset_type="PDSE")
        for member_name, content in _DRIVER_MEMBERS.items():
            datasets.write(f"{dsname}({member_name})", content=content)
    except exceptions.DatasetWriteException as e:
        datasets.delete(dsname)
        raise TsoError(f"Failed to create pyIPCS driver data set {dsname}") from e


def validate_driver(dsname: str) -> None:
    """
    Validate an existing pyIPCS driver data set.

    Confirms that the driver data set exists,
    and contains all required members with expected contents

    Args:
        dsname: The fully-qualified driver data set name.

    Raises:
        TsoError: If the data set does not exist, its members cannot be listed,
            a required member is missing, or a member's content does not match.
    """
    if not check_dataset_exists(dsname):
        raise TsoError(f"pyIPCS driver data set {dsname} does not exist")

    try:
        members = datasets.list_members(dsname)
    except Exception as e:  # pylint: disable=broad-except
        raise TsoError(
            f"Failed to list members of pyIPCS driver data set {dsname}"
        ) from e

    for member_name, expected_content in _DRIVER_MEMBERS.items():
        if member_name not in members:
            raise TsoError(
                f"pyIPCS driver data set {dsname} is missing required member {member_name}"
            )

        def normalize(s: str) -> str:
            return "\n".join(line.rstrip() for line in s.splitlines()).strip()

        content = datasets.read(f"{dsname}({member_name})")
        actual_norm = normalize(content)
        expected_norm = normalize(expected_content)
        if actual_norm != expected_norm:
            raise TsoError(
                f"pyIPCS driver data set {dsname} member {member_name} has unexpected content\n"
                f"[ACTUAL]:\n{repr(actual_norm)}\n"
                f"[EXPECTED]:\n{repr(expected_norm)}"
            )
