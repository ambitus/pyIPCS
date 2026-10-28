"""
TSO Shell Script
"""

_TSO_SHELL_SCRIPT = """
# TSO Shell Script
# Shell Script to run TSO/E Command with allocations

# Use parenthesis around shell commands to create a subshell
(

# List all DD names in TSOALLOC export
{tsoalloc};

# TSO/E allocation specifications export statements
# Specifications are strings or concatenation of datasets separated by colon
{allocation_exports}

{tso_or_tsocmd} "{cmd}"

)
"""


def tso_shell_script(
    cmd: str,
    authorized: bool,
    allocations: dict[str, str | list[str]],
) -> str:
    """
    Build the TSO shell script string from the given parameters.

    Args:
        cmd: TSO/E command to run.
        authorized: If ``True``, uses the ``tsocmd`` shell command which can issue
            authorized TSO/E commands via the TSO/E terminal monitor program
            (IKJEFT01). If ``False``, uses the ``tso`` shell command which sets up
            a mini TSO/E environment in a new address space through the OMVS
            interface.
        allocations: Dictionary of allocations where keys are DD names and values
            are string data set allocation requests or lists of cataloged datasets.

    Returns:
        str: TSO shell script.
    """
    tsoalloc = "export TSOALLOC=" + ":".join(allocations.keys()) if allocations else ""
    allocation_exports = "\n".join(
        (
            f'export {dd_name}="{spec}";'
            if isinstance(spec, str)
            else f"export {dd_name}={':'.join(spec)};"
        )
        for dd_name, spec in allocations.items()
    )
    return _TSO_SHELL_SCRIPT.format(
        tsoalloc=tsoalloc,
        allocation_exports=allocation_exports,
        cmd=cmd,
        tso_or_tsocmd="tsocmd" if authorized else "tso",
    )
