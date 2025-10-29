# Changelog

- __Categories:__
  - __Added:__ New features.
  - __Changed:__ Updates to existing functionality.
  - __Deprecated:__ Features that will be removed in future versions.
  - __Removed:__ Features that have been removed.
  - __Fixed:__ Bug fixes.
  - __Security:__ Security related changes.

---

## [1.2.0] - TBD

### Added

- Support for zoautil_py 1.4.x
- Get info about a dump without the need for dump initialization
  - `DumpHeader` object
    - Also included in `Dump` object attribute `header`
- Improved allocation configuration/customization
  - `IpcsAllocations` object
  - `IpcsSession.aloc` attribute
- Improved DDIR configuration/customization
  - `DumpDirectory` object
  - `IpcsSession.ddir` attribute
  - More parameters for SETDEF defaults
    - `DumpDirectory.defaults` method
  - List dataset names of the sources described in the current dump directory
    - `DumpDirectory.sources` method
- Add `IpcsSession` attributes `uid`, `hlq_full`, and `directory_full`
  - For greater control over pyIPCS temporary datasets and files
- Add pyICS examples in `/examples`

## Changed

- In `Dump` object, data from dump header moved from `Dump.data` to now `Dump.header`/`DumpHeader`
- `IpcsSession.ddir` now returns `DumpDirectory` object rather than string
- Move to NumPy Style Docstrings
- Refactored testing framework to reduce number of tests and reduce time needed to run tests

## Removed

- Within `IpcsSession` object
  - Functionality now moved to `IpcsAllocations`/`IpcsSession.aloc`
    - Removed `IpcsSession.get_allocations`
    - Removed `IpcsSession.set_allocations`
    - Removed `IpcsSession.updated_allocations`
  - Functionality now moved to `DumpDirectory`/`IpcsSession.ddir`
    - Removed `IpcsSession.create_ddir`
    - Removed `IpcsSession.create_session_ddir`
    - Removed `IpcsSession.set_ddir`
    - Removed `IpcsSession.get_defaults`
    - Removed `IpcsSession.set_defaults`
    - Removed `IpcsSession.dsname_in_ddir` (Now can use `IpcsSession.ddir.sources`)
  - Remove `util.dump_header_data` and move functionality to `DumpHeader` object
  - Remove `IpcsLogger`/`IpcsSession.logger`
  - Remove User Guide

## [1.1.0] - 8/12/2025

### Added

- pyIPCS Jupyter Notebook Support
- pyIPCS JSON support
  - Added `IpcsJsonEncoder`
- Improved `print` and `repr` for pyIPCS objects
- `Subcmd.output` always returns string whether output is stored in string or file
- Development scripts
  - Added `/dev`
- `Subcmd` object `auth` parameter added to execute subcommands in an authorized environment
- Greater customization with ddir creation by adding `BLSCDDIR` parameters
  - Added `ddir_defaults`
  - Added `create_ddir` and `create_session_ddir` parameters
- Refactored internal code to remove problem with conflicting pyIPCS sessions under the same hlq

### Changed

- `Dump.data['asids_all']` and `Dump.data['storage_areas']` changed to list of dictionaries
- `PyIPCSLogger` changed to `IpcsLogger`
- `IpcsSession.set_defaults` parameter `other` changed to `setdef_params`
- Refactored internal code

### Fixed

- [https://github.com/ambitus/pyIPCS/issues/2](https://github.com/ambitus/pyIPCS/issues/2)
- [https://github.com/ambitus/pyIPCS/issues/3](https://github.com/ambitus/pyIPCS/issues/3)
- [https://github.com/ambitus/pyIPCS/issues/4](https://github.com/ambitus/pyIPCS/issues/4)
- Issue where no jobname in `SELECT ALL` would cause the dump object to fail

---

## [1.0.0] - 4/24/25

### Added

- Initial release with core features
