"""
IPCS Utility Functions
"""

from __future__ import annotations
import datetime
from typing import Optional, TYPE_CHECKING

from zoautil_py import zoau_io  # pylint: disable=import-error
from ._util import get_dataset
from .response import IpcsParsedResponse

if TYPE_CHECKING:
    from .ddir import IpcsDdir
    from .dump import IpcsDump


def is_dump(dsname: str) -> bool:
    """
    Determine whether a data set exists and is a z/OS dump data set.

    Args:
        dsname: Data set name.

    Returns:
        bool: ``True`` if the data set exists and is a dump data set,
        ``False`` otherwise.
    """
    # Check if the data set exists and perform checks
    dump_dataset_obj = get_dataset(dsname)
    if dump_dataset_obj is None:
        return False
    if int(dump_dataset_obj.record_length) != 4160:
        return False
    if int(dump_dataset_obj.block_size) % int(dump_dataset_obj.record_length) != 0:
        return False
    # Check if first record starts with DR2
    if (
        not zoau_io.RecordIO(f"//'{dsname}'")
        .readrecord()
        .hex()
        .upper()
        .startswith("C4D9F2")
    ):
        return False
    return True


def find_field(
    text: str,
    start_str: str,
    length: Optional[int] = None,
    end_str: Optional[str] = None,
    start: int = 0,
    end: Optional[int] = None,
) -> tuple[int, int]:
    """
    Find the first field that follows a start string.

    The field is the text in between ``start_str`` and either ``length`` characters later
    or the next occurrence of ``end_str``. If neither is given, the field ends at the next
    space character.

    Args:
        text: String to search.
        start_str: String that marks the beginning of the field.
        length: Number of characters in the field.
        end_str: String that marks the end of the field.
        start: Index in ``text`` where the search begins. Defaults to the beginning of
            ``text``.
        end: Index in ``text`` where the search stops (exclusive). Defaults to the end of
            ``text``.

    Returns:
        tuple[int, int]: Beginning index (inclusive) and end index (exclusive) of the text
        in between, relative to ``text``. ``(-1, -1)`` if ``start_str`` is not found.
        ``(begin, -1)`` if ``start_str`` is found but the end of the field cannot be found.

    Raises:
        ValueError: If both ``length`` and ``end_str`` are provided.
    """
    if length is not None and end_str is not None:
        raise ValueError("Only one of length or end_str may be provided")
    idx = text.find(start_str, start, end)
    if idx == -1:
        return (-1, -1)
    begin = idx + len(start_str)
    limit = len(text) if end is None else min(end, len(text))
    if length is not None:
        stop = begin + length
        return (begin, stop if stop <= limit else -1)
    return (begin, text.find(" " if end_str is None else end_str, begin, limit))


def rfind_field(
    text: str,
    start_str: str,
    length: Optional[int] = None,
    end_str: Optional[str] = None,
    start: int = 0,
    end: Optional[int] = None,
) -> tuple[int, int]:
    """
    Find the last field that follows a start string.

    Same as :func:`find_field`, but uses the last occurrence of ``start_str``.

    Args:
        text: String to search.
        start_str: String that marks the beginning of the field.
        length: Number of characters in the field.
        end_str: String that marks the end of the field.
        start: Index in ``text`` where the search begins. Defaults to the beginning of
            ``text``.
        end: Index in ``text`` where the search stops (exclusive). Defaults to the end of
            ``text``.

    Returns:
        tuple[int, int]: Beginning index (inclusive) and end index (exclusive) of the text
        in between, relative to ``text``. ``(-1, -1)`` if ``start_str`` is not found.
        ``(begin, -1)`` if ``start_str`` is found but the end of the field cannot be found.

    Raises:
        ValueError: If both ``length`` and ``end_str`` are provided.
    """
    if length is not None and end_str is not None:
        raise ValueError("Only one of length or end_str may be provided")
    idx = text.rfind(start_str, start, end)
    if idx == -1:
        return (-1, -1)
    begin = idx + len(start_str)
    limit = len(text) if end is None else min(end, len(text))
    if length is not None:
        stop = begin + length
        return (begin, stop if stop <= limit else -1)
    return (begin, text.find(" " if end_str is None else end_str, begin, limit))


