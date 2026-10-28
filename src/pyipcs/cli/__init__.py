"""
pyIPCS command-line interface entry point.
"""

from __future__ import annotations

import argparse

from ._parser import (
    parser_create_ddir,
    parser_setdef_global,
    parser_init_dump,
    parser_run,
)


def main() -> None:
    """CLI entry point for the ``pyipcs`` command."""
    parser = argparse.ArgumentParser(
        prog="pyipcs",
        description="pyIPCS command-line interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="The process exit code equals the TSO/IPCS response return code.",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="command")
    subparsers.required = True

    parser_create_ddir(subparsers)
    parser_setdef_global(subparsers)
    parser_init_dump(subparsers)
    parser_run(subparsers)

    args = parser.parse_args()
    args.func(args)
