"""
TSO Command Function
"""

# pylint: disable=duplicate-code

import subprocess
import tempfile
from typing import Optional
from pyipcs._tso_shell_script import tso_shell_script
from pyipcs.exceptions import TsoError
from pyipcs.response import TsoResponse


def tso_cmd(
    cmd: str,
    allocations: Optional[dict[str, str | list[str]]] = None,
) -> TsoResponse:
    """
    Run a TSO/E command.

    Args:
        cmd: TSO/E command to run.
        allocations: Dictionary of allocations where keys are DD names and values
            are string data set allocation requests or lists of cataloged datasets.
            Default is ``None`` (no allocations).

    Returns:
        TsoResponse: Response from the TSO/E command.
    """
    if allocations is None:
        allocations = {}

    shell_script = tso_shell_script(
        cmd=cmd,
        authorized=True,
        allocations=allocations,
    )

    # Write output to temporary file first to ensure encoding of output
    with tempfile.NamedTemporaryFile(
        mode="w+", encoding="cp1047", delete=True
    ) as tmp_file:
        try:
            completed_process = subprocess.run(
                shell_script,
                shell=True,
                stdout=tmp_file,
                stderr=subprocess.STDOUT,
                check=False,
            )
        except Exception as e:
            tmp_file.seek(0)
            output = tmp_file.read()
            message = f"Failed to run TSO/E command '{cmd}'"
            if output:
                message += f"\n[OUTPUT]:\n{output}"
            raise TsoError(message) from e

        tmp_file.seek(0)
        output = tmp_file.read()

    return TsoResponse(
        cmd=cmd,
        rc=completed_process.returncode,
        output=output,
        authorized=True,
    )
