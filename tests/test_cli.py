"""
Test pyIPCS CLI command handlers
"""

import json
import tempfile
from argparse import Namespace

import pytest

from pyipcs._util import check_dataset_exists
from pyipcs.cli._commands import (
    handle_create_ddir,
    handle_init_dump,
    handle_setdef_global,
    handle_run,
)

# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def allocations_path(allocations):
    """Write the allocations dict to a temp JSON file and yield its path.

    Yields ``None`` when ``allocations`` is ``None`` so callers omit the flag.
    """
    if allocations is None:
        yield None
        return
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=True, encoding="utf-8"
    ) as f:
        json.dump(allocations, f)
        f.flush()
        yield f.name


# ==============================================================================
# Helper Functions
# ==============================================================================


def _exit_code(exc: pytest.ExceptionInfo[SystemExit]) -> int:
    """Return the integer exit code from a SystemExit ExceptionInfo."""
    code = exc.value.code
    assert isinstance(code, int)
    return code


# ==============================================================================
# Tests
# ==============================================================================


def test_handle_create_ddir(ddir_dsname, allocations_path, ddir_parms):
    """handle_create_ddir should create the DDIR and exit 0."""
    assert not check_dataset_exists(ddir_dsname)
    args = Namespace(
        ddir=ddir_dsname,
        driver=None,
        allocations=allocations_path,
        ddir_parms=ddir_parms,
    )

    with pytest.raises(SystemExit) as exc:
        handle_create_ddir(args)

    assert _exit_code(exc) == 0
    assert check_dataset_exists(ddir_dsname)


def test_handle_create_ddir_existing(default_ddir, allocations_path):
    """handle_create_ddir should open an existing DDIR without error and exit 0."""
    assert check_dataset_exists(default_ddir.dsname)
    args = Namespace(
        ddir=default_ddir.dsname,
        driver=None,
        allocations=allocations_path,
        ddir_parms=None,
    )

    with pytest.raises(SystemExit) as exc:
        handle_create_ddir(args)

    assert _exit_code(exc) == 0


def test_handle_setdef_global(default_ddir, allocations_path, capsys):
    """handle_setdef_global should set defaults and exit with rc < 8."""
    args = Namespace(
        ddir=default_ddir.dsname,
        driver=None,
        allocations=allocations_path,
        dump=None,
        defaults=None,
    )

    with pytest.raises(SystemExit) as exc:
        handle_setdef_global(args)

    assert _exit_code(exc) < 8
    assert "LENGTH(4)" in capsys.readouterr().out


def test_handle_setdef_global_with_defaults(default_ddir, allocations_path, capsys):
    """handle_setdef_global should forward defaults and exit with rc < 8."""
    args = Namespace(
        ddir=default_ddir.dsname,
        driver=None,
        allocations=allocations_path,
        dump=None,
        defaults="LENGTH(8) NOCONFIRM",
    )

    with pytest.raises(SystemExit) as exc:
        handle_setdef_global(args)

    assert _exit_code(exc) < 8
    out = capsys.readouterr().out
    assert "LENGTH(8)" in out
    assert "NOCONFIRM" in out


@pytest.mark.dump
def test_handle_init_dump(dump, default_ddir, allocations_path, capsys):
    """handle_init_dump should initialize the dump in the DDIR and exit 0."""
    args = Namespace(
        ddir=default_ddir.dsname,
        driver=None,
        allocations=allocations_path,
        dump=dump.dsname,
    )

    with pytest.raises(SystemExit) as exc:
        handle_init_dump(args)

    assert _exit_code(exc) == 0
    assert "Dump initialization successful." in capsys.readouterr().out
    assert dump.dsname in default_ddir.sources()


@pytest.mark.dump
def test_handle_setdef_global_with_dump(
    dump, dump_ddir_dsname, allocations_path, capsys
):
    """handle_setdef_global should set the dump as global default when dump is given."""
    args = Namespace(
        ddir=dump_ddir_dsname,
        driver=None,
        allocations=allocations_path,
        dump=dump.dsname,
        defaults=None,
    )

    with pytest.raises(SystemExit) as exc:
        handle_setdef_global(args)

    assert _exit_code(exc) < 8
    assert f"DSNAME('{dump.dsname}')" in capsys.readouterr().out


def test_handle_run(default_ddir, allocations_path, capsys):
    """handle_run should run the subcommand and exit with rc < 8."""
    args = Namespace(
        ddir=default_ddir.dsname,
        driver=None,
        allocations=allocations_path,
        subcmd="SETDEF LIST",
        dump=None,
        auth=False,
        local_defaults=None,
    )

    with pytest.raises(SystemExit) as exc:
        handle_run(args)

    assert _exit_code(exc) < 8
    assert "LENGTH(4)" in capsys.readouterr().out


@pytest.mark.dump
def test_handle_run_with_dump(dump, dump_ddir_dsname, allocations_path, capsys):
    """handle_run should include the dump in the subcommand run when dump is given."""
    args = Namespace(
        ddir=dump_ddir_dsname,
        driver=None,
        allocations=allocations_path,
        subcmd="SETDEF LIST",
        dump=dump.dsname,
        auth=False,
        local_defaults=None,
    )

    with pytest.raises(SystemExit) as exc:
        handle_run(args)

    assert _exit_code(exc) < 8
    assert f"DSNAME('{dump.dsname}')" in capsys.readouterr().out


def test_handle_run_authorized(default_ddir, allocations_path):
    """handle_run should run the subcommand in an authorized environment."""
    args = Namespace(
        ddir=default_ddir.dsname,
        driver=None,
        allocations=allocations_path,
        subcmd="SETDEF LIST",
        dump=None,
        auth=True,
        local_defaults=None,
    )

    with pytest.raises(SystemExit) as exc:
        handle_run(args)

    assert _exit_code(exc) < 8


def test_handle_run_local_defaults(default_ddir, allocations_path, capsys):
    """handle_run should apply local_defaults for this run only."""
    args = Namespace(
        ddir=default_ddir.dsname,
        driver=None,
        allocations=allocations_path,
        subcmd="SETDEF LIST",
        dump=None,
        auth=False,
        local_defaults="LENGTH(8) NOCONFIRM",
    )

    with pytest.raises(SystemExit) as exc:
        handle_run(args)

    assert _exit_code(exc) < 8
    out = capsys.readouterr().out
    assert "LENGTH(8)" in out
    assert "NOCONFIRM" in out
