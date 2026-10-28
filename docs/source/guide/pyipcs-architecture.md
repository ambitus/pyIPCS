# pyIPCS Architecture

Understanding pyIPCS's basic architecture and key concepts.

Please review [IPCS Architecture](./ipcs-architecture.md) if you have not already —
the information below assumes familiarity with relevant IPCS terms and concepts.

## Overview

pyIPCS provides a Python interface to IPCS on z/OS. It works by:

1. **Opening** an IPCS dump directory (DDIR) which drives all subcommand execution
2. **Referencing** a dump data set to set context for IPCS subcommands
3. **Running** IPCS subcommands and returning structured response objects

## TSO/E Shell Commands

pyIPCS executes TSO/E commands and IPCS subcommands from Python via `subprocess` using two z/OS shell commands:

- **`tso`** — runs an unauthorized TSO/E command via the OMVS interface
- **`tsocmd`** — runs authorized TSO/E commands through `IKJEFT01`

DD allocations are passed via `TSOALLOC` and environment variable exports before each invocation.

**IBM Documentation:**
- [tso](https://www.ibm.com/docs/en/zos/3.2.0?topic=descriptions-tso-run-tsoe-command-from-shell)
- [tsocmd](https://www.ibm.com/docs/en/zos/3.2.0?topic=scd-tsocmd-run-tsoe-command-from-shell-including-authorized-commands)

## The pyIPCS Driver Data Set

The pyIPCS driver data set is a z/OS **PDSE** that pyIPCS creates and manages automatically.
It contains the REXX and CLIST execs that pyIPCS uses internally to execute IPCS subcommands.

**Example member:** `IPCSRUN` — executes an IPCS subcommand and captures output

**Naming convention:** `<TSO_profile_prefix>.PYIPCS.V<version>` (e.g. `MYNAME.PYIPCS.V020000`)

- If the driver data set does not exist when `IpcsDdir` is initialized, pyIPCS creates and populates it automatically.
- If it already exists, pyIPCS validates that all members are present and have the expected content before using it.
- The data set name can be overridden by passing a `driver` parameter to `IpcsDdir`.

## Core Components

### `IpcsDdir` — The IPCS Dump Directory

`IpcsDdir` is the central object in pyIPCS. It represents an IPCS dump directory (DDIR)
and drives all IPCS subcommand execution. On initialization it runs `BLSCDDIR` to create
or open the DDIR data set.

**Key Concepts:**
- Manages IPCS allocations (DD names → data sets)
- Holds a reference to a pyIPCS driver data set containing REXX/CLIST execs
- Supports a context manager (`with` block) for clean resource management
- Can optionally delete the DDIR on exit

### `IpcsDump` — The Dump Data Set

`IpcsDump` represents a z/OS dump data set. On initialization it validates that the
data set exists and is a valid dump, then parses metadata from the dump header record.

**Metadata available:**
- Dump type (`SAD`, `SVC`, `SYSM`, `SLIP`)
- Dump title
- System name
- z/OS version and release
- Timestamp (time of error)

### `TsoResponse` — TSO/E Command Response

`TsoResponse` holds the result of a TSO/E command execution.

**Properties:** `cmd`, `rc`, `output`, `authorized`

### `IpcsResponse` — IPCS Subcommand Response

`IpcsResponse` holds the result of an IPCS subcommand execution.

**Properties:** `subcmd`, `rc`, `output`, `authorized`

### `IpcsParsedResponse` — Parsed Subcommand Response

`IpcsParsedResponse[T]` is a generic response container that pairs parsed dump data with the underlying raw `IpcsResponse`.

**Properties:** `data`, `response`

### `pyipcs.ipcs` — IPCS Utility Functions

A module of higher-level utility functions, some of which run common IPCS subcommands and return `IpcsParsedResponse` objects containing parsed results alongside the raw response.

**Functions include:** `is_dump`, `find_field`, `rfind_field`, `sliptrap`, `ipl_time`,
`select_all`, `storage_areas`, `asids_dumped`, `opcode`

### `pyipcs.driver` — Driver Data Set

Manages the pyIPCS driver data set — a z/OS data set that holds the REXX and CLIST
execs used internally to drive IPCS subcommand execution.

### `pyipcs.exceptions` — Exceptions and Warnings

Defines the exception and warning hierarchy raised by pyIPCS operations.

| Class | Type | Description |
|---|---|---|
| `TsoError` | Exception | Base TSO/E error |
| `TsoInvalidReturnCodeError` | Exception | Unexpected TSO/E return code |
| `IpcsError` | Exception | Base IPCS error |
| `IpcsInvalidReturnCodeError` | Exception | Unexpected IPCS return code |
| `TsoWarning` | Warning | Base TSO/E warning |
| `TsoInvalidReturnCodeWarning` | Warning | Non-fatal unexpected TSO/E return code |
| `IpcsWarning` | Warning | Base IPCS warning |
| `IpcsInvalidReturnCodeWarning` | Warning | Non-fatal unexpected IPCS return code |
| `DdirDeletedError` | Exception | Operation on a deleted DDIR |

## Basic Data Flow

```
┌──────────────┐     ┌─────────────────────────────────┐
│  IpcsDump    │     │  IpcsDdir                       │
│  (Dump DS)   │────▶│  (DDIR / Subcommand Driver)     │
└──────────────┘     └────────────────┬────────────────┘
                                      │
                                      │ runs subcommands
                                      ▼
                             ┌─────────────────┐
                             │  IpcsResponse   │
                             │  (rc, output)   │
                             └─────────────────┘
```

## Best Practices

1. **Use `IpcsDdir` as a context manager** — ensures allocations and resources are cleaned up properly
2. **Reuse a single `IpcsDdir`** for multiple subcommand calls against the same dump
3. **Check `IpcsResponse.rc`** — a non-zero return code may indicate a subcommand issue
