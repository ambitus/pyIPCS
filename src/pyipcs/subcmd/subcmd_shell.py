"""
IPCS Subcommand Shell Execution
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import os
import subprocess
import copy
from ..tso_shell import tsocmd, construct_tso_shell_script, CalledTsoProcessError

if TYPE_CHECKING:
    from ..session import IpcsSession


IPCS_EX_SUBCMD = """ex \'{ipcs_subcmd_exec}\' \'subcmd(\'\'{ipcs_subcmd}\'\')\'"""


def construct_ipcs_shell_script(session: IpcsSession, ipcs_subcmd: str) -> str:
    """
    Construct string for IPCS command shell script from template.

    IPCS_EX_SUBCMD template.

    Args:
        session (pyipcs.IpcsSession)
        ipcs_subcmd (str)
    Returns:
        str: constructed string for IPCS subcommand shell script
    """
    # ===================================================================
    # Create and fill dict to unpack for IPCS_EX_SUBCMD template
    # ===================================================================

    shell_strings = {
        "ipcs_subcmd_exec": f"{session._temporary_exec_dsname}({session._ipcs_subcmd_exec_name})",
        "ipcs_subcmd": ipcs_subcmd.strip().replace("'", "''''"),
    }

    # Parse allocations for shell script separating SYSEXEC datasets
    return IPCS_EX_SUBCMD.format(**shell_strings)

def construct_allocations(session: IpcsSession) -> dict[str, str | list[str]]:
    """
    Construct allocations for running the IPCS subcommand

    Args:
        session (pyipcs.IpcsSession)
    Returns:
        str: constructed string for IPCS subcommand shell script
    """

    allocations_copy = copy.deepcopy(session.get_allocations())

    allocations_copy["IPCSDDIR"] = [session.ddir]
    allocations_copy["SYSEXEC"] = [session._temporary_sysexec_dsname]

    if "SYSEXEC" in session.get_allocations():
        allocations_sysexec = copy.deepcopy(session.get_allocations()["SYSEXEC"])
        if isinstance(allocations_sysexec, str):
            allocations_copy["SYSEXEC"].append(allocations_sysexec)
        else:
            allocations_copy["SYSEXEC"].extend(allocations_sysexec)

    return allocations_copy


def run_ipcs_subcmd(session: IpcsSession, ipcs_subcmd: str) -> dict:
    """
    Run IPCS Subcommand Shell Script and save output to a string.

    Args:
        session (pyipcs.IpcsSession)
        ipcs_subcmd (str)
    Returns:
        dict: Dictionary of return code from IPCS subcommand and IPCS subcommand output
        ```
            'rc' (int): return code
            'output' (str): output of IPCS command
        ```
    """
    # =========================================================
    # Fill out IPCS_EX_SUBCMD template and run IPCS command
    # =========================================================

    shell_output = tsocmd(
        construct_ipcs_shell_script(session, ipcs_subcmd),
        construct_allocations(session),
        omvs=True
    )["output"]

    # ===============================================
    # Parse out subcommand output and return code
    # ===============================================

    # Return code is written the line after ___SUBCMD_RC_START___
    # Subommand output is written between lines ___SUBCMD_START___ and ___SUBCMD_END___
    subcmd_start_index = shell_output.find("___SUBCMD_START___")
    return_code_index = shell_output.rfind("___SUBCMD_RC_START___")

    if return_code_index != -1:
        subcmd_end_index = shell_output.rfind("___SUBCMD_END___", 0, return_code_index)
    else:
        subcmd_end_index = -1

    if subcmd_start_index == -1 or subcmd_end_index == -1 or return_code_index == -1:
        raise RuntimeError(
            "Failed To Parse Subcommand Output"
            + " or Return Code In IPCS Subcommand Shell Script Output\n"
            + f"\nIPCS Subcommand: {ipcs_subcmd}\n"
            + f"\nShell Output:\n\n {shell_output}\n"
        )

    return {
        "rc": int(shell_output[return_code_index:].splitlines()[1]),
        "output": shell_output[
            subcmd_start_index + len("___SUBCMD_START___\n") : (subcmd_end_index - 1)
        ],
    }