def sliptrap(
    ddir: IpcsDdir, dump: IpcsDump
) -> Optional[IpcsParsedResponse[Optional[str]]]:
    """
    Run ``LIST SLIPTRAP`` and return the SLIPTRAP string for the dump.

    Args:
        ddir: DDIR to run the subcommand against.
        dump: Dump data set to run the subcommand against.

    Returns:
        IpcsParsedResponse[str | None] | None: Parsed response containing the SLIPTRAP
        string (or ``None`` if not found) in ``data`` and the raw ``response``,
        or ``None`` if the dump is not a SLIP dump.
    """
    if dump.metadata is None or dump.metadata.get("type") != "SLIP":
        return None

    response = ddir.run("LIST SLIPTRAP", dump=dump)
    if response.rc > 0 or response.output is None:
        return IpcsParsedResponse(data=None, response=response)

    sliptrap_lines = response.output.splitlines()

    # If the number of lines is 1 or less there is no SLIPTRAP
    if len(sliptrap_lines) <= 1:
        return IpcsParsedResponse(data=None, response=response)

    # Remove first 3 lines to get to SLIPTRAP content
    sliptrap_lines = sliptrap_lines[3:]

    # SLIPTRAP text is between '| ' and ' |'
    result = ""
    for line in sliptrap_lines:
        start = line.find("| ")
        if start == -1:
            continue
        result += line[start + len("| ") : len(line) - len(" |")]

    return IpcsParsedResponse(data=result if result else None, response=response)


def ipl_time(ddir: IpcsDdir, dump: IpcsDump) -> IpcsParsedResponse[Optional[str]]:
    """
    Run ``IPLDATA`` and return the local IPL date/time in ISO 8601 format.

    Args:
        ddir: DDIR to run the subcommand against.
        dump: Dump data set to run the subcommand against.

    Returns:
        IpcsParsedResponse[str | None]: Parsed response containing the ISO 8601
        datetime string (``YYYY-MM-DDTHH:MM:SS``) in ``data`` and the raw
        ``response``, or ``data`` as ``None`` if the information could not be
        determined or the subcommand return code is greater than 0.
    """
    response = ddir.run("IPLDATA", dump=dump)
    if response.rc > 0 or response.output is None:
        return IpcsParsedResponse(data=None, response=response)

    output = response.output
    begin, end = find_field(output, "System IPLed at ", end_str="\n")
    if end == -1:
        return IpcsParsedResponse(data=None, response=response)

    line = output[begin:end].strip()

    # Line format: "HH:MM:SS on MM/DD/YYYY"
    try:
        time_str, date_str = line.split(" on ")
        dt = datetime.datetime.strptime(
            f"{date_str.strip()} {time_str.strip()}", "%m/%d/%Y %H:%M:%S"
        )
        return IpcsParsedResponse(data=dt.isoformat(), response=response)
    except (ValueError, AttributeError):
        return IpcsParsedResponse(data=None, response=response)


def select_all(
    ddir: IpcsDdir, dump: IpcsDump
) -> IpcsParsedResponse[Optional[list[dict]]]:
    """
    Run ``SELECT ALL`` and return a list of ASIDs on the system at dump time.

    Args:
        ddir: DDIR to run the subcommand against.
        dump: Dump data set to run the subcommand against.

    Returns:
        IpcsParsedResponse[list[dict] | None]: Parsed response containing a list
        of dictionaries in ``data`` with keys:

        - **"asid"** (str): Hex ASID string.
        - **"jobname"** (str | None): Job name, or ``None`` if unavailable.
        - **"ascb"** (str): Hex ASCB address string.

        and the raw ``response``. Returns ``data`` as ``None`` if the
        subcommand return code is greater than 0 or the output could not be
        parsed.
    """
    response = ddir.run("SELECT ALL", dump=dump)
    if response.rc > 0 or response.output is None:
        return IpcsParsedResponse(data=None, response=response)

    output = response.output
    header_marker = "ASID JOBNAME  ASCBADDR  SELECTION CRITERIA"
    idx = output.find(header_marker)
    if idx == -1:
        return IpcsParsedResponse(data=None, response=response)

    # Skip header line and separator line
    asid_lines = output[idx:].splitlines()[2:]

    asids_all = []
    for line in asid_lines:
        asid = line[1:5].strip()
        jobname = line[6:14].strip() or None
        ascb = line[15:24].strip()
        asids_all.append({"asid": asid, "jobname": jobname, "ascb": ascb})

    return IpcsParsedResponse(data=asids_all, response=response)


