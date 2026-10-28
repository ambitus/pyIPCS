"""
IPCS Subcommand Function
"""

# pylint: disable=duplicate-code

import subprocess
import tempfile
from typing import IO, Optional
from pyipcs._tso_shell_script import tso_shell_script
from pyipcs.exceptions import TsoError, IpcsError
from pyipcs.response import IpcsResponse


def ipcs_subcmd(
    subcmd: str,
    driver: str,
    ddir: str,
    allocations: dict[str, str | list[str]],
    authorized: bool,
    local_defaults: Optional[str] = None,
    tasklib: Optional[str] = None,
    output: Optional[IO[str]] = None,
) -> IpcsResponse:
    """
    Run an IPCS subcommand.

    Args:
        subcmd: IPCS subcommand to run.
        driver: Name of the pyIPCS driver data set (PDSE) that contains the
            IPCSRUN CLIST member.
        ddir: Data set name of the dump directory (DDIR) to allocate to
            ``IPCSDDIR`` for the subcommand.
        allocations: Dictionary of allocations where keys are DD names and values
            are string data set allocation requests or lists of cataloged datasets.
        authorized: Indicates whether the subcommand will be run in an
            authorized environment.
        local_defaults: If non-empty, runs
            ``SETDEF NOLIST LOCAL <local_defaults>`` before running the
            specified subcommand. Note: the defaults set by this will not carry
            over to future subcommands. May be a single string
            (e.g. ``'FLAG(WARNING) CONFIRM(NO)'``). Default is ``None`` to not
            run a ``SETDEF`` subcommand before running the specified subcommand.
        tasklib: If non-empty, passed as ``TASKLIB(<tasklib>)`` on the
            ``IPCS NOPARM`` call. Default is ``None``.
        output: An open, writable text file object. When provided, subcommand
            output is written to this file instead of being returned as a string
            (``output`` attribute will be ``None`` in the returned
            :class:`~pyipcs.IpcsResponse`). Default is ``None``.

    Returns:
        IpcsResponse: Response from the IPCS subcommand.
    """
    allocations = {**allocations, "IPCSDDIR": [ddir]}

    # Construct IPCS subcommand
    escaped_subcmd = subcmd.strip().replace("'", "''''")

    # Build optional CLIST keyword arguments
    extra_parms = ""
    if local_defaults:
        escaped_setdef = local_defaults.replace("'", "''''")
        extra_parms += f" SDL(''SETDEF NOLIST LOCAL {escaped_setdef}'')"
    if tasklib:
        escaped_tl = tasklib.replace("'", "''''")
        extra_parms += f" TL(''{escaped_tl}'')"

    cmd = f"ex '{driver}(IPCSRUN)' 'SUB(''{escaped_subcmd}''){extra_parms}'"

    shell_script = tso_shell_script(
        cmd=cmd,
        authorized=authorized,
        allocations=allocations,
    )

    # Write output to temporary file first to ensure encoding of output
    with tempfile.NamedTemporaryFile(
        mode="w+", encoding="cp1047", delete=True
    ) as tmp_file:
        try:
            subprocess.run(
                shell_script,
                shell=True,
                stdout=tmp_file,
                stderr=subprocess.STDOUT,
                check=True,
            )
        except Exception as e:
            tmp_file.seek(0)
            for _ in range(2):
                tmp_file.readline()
            err_output = tmp_file.read()
            message = f"Failed to execute IPCS process for subcommand '{subcmd}'"
            if err_output:
                message += f"\n[OUTPUT]:\n{err_output}"
            raise TsoError(message) from e

        # Skip the first lines which are not output of the subcommand
        tmp_file.seek(0)
        for _ in range(2):
            tmp_file.readline()

        # Determine if IO object was provided and pipe output if provided
        pyipcs_rc = None
        prev_line = None
        if output is not None:
            for line in tmp_file:
                # Return code line - ends subcommand output
                # Remove newline of prev line before write
                if line.startswith("PYIPCS_RC="):
                    if prev_line is not None:
                        output.write(prev_line.rstrip("\n"))
                    pyipcs_rc = int(line.strip().split("=", 1)[1])
                    break
                # Write first line as the first prev line
                if prev_line is None:
                    prev_line = line
                # Write line of subcommand output
                else:
                    output.write(prev_line)
                    prev_line = line
            subcmd_output = None
        else:
            # If no file object was provided read in rest of IPCS subcommand output
            lines = []
            for line in tmp_file:
                if line.startswith("PYIPCS_RC="):
                    pyipcs_rc = int(line.strip().split("=", 1)[1])
                    break
                lines.append(line)
            subcmd_output = "".join(lines).rstrip("\n")

    if pyipcs_rc is None:
        message = (
            f"Could not find return code output during pyIPCS driver execution "
            f"while running IPCS subcommand '{subcmd}'"
        )
        if subcmd_output:
            message += f"\n[OUTPUT]:\n{subcmd_output}"
        raise IpcsError(message)

    return IpcsResponse(
        subcmd=subcmd,
        rc=pyipcs_rc,
        output=subcmd_output,
        authorized=authorized,
    )
