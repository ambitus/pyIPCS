# Writing Tests

## Test Markers

| Marker | Description |
|--------|-------------|
| `dump` | Test requires a source dump. Skipped automatically when `--dump` is not provided. |

Mark a test with `@pytest.mark.dump` to declare it dump-dependent:

```python
@pytest.mark.dump
def test_something(dump, dump_ddir):
    ...
```

## Fixtures

Key fixtures provided by `conftest.py`:

| Fixture | Scope | Description |
|---------|-------|-------------|
| `allocations` | session | Allocations dict loaded from `--allocations` JSON file, or `None` |
| `ddir_parms` | session | Additional BLSCDDIR parameters from `--ddir-parms`, or `None` |
| `hlq` | session | High-level qualifier from `--hlq`, defaulting to `<tso_prefix>.PYTEST` |
| `driver_dsname` | session | Dataset name for the non-default test pyIPCS driver (`<hlq>.DRIVER`) |
| `ddir_dsname` | session | Dataset name for the general-purpose test DDIR (`<hlq>.TESTDDIR`) |
| `dump_dsname` | session | Dump dataset name string from `--dump`, or `None` |
| `dump_ddir_dsname` | session | Dataset name for the dump test DDIR (`<hlq>.DUMPDDIR`) |
| `temp_dsname` | session | Dataset name for a temporary test data set (`<hlq>.TEMPDSN`). Tests create it as needed; it is deleted after each test |
| `default_ddir` | function | Live `IpcsDdir` with no dump initialized; deleted after each test |
| `dump` | function | `IpcsDump` wrapping the dataset provided via `--dump` |
| `dump_ddir` | function | Live `IpcsDdir` with the dump already initialized |
| `ipcs_subcmd_job` | function | Callable that submits IPCS subcommands as a real z/OS job and returns their outputs |

## Data Set Cleanup

The test suite is designed to leave no leftover data sets on the system.

- **Before the session** — `pytest_configure` deletes any pre-existing test data sets matching the configured names and HLQ patterns.
- **After each test** — the `reset_state` fixture (autouse) deletes the default driver, custom driver, temporary data set (`temp_dsname`), general-purpose DDIR, and any `PYIPCS.DDIR*` / `<hlq>.DDIR*` temp DDIRs.
- **After the session** — the `environment` fixture (autouse) deletes the dump DDIR.

If any data set cannot be deleted, `pytest.exit` is called and the session is aborted with a list of survivors.