def storage_areas(ddir: IpcsDdir, dump: IpcsDump) -> IpcsParsedResponse[Optional[dict]]:
    """
    Run ``LISTDUMP SELECT DSNAME`` and return all ASIDs and data spaces included in the dump.

    Args:
        ddir: DDIR to run the subcommand against.
        dump: Dump data set to run the subcommand against.

    Returns:
        IpcsParsedResponse[dict | None]: Parsed response containing a dictionary
        in ``data`` with keys:

        - **"asids"** (list[str]): List of hex ASID strings present in the dump.
        - **"dspnames"** (dict[str, list[str]]): Mapping of hex ASID string to a
          list of data space names dumped for that ASID. ASIDs without a data space
          are not included.

        and the raw ``response``. Returns ``data`` as ``None`` if the
        subcommand return code is greater than 0 or the output could not be
        parsed.
    """
    response = ddir.run(f"LISTDUMP SELECT DSNAME('{dump.dsname}')", dump=dump)
    if response.rc > 0 or response.output is None:
        return IpcsParsedResponse(data=None, response=response)

    output = response.output
    asids: set[str] = set()
    dspnames: dict[str, list[str]] = {}
    pos = 0

    while True:
        idx = output.find("bytes described in", pos)
        if idx == -1:
            break

        line = output[output.rfind("\n", 0, idx) + 1 : output.find("\n", idx)]
        pos = idx + 1

        if "ASID" not in line:
            continue

        asid_start, asid_end = find_field(line, "ASID(X'", end_str="')")
        if asid_end == -1:
            continue
        asid = line[asid_start:asid_end]
        asids.add(asid)

        dspname_start, dspname_end = find_field(line, "DSPNAME(", end_str=")")
        if dspname_end != -1:
            if asid not in dspnames:
                dspnames[asid] = []
            dspnames[asid].append(line[dspname_start:dspname_end])

    return IpcsParsedResponse(
        data={"asids": list(asids), "dspnames": dspnames},
        response=response,
    )


def asids_dumped(
    ddir: IpcsDdir, dump: IpcsDump
) -> IpcsParsedResponse[Optional[list[str]]]:
    """
    Run ``CBF RTCT`` and return the list of requested ASIDs that were dumped.

    Args:
        ddir: DDIR to run the subcommand against.
        dump: Dump data set to run the subcommand against.

    Returns:
        IpcsParsedResponse[list[str] | None]: Parsed response containing a list
        of hex ASID strings that were dumped in ``data`` and the raw ``response``.
        Returns ``data`` as ``None`` if the subcommand return code is greater
        than 0 or the output could not be parsed.
    """
    response = ddir.run("CBF RTCT", dump=dump)
    if response.rc > 0 or response.output is None:
        return IpcsParsedResponse(data=None, response=response)

    marker = "SDAS  SDF4  SDF5"
    idx = response.output.find(marker)
    if idx == -1:
        return IpcsParsedResponse(data=None, response=response)

    # Skip the header line and separator line, take up to 16 ASID lines
    asid_lines = response.output[idx:].splitlines()[2:18]

    asids = []
    for line in asid_lines:
        parts = line.split()
        if len(parts) < 2:
            break
        asid = parts[1]
        if asid == "0000":
            break
        asids.append(asid)

    return IpcsParsedResponse(data=asids, response=response)


def opcode(
    ddir: IpcsDdir, dump: IpcsDump, instr: str
) -> IpcsParsedResponse[Optional[str]]:
    """
    Run ``OPCODE`` and return the mnemonic for an instruction.

    Args:
        ddir: DDIR to run the subcommand against.
        dump: Dump data set to run the subcommand against.
        instr: Hex string of the instruction opcode (e.g. ``"0A0A"``).

    Returns:
        IpcsParsedResponse[str | None]: Parsed response containing the
        instruction mnemonic in ``data`` and the raw ``response``. Returns
        ``data`` as ``None`` if the mnemonic could not be determined or the
        subcommand return code is greater than 0.
    """
    response = ddir.run(f"OPCODE {instr}", dump=dump)
    if response.rc > 0 or response.output is None:
        return IpcsParsedResponse(data=None, response=response)
    if "IKJ56702I INVALID VARIABLE MNEMONIC OPTION" in response.output:
        return IpcsParsedResponse(data=None, response=response)

    begin, end = find_field(
        response.output, f"Mnemonic for X'{instr}' is ", end_str="\n"
    )
    if end == -1:
        return IpcsParsedResponse(data=None, response=response)

    mnemonic = response.output[begin:end].strip()
    return IpcsParsedResponse(data=mnemonic if mnemonic else None, response=response)
