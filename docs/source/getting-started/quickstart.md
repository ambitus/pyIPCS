# Quickstart Guide

Get up and running with pyIPCS.

## 1. Installation

Install pyIPCS by following the [Installation Guide](installation.md).

## 2. Understanding the Architecture

Before writing code, review the key concepts:

- **[IPCS Architecture](../guide/ipcs-architecture.md)** — Overview of IPCS, DDIRs, BLSCDDIR, and z/OS dump data sets
- **[pyIPCS Architecture](../guide/pyipcs-architecture.md)** — How pyIPCS drives IPCS: TSO/E shell commands, the driver data set, and core API objects

## 3. Basic Usage

Start with practical examples:

- **[Basic Examples](../examples/basic-examples.md)** — Core workflow covering:
  - Opening a DDIR and referencing a dump
  - Inspecting dump metadata
  - Running IPCS subcommands
  - Using `pyipcs.ipcs` utility functions

## 4. CLI Usage

- **[Command-Line Interface](../guide/cli.md)** — Run IPCS commands directly from the z/OS UNIX shell without writing Python scripts:
  - Creating and opening DDIRs
  - Initializing dump data sets
  - Running IPCS subcommands
  - Shell automation examples

## 5. API Reference

- **[API Documentation](../api/index.md)** — Full reference for all classes and functions
