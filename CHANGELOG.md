# Changelog

- __Categories:__
  - __Added:__ New features.
  - __Changed:__ Updates to existing functionality.
  - __Deprecated:__ Features that will be removed in future versions.
  - __Removed:__ Features that have been removed.
  - __Fixed:__ Bug fixes.
  - __Security:__ Security related changes.

---

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
