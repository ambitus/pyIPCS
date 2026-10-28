# Basic Examples

The typical pyIPCS workflow:

1. **Open a DDIR** with `IpcsDdir`
2. **Reference a dump** with `IpcsDump`
3. **Run subcommands** via `ddir.run()` and inspect the `IpcsResponse`

## Your First Dump Analysis

```python
from pyipcs import IpcsDdir, IpcsDump

DUMP_DSNAME = "MY.DUMP.DSNAME"
DDIR_DSNAME = "MY.IPCS.DDIR"

with IpcsDdir(DDIR_DSNAME) as ddir:
    dump = IpcsDump(DUMP_DSNAME)

    # Run a subcommand against the dump
    response = ddir.run("STATUS FAILDATA", dump=dump)

    print(f"Return code: {response.rc}")
    print(response.output)
```

## Using a Temporary DDIR

For one-off analysis, use `IpcsDdir.temp_ddir()` to create a temporary DDIR that is
automatically deleted on exit:

```python
from pyipcs import IpcsDdir, IpcsDump

with IpcsDdir.temp_ddir() as ddir:
    dump = IpcsDump("MY.DUMP.DSNAME")
    response = ddir.run("STATUS REGISTERS", dump=dump)
    print(response.output)
```

## Inspecting Dump Metadata

`IpcsDump` parses the dump header on initialization:

```python
from pyipcs import IpcsDump

dump = IpcsDump("MY.DUMP.DSNAME")

if dump.metadata:
    print(f"Type:      {dump.metadata['type']}")
    print(f"Title:     {dump.metadata['title']}")
    print(f"System:    {dump.metadata['sysname']}")
    print(f"z/OS:      {dump.metadata['version']}.{dump.metadata['release']}")
    print(f"Timestamp: {dump.metadata['timestamp']}")
```

## Using pyipcs.ipcs Utility Functions

The `pyipcs.ipcs` module provides convenience functions that run common subcommands
and return parsed results:

```python
from pyipcs import IpcsDdir, IpcsDump
from pyipcs import ipcs

with IpcsDdir.temp_ddir() as ddir:
    dump = IpcsDump("MY.DUMP.DSNAME")

    # List all address spaces on the system at dump time
    asids = ipcs.select_all(ddir, dump)
    if asids.data:
        for entry in asids.data:
            print(f"ASID: {entry['asid']}  Job: {entry['jobname']}  ASCB: {entry['ascb']}")

    # Get IPL time
    ipl = ipcs.ipl_time(ddir, dump)
    print(f"IPL time: {ipl.data}")
    print(f"Return code: {ipl.response.rc}")

    # Decode an opcode
    mnemonic = ipcs.opcode(ddir, dump, "0A0A")
    print(f"Mnemonic: {mnemonic.data}")
```

### Parsing Output with `find_field` and `rfind_field`

`find_field` and `rfind_field` locate the text that follows a start string and return
its `(begin, end)` indexes. `find_field` uses the first occurrence of the start string and
`rfind_field` uses the last. The field ends after `length` characters, at the next
`end_str`, or at the next space if neither is given. Use `start` and `end` to limit the
part of the text that is searched.

```python
from pyipcs.ipcs import find_field, rfind_field

text = "key=ABC def=XYZ key=123 end"

begin, end = find_field(text, "key=")
print(text[begin:end])  # ABC

begin, end = rfind_field(text, "key=")
print(text[begin:end])  # 123

begin, end = find_field(text, "def=", length=2)
print(text[begin:end])  # XY

begin, end = find_field(text, "def=", end_str=" key")
print(text[begin:end])  # XYZ
```

If the start string is not found, `(-1, -1)` is returned. If it is found but the end
cannot be found, the end index is `-1`:

```python
find_field(text, "nope")             # (-1, -1)
find_field(text, "def=", end_str="!")  # (12, -1)
```

## Writing Subcommand Output to a File

For large subcommand outputs, write directly to a file instead of buffering in memory:

```python
from pyipcs import IpcsDdir, IpcsDump

with IpcsDdir.temp_ddir() as ddir:
    dump = IpcsDump("MY.DUMP.DSNAME")

    with open("/tmp/output.txt", "w", encoding="cp1047") as f:
        ddir.run("SELECT ALL", dump=dump, output=f)
```

## Creating Your Own Parsed Response

You can use `IpcsParsedResponse` to build custom helper functions that parse IPCS subcommand outputs while preserving the underlying `IpcsResponse` for diagnostics:

```python
from typing import Optional
from pyipcs import IpcsDdir, IpcsDump, IpcsParsedResponse


def parse_my_data(ddir: IpcsDdir, dump: IpcsDump) -> IpcsParsedResponse[str]:
    """Run a custom subcommand and parse a key field from its output."""
    response = ddir.run("YOUR SUBCMD OPTION(ALL)", dump=dump)

    marker = "KEY: "
    idx = response.output.find(marker)
    if idx == -1:
        return IpcsParsedResponse(data=None, response=response)

    idx += len(marker)
    key_val = response.output[idx:idx+3]

    return IpcsParsedResponse(data=key_val if key_val else None, response=response)


# Using the custom parsed response:
with IpcsDdir.temp_ddir() as ddir:
    dump = IpcsDump("MY.DUMP.DSNAME")
    result = parse_my_data(ddir, dump)

    # Return the parsed data
    print(f"Parsed data: {result.data}")

    # Access the raw subcommand response and return code at any time
    print(f"Subcommand RC: {result.response.rc}")
```

## Best Practices

1. **Use `IpcsDdir` as a context manager** — ensures resources are cleaned up properly
2. **Use `IpcsDdir.temp_ddir()`** for one-off analysis to avoid managing DDIR data set names
3. **Pass `dump` per `run()` call** rather than using `setdef_global` unless you have exclusive DDIR access
4. **Check `IpcsResponse.rc`** — a non-zero return code may indicate a subcommand issue