def run_ipcs_subcmd_outfile(
    session: IpcsSession,
    ipcs_subcmd: str,
    filepath: str,
) -> dict:
    """
    Run IPCS Subcommand Shell Script and save output to a file.

    Creates file for subcommand output.

    Args:
        session (pyipcs.IpcsSession)
        ipcs_subcmd (str)
        filepath (str):
            Filepath for IPCS subcommand output file.
            If filepath is a duplicate will add `'(1)'`,`'(2)'`, etc. for copy.
        encoding (str):
            Optional. Encoding for subcommand output file. Default is `'cp1047'`.
    Returns:
        dict: Dictionary of return code from IPCS subcommand and IPCS subcommand output filepath
        ```
            'rc' (int): return code
            'filepath' (str): filepath of subcommand output file for IPCS subcommand
        ```
    """
    # ===========================================
    # Create File and if exists create copy file
    # ===========================================

    encoding = "cp1047"

    # Split filepath (path/to/my/dir/myfile.txt) into:
    #   Path to the directory (path/to/my/dir/)
    #   Filename with the extension (myfile.txt)
    dirpath, filename_plus_extension = os.path.split(filepath)

    tmp_dirpath = os.path.join(dirpath, "pyipcs_tmp")

    # Create Temp Directory needed to store unprocessed shell output
    os.makedirs(tmp_dirpath, exist_ok=True)

    # Create tmp file to dump unproccessed output to
    tmp_filepath = os.path.join(tmp_dirpath, "output.tmp")

    # Split Filename with extension (myfile.txt) into:
    #   Filename (myfile)
    #   Extension (.txt)
    filename, file_extension = os.path.splitext(filename_plus_extension)

    dup_num = 1
    while os.path.exists(filepath):
        # Create filepath of copy subcommand output
        filename_plus_extension = f"{filename}({dup_num}){file_extension}"
        # Change filepath to copy
        filepath = os.path.join(dirpath, filename_plus_extension)
        dup_num += 1

    # ===============================================================
    # Run IPCS Subcommand
    # Place unformatted IPCS subcommand CLIST output into tmp file
    # Format output and move into subcommand output file
    # ===============================================================

    shell_script = construct_tso_shell_script(
        tso_command=construct_ipcs_shell_script(session, ipcs_subcmd),
        allocations=construct_allocations(session),
        omvs = True
    )

    with (
        open(filepath, "w", encoding=encoding) as outfile_obj,
        open(tmp_filepath, "w+", encoding=encoding) as outfile_obj_tmp,
    ):
        # Run IPCS Subcommand
        # Place unformatted IPCS subcommand CLIST output into tmp file
        with subprocess.Popen(
            shell_script,
            shell=True,
            stdout=outfile_obj_tmp,
            stderr=subprocess.PIPE,
            encoding=encoding,
        ) as process:
            process.wait()
            if process.returncode != 0:
                os.remove(tmp_filepath)
                os.rmdir(tmp_dirpath)
                raise CalledTsoProcessError(
                    construct_ipcs_shell_script(session, ipcs_subcmd),
                    0,
                    process.returncode,
                    process.stderr.read() if process.stderr is not None else None,
                )

        # ====================================================
        # Format output and move into subcommand output file
        # ====================================================

        # Written Label Checks
        found_subcmd_start = False
        found_subcmd_end = False
        found_return_code = False

        outfile_obj_tmp.seek(0)

        # Search for ___SUBCMD_START___ and break
        # The next line will be the start of the output
        for line in outfile_obj_tmp:
            if "___SUBCMD_START___" in line:
                found_subcmd_start = True
                break

        # Store lines in subcommand output file until you hit ___SUBCMD_END___
        # If next line is ___SUBCMD_END___ - remove endline character from final output line
        # The next line after that would then be ___SUBCMD_RC_START___, then the return code
        if found_subcmd_start:
            # Start reading subcmd output
            subcmd_output_line = outfile_obj_tmp.readline()
            for line in outfile_obj_tmp:
                if "___SUBCMD_END___" in line:
                    found_subcmd_end = True
                    if subcmd_output_line[-1] == "\n":
                        outfile_obj.write(subcmd_output_line[:-1])
                    else:
                        outfile_obj.write(subcmd_output_line)
                    break
                outfile_obj.write(subcmd_output_line)
                subcmd_output_line = line

        # Start reading return code
        if found_subcmd_end:
            for line in outfile_obj_tmp:
                if "___SUBCMD_RC_START___" in line:
                    found_return_code = True
                    break

        # If we failed to parse something, delete files and raise error
        if not found_subcmd_start or not found_subcmd_end or not found_return_code:
            outfile_obj_tmp.seek(0)
            shell_output = outfile_obj_tmp.read()
            os.remove(filepath)
            os.remove(tmp_filepath)
            os.rmdir(tmp_dirpath)
            raise RuntimeError(
                "Failed To Parse Subcommand Output"
                + " or Return Code In IPCS Subcommand Shell Script Output\n"
                + f"\nIPCS Subcommand: {ipcs_subcmd}\n"
                + f"\nShell Output:\n\n {shell_output}\n"
            )

        # The next line is the return code
        rc = int(outfile_obj_tmp.readline().strip())

    # Remove temp file and directory before returning
    os.remove(tmp_filepath)
    os.rmdir(tmp_dirpath)
    return {"rc": rc, "filepath": filepath}
