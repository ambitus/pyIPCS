"""
IPCS Subcommand Shell Execution
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import os
import subprocess

if TYPE_CHECKING:
    from ..session import IpcsSession

IPCS_SHELL_SCRIPT = """
# pyIPCS Shell Script
# Shell Script to run an IPCS Subcommand with specified TSO Allocations

# Use parenthesis around shell commands to create a subshell
(

# List all DD names in TSOALLOC 
export TSOALLOC=IPCSDDIR:SYSEXEC{dd_names};

# Must include IPCSDDIR to set DDIR
export IPCSDDIR={ddir};

# Must include SYSEXEC to include pyIPCS SYSEXEC execs
export SYSEXEC={temporary_sysexec_dsname}{other_sysexec_datasets}

# Rest of TSO/E allocation specifications export statements
# Specifications are strings or concatenation of datasets separated by colon
{allocation_exports}

# Executes temporary IPCS subcommand exec
# IPCS subcommand exec excutes IPCS subcommand in parm1
tso "ex  \'{ipcs_subcmd_exec}\'  \'parm1(\'\'{ipcs_subcmd}\'\')\'";

)
"""


def construct_ipcs_shell_script(session: IpcsSession, ipcs_subcmd: str) -> str:
    """
    Construct string for IPCS command shell script from template.

    IPCS_SHELL_SCRIPT template.

    Args:
        session (pyipcs.IpcsSession)
        ipcs_subcmd (str)
    Returns:
        str: constructed string for IPCS subcommand shell script
    """
    # ===================================================================
    # Create and fill dict to unpack for IPCS_SHELL_SCRIPT template
    # ===================================================================

    shell_strings = {
        "ddir": session.ddir,
        "temporary_sysexec_dsname": session._temporary_sysexec_dsname,
        "ipcs_subcmd_exec": f"{session._temporary_exec_dsname}({session._ipcs_subcmd_exec_name})",
        "ipcs_subcmd": ipcs_subcmd.strip().replace("'", "''''"),
    }

    # Parse allocations for shell script separating SYSEXEC datasets
    shell_strings["dd_names"] = ""
    shell_strings["allocation_exports"] = ""
    shell_strings["other_sysexec_datasets"] = ""

    # If dict is empty do nothing
    if session._allocations:
        for dd_name, specification in session._allocations.items():
            # Special condition for SYSEXEC
            if dd_name == "SYSEXEC":
                shell_strings["other_sysexec_datasets"] += ":"
                shell_strings["other_sysexec_datasets"] += ":".join(specification)
                # Skip other conditions to next DD name
                continue
            # If DD name is not SYSEXEC add to TSOALLOC
            shell_strings["dd_names"] += f":{dd_name}"

            # Specifications for TSO Allocations can be strings
            # or a concatenation of datasets in a list
            # Concatenation of lists converted to string of datasets separated by colons
            if isinstance(specification, str):
                shell_strings[
                    "allocation_exports"
                ] += f'export {dd_name}="{specification}";\n'
            elif isinstance(specification, list):
                specification_string = ":".join(specification)
                shell_strings[
                    "allocation_exports"
                ] += f"export {dd_name}={specification_string};\n"
            else:
                raise TypeError(
                    f"DD name {dd_name} specification "
                    + f"must be of type str or list, got {type(specification)}"
                )

    return IPCS_SHELL_SCRIPT.format(**shell_strings)


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
    # Fill out IPCS_SHELL_SCRIPT template and run IPCS command
    # =========================================================
    try:
        shell_output = subprocess.check_output(
            construct_ipcs_shell_script(session, ipcs_subcmd),
            shell=True,
            encoding="ISO-8859-1",
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            "Subprocess Error - Calling IPCS Subcommand CLIST\n"
            + f"\nIPCS Subcommand: {ipcs_subcmd}\n"
            + f"\nReturn Code: {e.returncode}\n"
            + f"\nError output:\n\n {e.output}\n"
        ) from e

    # ===============================================
    # Parse out subcommand output and return code
    # ===============================================

    # Return code is written the line after PYIPCS_SUBCMD_RETURN_CODE
    # Subommand output is written between lines PYIPCS_SUBCMD_START and PYIPCS_SUBCMD_RETURN_CODE
    subcommand_index = shell_output.find("PYIPCS_SUBCMD_START")
    return_code_index = shell_output.rfind("PYIPCS_SUBCMD_RETURN_CODE")

    if subcommand_index == -1 and return_code_index == -1:
        raise RuntimeError(
            "Failed To Find Subcommand Output "
            + "And Return Code In IPCS Subcommand Shell Script Output\n"
            + f"\nIPCS Subcommand: {ipcs_subcmd}\n"
            + f"Shell Output:\n\n {shell_output}\n"
        )

    if return_code_index == -1:
        raise RuntimeError(
            "Failed To Find Return Code In IPCS Subcommand Shell Script Output\n"
            + f"\nIPCS Subcommand: {ipcs_subcmd}\n"
            + f"\nShell Output:\n\n {shell_output}\n"
        )

    if subcommand_index == -1:
        raise RuntimeError(
            "Failed To Find Subcommand Output In IPCS Subcommand Shell Script Output\n"
            + f"\nIPCS Subcommand: {ipcs_subcmd}\n"
            + f"Shell Output:\n\n {shell_output}\n"
        )

    return {
        "rc": int(shell_output[return_code_index:].splitlines()[1]),
        "output": shell_output[
            subcommand_index + len("PYIPCS_SUBCMD_START\n") : return_code_index - 1
        ],
    }


def run_ipcs_subcmd_outfile(
    session: IpcsSession,
    ipcs_subcmd: str,
    filepath: str,
    encoding: str = "cp1047",
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

    with (
        open(filepath, "w", encoding=encoding) as outfile_obj,
        open(tmp_filepath, "w+", encoding=encoding) as outfile_obj_tmp,
    ):
        # Run IPCS Subcommand
        # Place unformatted IPCS subcommand CLIST output into tmp file
        with subprocess.Popen(
            construct_ipcs_shell_script(session, ipcs_subcmd),
            shell=True,
            stdout=outfile_obj_tmp,
            stderr=subprocess.PIPE,
            encoding=encoding,
        ) as process:
            process.wait()
            if process.returncode != 0:
                os.remove(filepath)
                os.remove(tmp_filepath)
                os.rmdir(tmp_dirpath)
                raise RuntimeError(
                    "Subprocess Error - Calling IPCS Subcommand CLIST For Outfile\n"
                    + f"\nIPCS Subcommand: {ipcs_subcmd}\n"
                    + f"\nWriting To Tmp File:{tmp_filepath}"
                    + f"\nReturn Code: {process.returncode}\n"
                    + f"\nError output: \n\n{process.stderr.read().decode()}\n"
                )

        # Format output and move into subcommand output file
        outfile_obj_tmp.seek(0)
        found_subcmd_start = False
        # Search for PYIPCS_SUBCMD_START and break
        # The next line will be the start of the output
        for line in outfile_obj_tmp:
            if "PYIPCS_SUBCMD_START" in line:
                found_subcmd_start = True
                break

        # If we didn't find the subcommand output, delete files and raise error
        if not found_subcmd_start:
            outfile_obj_tmp.seek(0)
            shell_output = outfile_obj_tmp.read()
            os.remove(filepath)
            os.remove(tmp_filepath)
            os.rmdir(tmp_dirpath)
            raise RuntimeError(
                "Failed To Find Subcommand Output In IPCS Subcommand Shell Script Output\n"
                + f"\nIPCS Subcommand: {ipcs_subcmd}\n"
                + f"\nShell Output:\n\n {shell_output}\n"
            )

        # Store lines in subcommand output file until you hit PYIPCS_SUBCMD_RETURN_CODE
        # If next line is PYIPCS_SUBCMD_RETURN_CODE - remove endline character
        # The next line would then be the return code
        found_return_code = False
        subcmd_output_line = outfile_obj_tmp.readline()
        # If subcmd_output line is PYIPCS_SUBCMD_RETURN_CODE the output is empty do nothing
        if "PYIPCS_SUBCMD_RETURN_CODE" in subcmd_output_line:
            found_return_code = True
        else:
            for line in outfile_obj_tmp:
                if "PYIPCS_SUBCMD_RETURN_CODE" in line:
                    found_return_code = True
                    if subcmd_output_line[-1] == "\n":
                        outfile_obj.write(subcmd_output_line[:-1])
                    else:
                        outfile_obj.write(subcmd_output_line)
                    break
                outfile_obj.write(subcmd_output_line)
                subcmd_output_line = line

        # If we didn't find the return code, delete files and raise error
        if not found_return_code:
            outfile_obj_tmp.seek(0)
            shell_output = outfile_obj_tmp.read()
            os.remove(filepath)
            os.remove(tmp_filepath)
            os.rmdir(tmp_dirpath)
            raise RuntimeError(
                "Failed To Find Return Code In IPCS Subcommand Shell Script Output\n"
                + f"\nIPCS Subcommand: {ipcs_subcmd}\n"
                + f"\nShell Output:\n\n {shell_output}\n"
            )

        # The next line is the return code
        rc = int(outfile_obj_tmp.readline().strip())

    # Remove temp file and directory before returning
    os.remove(tmp_filepath)
    os.rmdir(tmp_dirpath)

    return {"rc": rc, "filepath": filepath}
