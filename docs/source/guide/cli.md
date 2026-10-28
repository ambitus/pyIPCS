# Command-Line Interface (CLI)

pyIPCS provides a command-line interface (`pyipcs`) that allows you to manage IPCS dump directories (DDIRs), initialize dump data sets, and run IPCS subcommands directly from the z/OS UNIX shell without writing Python scripts.

## Overview

Before using the CLI, make sure pyIPCS is correctly installed — see the [Installation Guide](../getting-started/installation.md).

The `pyipcs` command is installed as an entry point script when installing the pyIPCS package:

```bash
pyipcs <command> [arguments] [options]
```

### Exit Codes

Exit codes returned by the CLI generally match the underlying TSO/E or IPCS return code.

### Allocations File Format

The `--allocations FILE` option takes a path to a JSON file specifying TSO/E DD allocations. If omitted, pyIPCS uses the default allocations:

```json
{
  "IPCSPARM": "SYS1.PARMLIB",
  "SYSPROC": "SYS1.SBLSCLI0"
}
```

You can specify a single data set name as a string or a list of data set names for concatenated DDs:

```json
{
  "IPCSPARM": "SYS1.PARMLIB",
  "SYSPROC": [
    "SYS1.SBLSCLI0",
    "MY.CUSTOM.SBLSCLI0"
  ]
}
```

---

## Commands

### `create-ddir`

Create or open a dump directory (DDIR). If the DDIR data set does not already exist, `BLSCDDIR` is executed to allocate and initialize it. If the DDIR data set already exists, it is opened directly without executing `BLSCDDIR` (and any `--ddir-parms` are ignored).

#### Syntax

```bash
pyipcs create-ddir <ddir> [--ddir-parms PARMS] [--driver DSNAME] [--allocations FILE]
```

#### Arguments & Options

| Argument / Option | Type | Description |
|---|---|---|
| `ddir` | Positional | Data set name of the DDIR to create or open. |
| `--ddir-parms PARMS` | Optional | Additional parameters to pass to the `BLSCDDIR` CLIST (e.g., `RECORDS(2500) VOLUME(VOL001)`). Ignored if the DDIR already exists. |
| `--driver DSNAME` | Optional | Driver data set name to use for the DDIR. Defaults to `<TSO_prefix>.PYIPCS.V<version>`. |
| `--allocations FILE` | Optional | Path to a JSON file containing custom TSO/E allocations. |

#### Examples

Create a new DDIR with default sizing:

```bash
pyipcs create-ddir "USER.IPCS.DDIR"
```

Create a DDIR with custom record count and volume allocation:

```bash
pyipcs create-ddir "USER.IPCS.DDIR" --ddir-parms "RECORDS(5000) VOLUME(PRD001)"
```

Using custom driver and allocations:

```bash
pyipcs create-ddir "USER.IPCS.DDIR" --driver "USER.PYIPCS.CUSTOM" --allocations allocs.json
```

---

### `setdef-global`

Set global defaults (such as default dump source or formatting options) on an existing DDIR using the IPCS `SETDEF` subcommand.

#### Syntax

```bash
pyipcs setdef-global <ddir> [--dump DSNAME] [--defaults DEFAULTS] [--driver DSNAME] [--allocations FILE]
```

#### Arguments & Options

| Argument / Option | Type | Description |
|---|---|---|
| `ddir` | Positional | Data set name of the DDIR. |
| `--dump DSNAME` | Optional | Source dump data set name to set as the global default (`DSNAME('...')`). |
| `--defaults DEFAULTS` | Optional | Additional parameters to pass to the `SETDEF` command (e.g., `LENGTH(8) NOCONFIRM`). |
| `--driver DSNAME` | Optional | Driver data set name to use for the DDIR. Defaults to `<TSO_prefix>.PYIPCS.V<version>`. |
| `--allocations FILE` | Optional | Path to a JSON file containing custom TSO/E allocations. |

#### Examples

Set the default dump source for the DDIR:

```bash
pyipcs setdef-global "USER.IPCS.DDIR" --dump "DUMP.SYSTEM.SVCDUMP"
```

Set global formatting options:

