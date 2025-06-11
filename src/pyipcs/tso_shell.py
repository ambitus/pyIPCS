"""
TSO Shell Functions
"""

import subprocess

TSO_SHELL_SCRIPT = """
# TSO Shell Script
# Shell Script to run TSO/E Command with allocations

# Use parenthesis around shell commands to create a subshell
(

# List all DD names in TSOALLOC export
{tsoalloc};

# TSO/E allocation specifications export statements
# Specifications are strings or concatenation of datasets separated by colon
{allocation_exports}

{tso_or_tsocmd} "{tso_command}";

)
"""


def construct_tso_shell_script(
    tso_command: str,
    allocations: dict[str, str | list[str]],
    omvs: bool,
) -> str:
    """
    Construct string for TSO command shell script from template.

    TSO_SHELL_SCRIPT template.

    Args:
        tso_command (str):
            TSO/E command to run
        allocations (dict[str,str|list[str]]):
            Optional. Dictionary of allocations where keys are DD names
            and values are string data set allocation requests or lists of cataloged datasets.
        omvs (bool):
            If `True` uses the tso `'-o'` flag to issue a command through the OMVS interface.
            If `False` uses the tso `'-t'` flag to issue a command through a TSO/E service routine.
            The `'-t'` flag will set up a mini TSO/E environment in a new address space.
            The `'-t'` flag can be used to issue authorized TSO/E commands.
    Returns:
        str: constructed string for TSO command shell script
    """
    # =========================================
    # Create Dict to fill out string template
    # =========================================

    shell_strings = {
        "tso_command": tso_command.strip(),
        "tso_or_tsocmd": "tso" if omvs else "tsocmd",
    }

    # =======================================================
    # If there are allocations add them to template strings
    # =======================================================

    if allocations:
        shell_strings["tsoalloc"] = "export TSOALLOC="
        shell_strings["tsoalloc"] += ":".join(allocations.keys())
    else:
        shell_strings["tsoalloc"] = ""

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
    return TSO_SHELL_SCRIPT.format(**shell_strings)


class CalledTsoProcessError(Exception):
    """
    Custom exception for invalid return code from a TSO command shell script
    """

    def __init__(
        self,
        tso_command: str,
        expected_rc: int,
        rc: int,
        stderr: str | None,
    ):
        """
        Constructor for invalid return code from a TSO command exception

        Args:
            tso_command (str):
                TSO/E command that was attempted
            expected_rc (int):
                Expected return code from TSO command shell script
            rc (int):
                Return code from TSO command shell script
            stderr (str|None):
                Error output from TSO command shell script.
                `None` if there is no error output
        Returns:
            None
        """
        exception_str = (
            "Unexpected TSO Subprocess Error - Invalid Return Code\n"
            + f"\nTSO Command: {tso_command}\n"
            + f"\nExpected Return Code: {expected_rc}\n"
            + f"\nActual Return Code: {rc}\n"
        )
        if stderr is not None:
            exception_str += f"\nError Output: \n\n{stderr}\n"
        super().__init__(exception_str)


def tsocmd(
    tso_command: str,
    allocations: dict[str, str | list[str]] = {},
    omvs: bool = False,
    check: bool = True,
    expected_rc: int = 0,
) -> dict:
    """
    Run a TSO/E Command and store output in a string

    Args:
        tso_command (str):
            TSO/E command to run
        allocations (dict[str,str|list[str]]):
            Optional. Dictionary of allocations where keys are DD names
            and values are string data set allocation requests or lists of cataloged datasets.
            Default is an empty dictionary.
        omvs (bool):
            Optional.
            If `True` uses the `tso` shell command to issue a command through the OMVS interface.
            If `False` uses the `tsocmd` shell command 
            to issue a command through a TSO/E service routine.
            The `tso` shell command will set up a mini TSO/E environment in a new address space.
            The `tsocmd` shell command can be used to issue authorized TSO/E commands.
            Default is `False`.
        check (bool):
            If `True`, return error for unexpected return code as specified by `expected_rc`
            Default is `True`.
        expected_rc (int):
            Specify expected return code.
            Default is `0`.
    Returns:
        dict: Dictionary containing output, return code and standard error.
        ```
            'rc' (int): Return code of TSO shell script
            'output' (str): Output of TSO shell script combined with possible error output
        ```
    """
    # ======================
    # Form TSO shell script
    # ======================

    shell_script = construct_tso_shell_script(
        tso_command=tso_command,
        allocations=allocations,
        omvs=omvs,
    )

    # =============================
    # Run TSO Command from shell
    # =============================

    completed_process = subprocess.run(
        shell_script,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="ISO-8859-1",
        check=False,
    )

    # =======================================================================
    # If check is specified and not the expected return code - raise error
    # =======================================================================

    if check and completed_process.returncode != expected_rc:
        raise CalledTsoProcessError(
            tso_command,
            expected_rc,
            completed_process.returncode,
            completed_process.stdout,
        )

    return {
        "rc": completed_process.returncode,
        "output": completed_process.stdout,
    }

def hrecall(
    dsname: str,
    allocations: dict[str, str | list[str]] = {},
):
    """
    Use HRECALL TSO command to recall migrated dataset

    Args:
        dsname (str):
            Dataset name for dataset you want to recall
        allocations (dict[str,str|list[str]]):
            Optional. Dictionary of allocations where keys are DD names
                and values are string data set allocation requests or lists of cataloged datasets.
                Default is an empty dictionary.
    Returns:
        None
    """
    tsocmd(
        f"HRECALL '{dsname}' WAIT EXTENDRC",
        allocations=allocations,
        check=False,
    )
