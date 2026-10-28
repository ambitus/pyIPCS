"""
Test running IPCS subcommands
"""

import tempfile

import pytest


def test_subcmd_defaults(default_ddir, allocations, ipcs_subcmd_job):
    """Test that local_defaults are applied for a single subcommand run."""
    subcmd = "SETDEF LIST"

    # Baseline: default LENGTH(4)
    response = default_ddir.run(subcmd)
    assert response.rc < 8
    assert response.output.find("LENGTH(4)") != -1

    # With local_defaults: LENGTH(8) should appear
    job_outputs = ipcs_subcmd_job(
        ddir=default_ddir,
        subcmds=[subcmd],
        allocations=allocations,
        local_defaults="LENGTH(8) NOCONFIRM",
    )
    response = default_ddir.run(subcmd, local_defaults="LENGTH(8) NOCONFIRM")
    assert response.rc < 8
    assert response.output.find("LENGTH(8)") != -1
    assert response.output.find("NOCONFIRM") != -1
    assert response.output == job_outputs[0], f"Subcommand: {subcmd}"

    # Confirm local_defaults did not persist
    response = default_ddir.run(subcmd)
    assert response.rc < 8
    assert response.output.find("LENGTH(4)") != -1


@pytest.mark.dump
def test_subcmd_defaults_dump(dump, dump_ddir, allocations, ipcs_subcmd_job):
    """Test that local_defaults are applied alongside a dump for a single subcommand run."""
    subcmd = "SETDEF LIST"

    # Baseline: no dump set globally
    dump_ddir.setdef_global(defaults="NODSNAME LENGTH(4)")
    response = dump_ddir.run(subcmd)
    assert response.rc < 8
    assert response.output.find("NODSNAME") != -1
    assert response.output.find("LENGTH(4)") != -1

    # With dump + local_defaults: DSNAME and LENGTH(8) should appear
    job_outputs = ipcs_subcmd_job(
        ddir=dump_ddir,
        subcmds=[subcmd],
        allocations=allocations,
        dump=dump,
        local_defaults="LENGTH(8)",
    )
    response = dump_ddir.run(subcmd, dump=dump, local_defaults="LENGTH(8)")
    assert response.rc < 8
    assert response.output.find(f"DSNAME('{dump.dsname}')") != -1
    assert response.output.find("LENGTH(8)") != -1
    assert response.output == job_outputs[0], f"Subcommand: {subcmd}"

    # Confirm local_defaults did not persist
    response = dump_ddir.run(subcmd)
    assert response.rc < 8
    assert response.output.find("NODSNAME") != -1
    assert response.output.find("LENGTH(4)") != -1


def test_subcmd_output(default_ddir, allocations, ipcs_subcmd_job):
    """Test subcommand output against job output."""

    subcmds = ["SETDEF LIST", "LISTDUMP"]

    job_outputs = ipcs_subcmd_job(
        ddir=default_ddir,
        subcmds=subcmds,
        allocations=allocations,
    )
    for subcmd, expected in zip(subcmds, job_outputs):
        response = default_ddir.run(subcmd)
        assert response.output == expected, f"Subcommand: {subcmd}"
        response = default_ddir.run(subcmd, authorized=True)
        assert response.output == expected, f"Subcommand - Authorized: {subcmd}"
        with tempfile.TemporaryFile(mode="w+") as f:
            response = default_ddir.run(subcmd, output=f)
            assert response.output is None, f"Subcommand - Output Param: {subcmd}"
            f.seek(0)
            assert f.read() == expected, f"Subcommand - File Output: {subcmd}"


@pytest.mark.dump
def test_subcmd_output_dump(dump, dump_ddir, allocations, ipcs_subcmd_job):
    """Test subcommand output against job output with a source dump."""

    subcmds = ["LIST TITLE", "STATUS WORKSHEET", "STATUS REGISTERS"]

    job_outputs = ipcs_subcmd_job(
        ddir=dump_ddir,
        subcmds=subcmds,
        allocations=allocations,
        dump=dump,
    )
    for subcmd, expected in zip(subcmds, job_outputs):
        response = dump_ddir.run(subcmd, dump=dump)
        assert response.output == expected, f"Subcommand: {subcmd}"
        response = dump_ddir.run(subcmd, dump=dump, authorized=True)
        assert response.output == expected, f"Subcommand - Authorized: {subcmd}"
        with tempfile.TemporaryFile(mode="w+") as f:
            response = dump_ddir.run(subcmd, dump=dump, output=f)
            assert response.output is None, f"Subcommand - Output Param: {subcmd}"
            f.seek(0)
            assert f.read() == expected, f"Subcommand - File Output: {subcmd}"
