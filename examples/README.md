# pyIPCS Examples

- **Note:** In order to run example scripts further configuration of you IpcsSession may be required
  - Configure your Allocations
    - `IpcsSession.aloc`
  - Configure Your DDIR Defaults or DDIR Creation Settings
    - `IpcsSession.ddir`

---

## Basic Example

- **File:** `/examples/basic.py`
- **Description:** Run basic pyIPCS functionality with a z/OS dump.
- **Usage:** `basic.py <dump_dsname>`
- **Example:** `basic.py YOUR.DUMP.DSNAME`

## Custom Subcommand Object Example

- **File:** `/examples/custom_subcmd.py`
- **Description:** Create a Custom Subcommand Object for `STATUS REGISTERS` and store PSW in `data`.
- **Usage:** `custom_subcmd.py <dump_dsname>`
- **Example:** `custom_subcmd.py YOUR.DUMP.DSNAME`

## pyIPCS Example Jupyter Notebook

- **File:** `/examples/pyipcs_notebook.ipynb`
- **Description:** Jupyter Notebook for basic pyIPCS functionality with a z/OS dump.
