# Running the Tests

The pyIPCS test suite runs on z/OS using [pytest](https://docs.pytest.org/). All tests interact with real z/OS resources such as TSO/E, IPCS DDIRs, and dump data sets.

## Usage

```bash
pytest tests/ [--allocations FILE] [--ddir-parms PARMS] [--dump DSNAME] [--hlq HLQ]
```

## Flags

### `--allocations FILE`

Path to a JSON file containing custom TSO/E DD allocations used for every test.

The file must be a JSON object where:

- **Keys** are DD names (e.g. `"IPCSPARM"`, `"SYSPROC"`)
- **Values** are either a string allocation request or a list of dataset names

```json
{
  "IPCSPARM": "SYS1.PARMLIB",
  "SYSPROC": ["SYS1.SBLSCLI0", "MY.CLIST"]
}
```

### `--ddir-parms PARMS`

Additional parameters forwarded to the `BLSCDDIR` CLIST when DDIRs are created during tests.

### `--dump DSNAME`

Data set name of the dump to use in dump-dependent tests.

When omitted, all tests decorated with `@pytest.mark.dump` are automatically **skipped**.

### `--hlq HLQ`

High-level qualifier used when naming temporary test data sets (DDIRs, JCL, output datasets).

## Examples

```bash
# Run all tests with default allocations
pytest tests/

# Custom allocations
pytest tests/ --allocations /path/to/allocations.json

# Run dump-dependent tests
pytest tests/ --dump MY.HLQ.DUMP

# Full example with all flags
pytest tests/ --allocations /path/to/allocations.json --dump MY.HLQ.DUMP --hlq MY.HLQ --ddir-parms "RECORDS(3000)"
```
