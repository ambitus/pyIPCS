"""
TSO Command Function
"""

import subprocess

TSO_SHELL_SCRIPT = """
# TSO Shell Script
# Shell Script to run TSO/E Command with allocations

# Use parenthesis around shell commands to create a subshell
(

# List all DD names in TSOALLOC 
export TSOALLOC={dd_names};

# TSO/E allocation specifications export statements
# Specifications are strings or concatenation of datasets separated by colon
{allocation_exports}

tsocmd "{tso_command}";

)
"""

TSO_SHELL_COMMAND = """
# TSO Shell Command
# Shell Command to run TSO/E Command withouts allocations

# Use parenthesis around shell commands to create a subshell
(

tsocmd "{tso_command}";

)

"""


def tso_cmd(
    tso_command: str,
    allocations: dict[str, str | list[str]] = {},
) -> str:
    """
    Run a TSO/E Command

    Uses TSO_SHELL_SCRIPT template if there are allocations

    Use TSO_SHELL_COMMAND template if there are not allocations needed

    Args:
        tso_command (str):
            TSO/E command to run
    Returns:
        str : shell output from running TSO/E command
    """
    # =========================================
    # Create Dict to fill out string template
    # =========================================

    shell_strings = {"tso_command": tso_command.strip()}

    # =======================================================
    # If there are allocations add them to template strings
    # =======================================================

    if allocations != {}:

        shell_strings["dd_names"] = ":".join(allocations.keys())

        shell_strings["allocation_exports"] = ""
        for dd_name, specification in allocations.items():

            # Specifications for TSO Allocations can be strings
            #   or a concatenation of datasets in a list
            # Concatenation of lists converted to string
            #   of datasets separated by colons
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
                    f"DD name {dd_name} specification"
                    + f" must be of type str or list, got {type(specification)}"
                )

        shell_script = TSO_SHELL_SCRIPT.format(**shell_strings)
    else:
        shell_script = TSO_SHELL_COMMAND.format(**shell_strings)

    # =============================
    # Run TSO Command from shell
    # =============================
    try:
        shell_output = subprocess.check_output(
            shell_script,
            shell=True,
            encoding="ISO-8859-1",
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            "Subprocess Error - Running General TSO Command\n"
            + f"\nTSO Command: {tso_command}\n"
            + f"\nReturn Code: {e.returncode}\n"
            + f"\nError output: \n\n{e.output}\n"
        ) from e

    return shell_output


def hrecall(
    dsname: str,
    allocations: dict[str, str | list[str]] = {},
):
    """
    Use HRECALL TSO command to recall migrated dataset

    Args:
        dsname (str):
            Dataset name for dataset you want to recall
    Returns:
        None
    """
    try:
        tso_cmd(f"HRECALL '{dsname}' WAIT EXTENDRC", allocations)
    except Exception:
        pass
