"""
Command handler functions for the pyIPCS CLI.
"""

from __future__ import annotations

import argparse
import sys
import json
from ..dump import IpcsDump
from ..ddir import IpcsDdir


def _load_allocations(path: str | None) -> dict[str, str | list[str]] | None:
    """Load allocations from a JSON file, or return ``None`` to use defaults.

    The JSON file must contain an object whose keys are DD names and values are
    string data set allocation requests or lists of cataloged dataset names::

        {
            "IPCSPARM": "SYS1.PARMLIB",
            "SYSPROC": ["SYS1.SBLSCLI0", "MY.SBLSCLI0"]
        }

    Args:
        path: Path to the JSON file, or ``None`` to use defaults.

    Returns:
        dict[str, str | list[str]] | None: Allocations dictionary, or ``None``
        if ``path`` is ``None``.

    Raises:
        argparse.ArgumentTypeError: If the file cannot be read or is not valid.
    """
    if path is None:
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def handle_create_ddir(args: argparse.Namespace) -> None:
    """Handle the ``create-ddir`` command."""
    ddir = IpcsDdir(
        args.ddir,
        driver=args.driver,
        allocations=_load_allocations(args.allocations),
        ddir_parms=args.ddir_parms,
    )
    if ddir.response is not None:
        print(ddir.response.output, end="")
        sys.exit(ddir.response.rc)
    sys.exit(0)


def handle_setdef_global(args: argparse.Namespace) -> None:
    """Handle the ``setdef-global`` command."""
    ddir = IpcsDdir(
        args.ddir,
        driver=args.driver,
        allocations=_load_allocations(args.allocations),
    )
    response = ddir.setdef_global(
        dump=IpcsDump(args.dump) if args.dump else None,
        defaults=args.defaults,
    )
    print(response.output, end="")
    sys.exit(response.rc)


def handle_init_dump(args: argparse.Namespace) -> None:
    """Handle the ``init-dump`` command."""
    dump = IpcsDump(args.dump)
    ddir = IpcsDdir(
        args.ddir,
        driver=args.driver,
        allocations=_load_allocations(args.allocations),
    )
    response = ddir.init_dump(dump)
    if response.rc >= 8:
        print(
            "Dump initialization unsuccessful: "
            "Error encountered while running the 'STATUS' subcommand to initialize dump."
        )
        sys.exit(response.rc)
    if dump.dsname not in ddir.sources():
        print(
            "Dump initialization unsuccessful: "
            "Dump not listed as a source description."
        )
        sys.exit(1)
    print("Dump initialization successful.")
    sys.exit(0)


def handle_run(args: argparse.Namespace) -> None:
    """Handle the ``run`` command."""
    ddir = IpcsDdir(
        args.ddir,
        driver=args.driver,
        allocations=_load_allocations(args.allocations),
    )
    response = ddir.run(
        args.subcmd,
        dump=IpcsDump(args.dump) if args.dump else None,
        authorized=args.auth,
        local_defaults=args.local_defaults,
        output=sys.stdout,
    )
    sys.exit(response.rc)
