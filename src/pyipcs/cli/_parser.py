"""
Subparser registration for the pyIPCS CLI.
"""

from __future__ import annotations

import argparse

from ._commands import (
    handle_create_ddir,
    handle_setdef_global,
    handle_init_dump,
    handle_run,
)


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add the shared ``dsname`` positional arg and ``--driver`` / ``--allocations`` flags.

    Args:
        parser: The subparser to add arguments to.
    """
    parser.add_argument("ddir", help="Data set name of the DDIR.")
    parser.add_argument(
        "--driver",
        metavar="DSNAME",
        default=None,
        help="Driver data set name to use for the DDIR.",
    )
    parser.add_argument(
        "--allocations",
        metavar="FILE",
        default=None,
        help=(
            "Path to a JSON file containing custom TSO/E allocations. "
            "The file must be a JSON object where keys are DD names and values "
            "are string allocation requests or lists of dataset names. "
            'Defaults to {"IPCSPARM": "SYS1.PARMLIB", "SYSPROC": "SYS1.SBLSCLI0"}.'
        ),
    )


def parser_create_ddir(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Register the ``create-ddir`` subparser."""
    p = subparsers.add_parser(
        "create-ddir",
        help="Create a dump directory (DDIR) by running BLSCDDIR, or open an existing one.",
    )
    _add_common_args(p)
    p.add_argument(
        "--ddir-parms",
        dest="ddir_parms",
        default=None,
        help=(
            "Additional parameters to pass to the BLSCDDIR CLIST. "
            "Ignored if the DDIR already exists."
        ),
    )
    p.set_defaults(func=handle_create_ddir)


def parser_setdef_global(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Register the ``setdef-global`` subparser."""
    p = subparsers.add_parser(
        "setdef-global",
        help="Set global defaults on an existing DDIR.",
    )
    _add_common_args(p)
    p.add_argument(
        "--dump",
        metavar="DSNAME",
        default=None,
        help="Source dump data set name to set as the global default.",
    )
    p.add_argument(
        "--defaults",
        default=None,
        help="Additional parameters to pass to the setdef-global command.",
    )
    p.set_defaults(func=handle_setdef_global)


def parser_init_dump(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Register the ``init-dump`` subparser."""
    p = subparsers.add_parser(
        "init-dump",
        help="Initialize a dump data set in an existing DDIR by running STATUS.",
    )
    _add_common_args(p)
    p.add_argument(
        "dump", metavar="DSNAME", help="Source dump data set name to initialize."
    )
    p.set_defaults(func=handle_init_dump)


def parser_run(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Register the ``run`` subparser."""
    p = subparsers.add_parser(
        "run",
        help="Run an IPCS subcommand against an existing DDIR.",
    )
    _add_common_args(p)
    p.add_argument("subcmd", help="IPCS subcommand to run.")
    p.add_argument(
        "--dump",
        metavar="DSNAME",
        default=None,
        help="Source dump data set name for this invocation.",
    )
    p.add_argument(
        "--auth",
        action="store_true",
        default=False,
        help="Run the subcommand in an authorized environment.",
    )
    p.add_argument(
        "--local-defaults",
        default=None,
        help="Parameters for SETDEF NOLIST LOCAL run before the subcommand.",
    )
    p.set_defaults(func=handle_run)