```bash
pyipcs setdef-global "USER.IPCS.DDIR" --defaults "LENGTH(8) NOCONFIRM"
```

Combine both dump and options:

```bash
pyipcs setdef-global "USER.IPCS.DDIR" --dump "DUMP.SYSTEM.SVCDUMP" --defaults "FLAG(ERROR) NOCONFIRM"
```

---

### `init-dump`

Initialize a dump data set in an existing DDIR by executing the `STATUS` subcommand. This validates the dump and creates the source description in the DDIR.

#### Syntax

```bash
pyipcs init-dump <ddir> <dump> [--driver DSNAME] [--allocations FILE]
```

#### Arguments & Options

| Argument / Option | Type | Description |
|---|---|---|
| `ddir` | Positional | Data set name of the DDIR. |
| `dump` | Positional | Source dump data set name to initialize. |
| `--driver DSNAME` | Optional | Driver data set name to use for the DDIR. Defaults to `<TSO_prefix>.PYIPCS.V<version>`. |
| `--allocations FILE` | Optional | Path to a JSON file containing custom TSO/E allocations. |

#### Examples

Initialize a dump data set:

```bash
pyipcs init-dump "USER.IPCS.DDIR" "DUMP.SYSTEM.SVCDUMP"
```

Output on success:

```text
Dump initialization successful.
```

---

### `run`

Execute an IPCS subcommand against an existing DDIR and stream the output to standard output.

#### Syntax

```bash
pyipcs run <ddir> "<subcmd>" [--dump DSNAME] [--auth] [--local-defaults DEFAULTS] [--driver DSNAME] [--allocations FILE]
```

#### Arguments & Options

| Argument / Option | Type | Description |
|---|---|---|
| `ddir` | Positional | Data set name of the DDIR. |
| `subcmd` | Positional | IPCS subcommand to run (e.g., `"STATUS FAILDATA"`, `"SELECT ALL"`). |
| `--dump DSNAME` | Optional | Source dump data set name for this invocation. |
| `--auth` | Optional Flag | Run the subcommand in an authorized environment (`tsocmd`). |
| `--local-defaults DEFAULTS` | Optional | Parameters for `SETDEF NOLIST LOCAL` run before the subcommand. |
| `--driver DSNAME` | Optional | Driver data set name to use for the DDIR. Defaults to `<TSO_prefix>.PYIPCS.V<version>`. |
| `--allocations FILE` | Optional | Path to a JSON file containing custom TSO/E allocations. |

#### Examples

Run a status report against a specific dump:

```bash
pyipcs run "USER.IPCS.DDIR" "STATUS FAILDATA" --dump "DUMP.SYSTEM.SVCDUMP"
```

Run an IPCS subcommand with local temporary defaults:

```bash
pyipcs run "USER.IPCS.DDIR" "STATUS REGISTERS" --dump "DUMP.SYSTEM.SVCDUMP" --local-defaults "LENGTH(8) NOCONFIRM"
```

Run an authorized subcommand:

```bash
pyipcs run "USER.IPCS.DDIR" "TCBEXIT EP(MYEXIT)" --dump "DUMP.SYSTEM.SVCDUMP" --auth
```

Redirect subcommand output to a file:

```bash
pyipcs run "USER.IPCS.DDIR" "SUMMARY FORMAT" --dump "DUMP.SYSTEM.SVCDUMP" > /tmp/summary_report.txt
```

---

## Complete Shell Automation Example

The following bash script demonstrates a complete end-to-end workflow using the `pyipcs` CLI:

```bash
#!/usr/bin/env bash
set -e

DDIR="USER.PROD.DDIR"
DUMP="DUMP.SYSTEM.SVCDUMP"

echo "==> Creating / opening DDIR..."
pyipcs create-ddir "$DDIR" --ddir-parms "RECORDS(3000)"

echo "==> Initializing dump..."
pyipcs init-dump "$DDIR" "$DUMP"

echo "==> Running STATUS FAILDATA..."
pyipcs run "$DDIR" "STATUS FAILDATA" --dump "$DUMP"

echo "==> Extracting address space list..."
pyipcs run "$DDIR" "SELECT ALL" --dump "$DUMP" > /tmp/asids.txt

echo "==> Analysis complete!"
```
