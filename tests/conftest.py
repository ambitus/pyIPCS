"""
Pytest configuration for pyIPCS
"""

import json
import warnings
from typing import Iterable, Optional
from collections.abc import Generator
import pytest

from zoautil_py import datasets, jobs
from pyipcs import IpcsDump, IpcsDdir
from pyipcs._util import tso_profile_prefix, check_dataset_exists
from pyipcs.driver import default_driver_dsname

# ==============================================================================
# Helper Functions
# ==============================================================================


def cleanup_test_datasets(standard: list[str] = [], ddirs: list[str] = []) -> None:
    """Delete test datasets and DDIRs, then verify all were removed.

    Attempts to delete every dataset and DDIR in the provided lists. Issues a
    warning for each deletion that returns a non-zero RC. After all deletions
    are attempted, checks for any datasets that still exist and calls
    ``pytest.exit`` with the full list of survivors if any remain.

    Args:
        standard: List of standard dataset names to delete via ``datasets.delete``.
        ddirs: List of DDIR dataset names to delete via ``IpcsDdir._delete_ddir``.
    """
    # First pass — attempt deletions, warn on non-zero RC
    for dsname in standard:
        if check_dataset_exists(dsname):
            rc = datasets.delete(dsname)
            if rc != 0:
                warnings.warn(
                    f"Data set deletion exited with non-zero return code for test data set '{dsname}': rc={rc}"
                )

    for dsname in ddirs:
        if check_dataset_exists(dsname):
            response = IpcsDdir._delete_ddir(dsname)
            if response.rc != 0:
                warnings.warn(
                    f"Data set deletion exited with non-zero return code for test data set '{dsname}': rc={response.rc}"
                )

    # Second pass — collect anything that still exists
    still_exist: list[str] = []
    for dsname in standard:
        if check_dataset_exists(dsname):
            still_exist.append(dsname)
    for dsname in ddirs:
        if check_dataset_exists(dsname):
            still_exist.append(dsname)

    if still_exist:
        pytest.exit(
            "Failed to remove the following test data sets:\n"
            + "\n".join(f"  {ds}" for ds in still_exist)
        )


# ==============================================================================
# Stash Keys
# ==============================================================================

DUMP_DSNAME_KEY: pytest.StashKey[str | None] = pytest.StashKey()
ALLOCATIONS_KEY: pytest.StashKey[dict[str, str | list[str]] | None] = pytest.StashKey()
DDIR_PARMS_KEY: pytest.StashKey[str | None] = pytest.StashKey()
HLQ_KEY: pytest.StashKey[str] = pytest.StashKey()
DRIVER_DSNAME_KEY: pytest.StashKey[str] = pytest.StashKey()
DEF_DDIR_DSNAME_KEY: pytest.StashKey[str] = pytest.StashKey()
DUMP_DDIR_DSNAME_KEY: pytest.StashKey[str] = pytest.StashKey()
TEMP_DSNAME_KEY: pytest.StashKey[str] = pytest.StashKey()

