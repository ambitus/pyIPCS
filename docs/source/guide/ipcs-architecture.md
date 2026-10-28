# IPCS Architecture

An overview of IPCS and the z/OS concepts relevant to pyIPCS.

## What is IPCS?

IPCS (Interactive Problem Control System) is a z/OS facility for analyzing dump data sets.
It provides subcommands for formatting and interpreting dump contents — such as listing
storage, decoding PSWs, identifying ASIDs, and more.

pyIPCS drives IPCS programmatically from Python by invoking IPCS subcommands through TSO/E
and capturing their output.

**IBM Documentation:** [Getting Started with IPCS](https://www.ibm.com/docs/en/zos/3.2.0?topic=guide-getting-started-ipcs)

## Dump Directories (DDIR)

A **dump directory (DDIR)** is a z/OS data set that IPCS uses to maintain information about
dump data sets — including source pointers, default options, and subcommand results. IPCS
requires an active DDIR before it can process any dump.

**IBM Documentation:** [Using User and Sysplex Dump Directories](https://www.ibm.com/docs/en/zos/3.2.0?topic=functions-using-user-sysplex-dump-directories)

### BLSCDDIR

`BLSCDDIR` is the CLIST used to create or open a DDIR data set. pyIPCS calls `BLSCDDIR`
automatically when you initialize an `IpcsDdir` object.

**IBM Documentation:** [BLSCDDIR CLIST](https://www.ibm.com/docs/en/zos/3.2.0?topic=execs-blscddir-clist-create-dump-directory)

Key `BLSCDDIR` parameters:

| Parameter | Description |
|---|---|
| `DSNAME` | Data set name of the DDIR to create or open |
| `RECORDS` | Number of records to allocate (new DDIRs only) |
| `VOLUME` | Volume on which to allocate the DDIR |

## IPCS Subcommands

IPCS subcommands are the primary way to interact with dump data. They are issued within an
IPCS session against an active DDIR and dump source, and produce formatted output describing
dump contents.

**IBM Documentation:** [IPCS Subcommands](https://www.ibm.com/docs/en/zos/3.2.0?topic=commands-ipcs-subcommands)

## z/OS Dump Data Sets

A z/OS dump data set is a z/OS data set containing dump data captured at the time of an error.
IPCS uses the dump data set — referenced through the DDIR — as the source for all subcommand analysis.