# ==============================================================================
# Pytest Options
# ==============================================================================


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--allocations",
        action="store",
        default=None,
        metavar="FILE",
        help=(
            "Path to a JSON file containing custom TSO/E allocations. "
            "The file must be a JSON object where keys are DD names and values "
            "are string allocation requests or lists of dataset names. "
            'Defaults to {"IPCSPARM": "SYS1.PARMLIB", "SYSPROC": "SYS1.SBLSCLI0"}.'
        ),
    )
    parser.addoption(
        "--ddir-parms",
        action="store",
        default=None,
        metavar="PARMS",
        help=(
            "Additional parameters to pass to the BLSCDDIR CLIST when creating DDIRs in tests. "
            "Default is None."
        ),
    )
    parser.addoption(
        "--dump",
        action="store",
        default=None,
        metavar="DSNAME",
        help="Data set name of the dump to use in tests.",
    )
    parser.addoption(
        "--hlq",
        action="store",
        default=None,
        metavar="HLQ",
        help=(
            "High-level qualifier to use in tests. "
            "Defaults to <TSO profile prefix>.PYTEST."
        ),
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    # Skip tests marked with ``dump`` when no test dump data set was provided.
    if config.stash[DUMP_DSNAME_KEY] is None:
        skip = pytest.mark.skip(reason="--dump not provided")
        for item in items:
            if item.get_closest_marker("dump"):
                item.add_marker(skip)


def pytest_configure(config: pytest.Config) -> None:

    # Setup markers
    config.addinivalue_line(
        "markers", "dump: marks tests that make use of a provided test dump"
    )

    # Load allocations from optionally provided JSON file
    allocations_path = config.getoption("--allocations")
    if allocations_path is None:
        config.stash[ALLOCATIONS_KEY] = None
    else:
        with open(allocations_path, encoding="utf-8") as f:
            config.stash[ALLOCATIONS_KEY] = json.load(f)

    config.stash[DDIR_PARMS_KEY] = config.getoption("--ddir-parms")
    config.stash[DUMP_DSNAME_KEY] = config.getoption("--dump")

    hlq = config.getoption("--hlq") or f"{tso_profile_prefix()}.PYTEST"
    config.stash[HLQ_KEY] = hlq
    config.stash[DRIVER_DSNAME_KEY] = f"{hlq}.DRIVER"
    config.stash[DEF_DDIR_DSNAME_KEY] = f"{hlq}.TESTDDIR"
    config.stash[DUMP_DDIR_DSNAME_KEY] = f"{hlq}.DUMPDDIR"
    config.stash[TEMP_DSNAME_KEY] = f"{hlq}.TEMPDSN"

    # Cleanup Dump DDIR if needed
    cleanup_test_datasets(ddirs=[config.stash[DUMP_DDIR_DSNAME_KEY]])

    # Initialize dump if provided to reuse over multiple tests
    dump_dsname = config.stash[DUMP_DSNAME_KEY]
    if dump_dsname is not None:
        # Initialize dump
        dump = IpcsDump(dump_dsname)
        with IpcsDdir(
            config.stash[DUMP_DDIR_DSNAME_KEY],
            allocations=config.stash[ALLOCATIONS_KEY],
            ddir_parms=config.stash[DDIR_PARMS_KEY],
        ) as pytest_ddir:
            pytest_ddir.init_dump(dump)
            if dump.dsname not in pytest_ddir.sources():
                pytest.exit(
                    f"Failed to initialize '{dump.dsname}' in test DDIR '{config.stash[DUMP_DDIR_DSNAME_KEY]}'"
                )

        # Check DDIR exists for rest of tests
        if not check_dataset_exists(config.stash[DUMP_DDIR_DSNAME_KEY]):
            pytest.exit(
                f"Test dump DDIR '{config.stash[DUMP_DDIR_DSNAME_KEY]}' did not persist after dump initialization"
            )

    # Cleanup the rest of the test data sets if needed
    cleanup_test_datasets(
        standard=[
            default_driver_dsname(),
            config.stash[DRIVER_DSNAME_KEY],
            config.stash[TEMP_DSNAME_KEY],
        ],
        ddirs=[config.stash[DEF_DDIR_DSNAME_KEY]]
        + [
            ds.name
            for ds in datasets.list_vsam_datasets(
                f"{tso_profile_prefix()}.PYIPCS.DDIR*"
            )
        ]
        + [ds.name for ds in datasets.list_vsam_datasets(f"{hlq}.DDIR*")],
    )


# ==============================================================================
# Standard Fixtures
# ==============================================================================


@pytest.fixture(scope="session")
def allocations(request: pytest.FixtureRequest) -> dict[str, str | list[str]] | None:
    """Allocations dict loaded from the JSON file passed via ``--allocations``."""
    return request.config.stash[ALLOCATIONS_KEY]


@pytest.fixture(scope="session")
def ddir_parms(request: pytest.FixtureRequest) -> str | None:
    """Additional BLSCDDIR parameters passed via ``--ddir-parms``."""
    return request.config.stash[DDIR_PARMS_KEY]


@pytest.fixture(scope="session")
def dump_dsname(request: pytest.FixtureRequest) -> str | None:
    """Dump data set name str passed via --dump."""
    return request.config.stash[DUMP_DSNAME_KEY]


@pytest.fixture(scope="session")
def hlq(request: pytest.FixtureRequest) -> str:
    """High-level qualifier passed via --hlq, defaulting to <tso_profile_prefix>.PYTEST."""
    return request.config.stash[HLQ_KEY]


@pytest.fixture(scope="session")
def driver_dsname(request: pytest.FixtureRequest) -> str:
    """Data set name for the non-default test pyIPCS driver."""
    return request.config.stash[DRIVER_DSNAME_KEY]


@pytest.fixture(scope="session")
def ddir_dsname(request: pytest.FixtureRequest) -> str:
    """Data set name for the general-purpose test DDIR."""
    return request.config.stash[DEF_DDIR_DSNAME_KEY]


@pytest.fixture(scope="session")
def dump_ddir_dsname(request: pytest.FixtureRequest) -> str:
    """Data set name for the dump test DDIR."""
    return request.config.stash[DUMP_DDIR_DSNAME_KEY]


@pytest.fixture(scope="session")
def temp_dsname(request: pytest.FixtureRequest) -> str:
    """Data set name for a temporary test data set."""
    return request.config.stash[TEMP_DSNAME_KEY]


# ==============================================================================
# Setup/Cleanup Fixtures
# ==============================================================================


@pytest.fixture(scope="session", autouse=True)
def environment(
    request: pytest.FixtureRequest,
    dump_ddir_dsname: str,
) -> None:
    """Test session setup and cleanup."""

    def _cleanup() -> None:
        # Delete DDIR with provided test dump
        cleanup_test_datasets(ddirs=[dump_ddir_dsname])

    request.addfinalizer(_cleanup)


@pytest.fixture(autouse=True)
def reset_state(
    request: pytest.FixtureRequest,
    hlq: str,
    driver_dsname: str,
    temp_dsname: str,
    ddir_dsname: str,
) -> None:
    """Delete leftover test data sets after each test."""

    def _cleanup() -> None:
        cleanup_test_datasets(
            standard=[default_driver_dsname(), driver_dsname, temp_dsname],
            ddirs=[ddir_dsname]
            + [
                ds.name
                for ds in datasets.list_vsam_datasets(
                    f"{tso_profile_prefix()}.PYIPCS.DDIR*"
                )
            ]
            + [ds.name for ds in datasets.list_vsam_datasets(f"{hlq}.DDIR*")],
        )

    request.addfinalizer(_cleanup)


# ==============================================================================
# Dump/DDir Fixtures
# ==============================================================================


@pytest.fixture
def default_ddir(
    allocations, ddir_parms, ddir_dsname
) -> Generator[IpcsDdir, None, None]:
    """DDIR with no dump initialized. DDIR deleted per test."""
    with IpcsDdir(
        ddir_dsname,
        allocations=allocations,
        ddir_parms=ddir_parms,
        delete=True,
    ) as pytest_ddir:
        yield pytest_ddir


@pytest.fixture
def dump(dump_dsname) -> IpcsDump:
    """Dump data set (IpcsDump)."""
    if dump_dsname is None:
        pytest.exit("Fixture used but --dump not provided")
    return IpcsDump(dump_dsname)


@pytest.fixture
def dump_ddir(
    dump, allocations, ddir_parms, dump_ddir_dsname
) -> Generator[IpcsDdir, None, None]:
    """DDIR with dump initialized. Skips the test if no dump was provided."""
    if dump is None:
        pytest.exit("Fixture user but --dump not provided")
    with IpcsDdir(
        dump_ddir_dsname,
        allocations=allocations,
        ddir_parms=ddir_parms,
    ) as pytest_ddir:
        yield pytest_ddir


# ==============================================================================
# JCL IPCS Subcommand Processing
# ==============================================================================


IPCS_JCL = """//MOCKPY JOB 'MOCK PYIPCS',CLASS=A
//*====================================================================
//* PYIPCS SUBCOMMAND JCL, VALIDATE SUBCMD OUTPUT
//*====================================================================
//IPCS EXEC PGM=IKJEFT01,DYNAMNBR=1000,REGION=0M
//IPCSDDIR DD DISP=SHR,DSN={ddir}
{allocations}
//SYSUDUMP DD SYSOUT=*
//SYSTSPRT  DD DSN={jcl_dsname},DISP=OLD
//SYSTSIN DD *
IPCS NOPARM
{setdef}
{subcmds}
END
"""


@pytest.fixture
def ipcs_subcmd_job(
    hlq: str,
):
    """Fixture that returns a callable that executes IPCS subcommands via a submitted job.

    Returns:
        Callable: A function with the signature::

            def _ipcs_subcmd_job(
                ddir: IpcsDdir,
                subcmds: list[str],
                allocations: Optional[dict[str, str | list[str]]],
                dump: Optional[IpcsDump] = None,
                local_defaults: Optional[str | Iterable[str]] = None,
            ) -> list[str]:
    """

    def _ipcs_subcmd_job(
        ddir: IpcsDdir,
        subcmds: list[str],
        allocations: Optional[dict[str, str | list[str]]],
        dump: Optional[IpcsDump] = None,
        local_defaults: Optional[str | Iterable[str]] = None,
    ) -> list[str]:
        """Run one or more IPCS subcommands in a job and return their outputs.

        Args:
            ddir: DDIR to run subcommands against.
            subcmds: Ordered list of IPCS subcommands to run.
            allocations: DD allocations. Values must be list[str] (dataset names).
                str values are not accepted for pyIPCS JCL testing.
            dump: Dump to set via SETDEF DSNAME.
            local_defaults: Additional SETDEF defaults to apply alongside the dump.

        Returns:
            list[str]: One raw output string per entry in ``subcmds``, in order.
        """
        jcl_temp_dsname = f"{hlq}.JCLIN"
        jcl_temp_membername = f"{jcl_temp_dsname}(TMP)"
        jcl_output_dsname = f"{hlq}.JCLOUT"

        def _ipcs_subcmd_jcl() -> str:
            """Format IPCS JCL for one or more subcommands.

            Returns:
                str: Formatted JCL string.
            """
            # Build DD allocations block
            dd_lines = "//*"
            if allocations:
                parts = []
                for dd_name, specification in allocations.items():
                    if isinstance(specification, str):
                        pytest.exit(
                            f"String allocation '{specification}' for DD '{dd_name}' "
                            "is not accepted for pyIPCS JCL testing. "
                            "Use a list of dataset names instead."
                        )
                    # list[str] — dataset concatenation as JCL DD lines
                    if specification:
                        parts.append(f"//{dd_name}  DD DSN={specification[0]},DISP=SHR")
                    for dsname in specification[1:]:
                        parts.append(f"//         DD DSN={dsname},DISP=SHR")
                dd_lines = "\n".join(parts) if parts else "//*"

            # Build SETDEF line
            _local_defaults = local_defaults
            if _local_defaults is not None and not isinstance(_local_defaults, str):
                _local_defaults = " ".join(_local_defaults)

            if dump is not None:
                if _local_defaults:
                    setdef_line = (
                        f"SETDEF LOCAL LIST DSNAME('{dump.dsname}') {_local_defaults}"
                    )
                else:
                    setdef_line = f"SETDEF LOCAL LIST DSNAME('{dump.dsname}')"
            elif _local_defaults:
                setdef_line = f"SETDEF LOCAL LIST {_local_defaults}"
            else:
                setdef_line = "SETDEF LOCAL LIST"

            subcmds_block = "\n".join(subcmds)

            return IPCS_JCL.format(
                jcl_dsname=jcl_output_dsname,
                ddir=ddir.dsname,
                allocations=dd_lines,
                setdef=setdef_line,
                subcmds=subcmds_block,
            )

        def _submit_ipcs_subcmd_jcl(jcl: str) -> str:
            """Submit IPCS JCL and return the raw SYSTSPRT output.

            Args:
                jcl: Formatted JCL string to submit.

            Returns:
                str: Raw SYSTSPRT output from the job.
            """
            # Create and write JCL to temp PDSE member
            datasets.create(name=jcl_temp_dsname, dataset_type="PDSE")
            datasets.write(dataset_name=jcl_temp_membername, content=jcl)

            # Create output dataset (SYSTSPRT target)
            datasets.create(
                name=jcl_output_dsname, dataset_type="SEQ", record_format="VB"
            )
            datasets.write(dataset_name=jcl_output_dsname, content="")

            # Submit and wait
            job = jobs.submit(jcl_temp_membername)
            job.wait()
            job.refresh()

            # Read output
            output = datasets.read(jcl_output_dsname)

            # Delete temp datasets
            rc_jcl = datasets.delete(jcl_temp_dsname)
            rc_out = datasets.delete(jcl_output_dsname)
            if rc_jcl != 0 or rc_out != 0:
                warnings.warn(
                    "Error deleting temp pyIPCS JCL test datasets: "
                    f"{jcl_temp_dsname} and/or {jcl_output_dsname}",
                    UserWarning,
                )

            return output

        jcl = _ipcs_subcmd_jcl()
        raw_output = _submit_ipcs_subcmd_jcl(jcl)

        # Parse each subcommand's output from the raw SYSTSPRT text.
        # SYSTSIN echoes each command as "IPCS\n<subcmd>\n"; slice between markers.
        outputs: list[str] = []
        subcmd_index = raw_output.find(f"\nIPCS\n{subcmds[0]}\n") + len(
            f"\nIPCS\n{subcmds[0]}\n"
        )
        for i in range(len(subcmds)):
            if i != len(subcmds) - 1:
                subcmd_end_index = raw_output.find(
                    f"\nIPCS\n{subcmds[i + 1]}\n", subcmd_index
                )
                subcmd_output = raw_output[subcmd_index:subcmd_end_index]
                subcmd_index = subcmd_end_index + len(f"\nIPCS\n{subcmds[i + 1]}\n")
            else:
                subcmd_end_index = raw_output.find("\nIPCS\n", subcmd_index)
                subcmd_output = (
                    raw_output[subcmd_index:subcmd_end_index]
                    if subcmd_end_index != -1
                    else raw_output[subcmd_index:]
                )
            outputs.append(subcmd_output)

        return outputs

    return _ipcs_subcmd_job
