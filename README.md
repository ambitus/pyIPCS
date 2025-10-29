# pyIPCS README

- **[Important Disclaimer (Please Read)](#important-disclaimer-please-read)**
- **[Getting Started (Installation Guide)](#getting-started-installation-guide)**
- **[pyIPCS Versioning and Updates](#pyipcs-versioning-and-updates)**
- **[Report a Bug or Request a Feature](#report-a-bug-or-request-a-feature)**
- **[Contribute to pyIPCS](#contribute-to-pyipcs)**
- **[pyIPCS Examples](#pyipcs-examples)**

- **Documentation**

  - **[Hex Object](#hex-object)**
  - **[IpcsSession Object](#ipcssession-object)**
  - **[DumpHeader Object](#dumpheader-object)**
  - **[Dump Object](#dump-object)**
  - **[Subcmd Object](#subcmd-object)**
  - **[Creating Custom Subcmd Objects](#creating-custom-subcmd-objects)**
  - **[Util Functions](#util-functions)**
  - **[Converting pyIPCS Objects to JSON](#converting-pyipcs-objects-to-json)**

---
---

## pyIPCS Version: `1.2.0`

- **To check your current pyIPCS version:**

```bash
pip show pyipcs
```

---
---

```python
from pyipcs import Hex, IpcsSession, Subcmd
from pyipcs.util import *

# Create IpcsSession object
# Manages settings for your IPCS session

session = IpcsSession()

# Open IPCS Session

session.open()

# String dataset name of z/OS dump

dsname = ...

# Create Dump object `dump`
# Initializes z/OS dump and stores general info

dump = session.init_dump(dsname)

# Print the dump title
# "SAD", "SVCD", "TDMP", "SYSM", or "SLIP"

if "dump_type" in dump.header:
  print(dump.header["dump_type"])
else:
  print("Dump Type Not Found")

# Run IPCS subcommand against z/OS dump `dump` and store output

subcmd = Subcmd(session, "STATUS REGISTERS")

# Print portion of IPCS subcommand output

print(subcmd[10:20])

# Close IPCS Session

session.close()
```

---
---

## Important Disclaimer (Please Read)

- **[Back to Top](#pyipcs-readme)**

---

- **In order to perform operations, pyIPCS creates temporary execs, DDIRs, and files while the IPCS Session is open.**

<br>

- **Please be aware of leftover datasets and files in the event of unintended cleanup failures.**

<br>

- **High level qualifiers for pyIPCS temporary datasets**
  - **`IpcsSession.hlq`**
  - **`IpcsSession.hlq_full`**

- **Directories for pyIPCS temporary files**
  - **`IpcsSession.directory`**
  - **`IpcsSession.directory_full`**

---
---

## Getting Started (Installation Guide)

- **[Back to Top](#pyipcs-readme)**

---

### [Getting Started](./GETTING_STARTED.md)

- **Dependencies and Prerequisites**
- **pyIPCS Installation**

---
---

## pyIPCS Versioning and Updates

- **[Back to Top](#pyipcs-readme)**

---

### Example Version: `1.2.3`

- **Major Version (`1`)**
  - Indicates a significant update.
  - Probable to include breaking changes that are not backward-compatible.

- **Minor Version (`2`)**
  - Adds new features or functionality.
  - Mostly backward-compatible with previous versions within the same major version.

- **Patch Version (`3`)**
  - Fixes bugs or makes small improvements.
  - Always backward-compatible.

### [CHANGELOG.md](./CHANGELOG.md)

- **The Changelog file contains info on changes between each new version**

---
---

## Report a Bug or Request a Feature

- **[Back to Top](#pyipcs-readme)**

---

- **To report a bug or request a feature/update, please open a new issue.**
  - Once you open an issue, there are various templates
    - Bug Report
    - Feature Request
    - Documentation Update
    - Other requests you might have for pyIPCS

---
---

## Contribute to pyIPCS

- **[Back to Top](#pyipcs-readme)**

---

### [How to Contribute to pyIPCS](./CONTRIBUTING.md)

- **Follow the link above to get information on how to contribute to pyIPCS**

---
---

## pyIPCS Examples

- **[Back to Top](#pyipcs-readme)**

---

- **You can find practical usage examples and runnable scripts in the `/examples` directory**

### [pyIPCS Examples README](./examples/README.md)

---
---

## Hex Object

- **[Back to Top](#pyipcs-readme)**
- **[Arithmetic, Logical, and Bitwise Operations With Hex Object](#arithmetic-logical-and-bitwise-operations-with-hex-object)**
- **[Methods](#hex-methods)**

---

### *class* pyipcs.Hex(*value*)

**Bases:** *object*

### Description

- Contains various methods and functionality to manage hex variables in an IPCS environment
- Accepts strings or integers as input

### Parameters

- **value** *(str|int)*: Hex string or integer for hex value

---

### Arithmetic, Logical, and Bitwise Operations With Hex Object

- **[Back to Hex Object](#hex-object)**

---

- The `Hex` object supports a variety of arithmetic, logical, and bitwise operations
- These operations include:  **+ , - , * , / *(integer division)* , = , == , !=, < , <= , > , >= , % , | , &**

```python
    from pyipcs import Hex

    # Use int or str as input for hex value
    x = Hex("A")
    y = Hex(-10)

    # Prints "A"
    print(x)

    # Prints "-A"
    print(y)

    # Arithmetic
    a = Hex("8")
    b = Hex(2)

    c = a + b
    d = a - b
    e = a * b
    f = a < b
    g = a | b

    # Prints "A"
    print(c)

    # Prints "6"
    print(d)

    # Prints "10"
    print(e)

    # Prints False
    print(f)

    # Prints "A" (b"1000" logical OR with b"0010")
    print(g)
```

---

### Hex Methods

- **[Back to Hex Object](#hex-object)**

- **[sign](#hexsign)**

- **[unsigned](#hexunsigned)**

- **[get_nibble](#hexget_nibble)**

- **[get_byte](#hexget_byte)**

- **[get_half_word](#hexget_half_word)**

- **[get_word](#hexget_word)**

- **[get_doubleword](#hexget_doubleword)**

- **[to_int](#hexto_int)**

- **[to_str](#hexto_str)**

- **[to_char_str](#hexto_char_str)**

- **[concat](#hexconcat)**

- **[resize](#hexresize)**

- **[bit_len_no_pad](#hexbit_len_no_pad)**

- **[bit_len](#hexbit_len)**

- **[turn_on_bit](#hexturn_on_bit)**

- **[turn_off_bit](#hexturn_off_bit)**

- **[check_bit](#hexcheck_bit)**

---

### Hex.sign

- **[Back to Hex Methods](#hex-methods)**

---

### sign()

#### Description

- Get sign of hex value.

#### Returns

- ***str***: `"-"` or `""` depending on whether Hex is positive or negative

---

### Hex.unsigned

- **[Back to Hex Methods](#hex-methods)**

---

### unsigned()

#### Description

- Get unsigned hex value.

#### Returns

- ***pyipcs.Hex***: Unsigned Hex

---

### Hex.get_nibble

- **[Back to Hex Methods](#hex-methods)**

---

### get_nibble(*nibble*, *from_right=False*)

#### Description

- Get 0 indexed nibble. Default 0 index is from left side of hex string.

#### Parameters

- **nibble** *(int)*: 0 indexed nibble position.
- **from_right** *(bool, optional)*: If `True` will make 0 index the right most nibble. `False` by Default.

#### Returns

- ***pyipcs.Hex***: 0 indexed nibble at position `nibble`

---

### Hex.get_byte

- **[Back to Hex Methods](#hex-methods)**

---

### get_byte(*byte*, *from_right=False*)

#### Description

- Get 0 indexed byte. Default 0 index is from left side of hex string.

#### Parameters

- **byte** *(int)*: 0 indexed byte position.
- **from_right** *(bool, optional)*: If `True` will make 0 index the right most byte. `False` by Default.

#### Returns

- ***pyipcs.Hex***: 0 indexed byte at position `byte`

---

### Hex.get_half_word

- **[Back to Hex Methods](#hex-methods)**

---

### get_half_word(*half_word*, *from_right=False*)

#### Description

- Get 0 indexed half word. Default 0 index is from left side of hex string.

#### Parameters

- **half_word** *(int)*: 0 indexed half word position.
- **from_right** *(bool, optional)*: If `True` will make 0 index the right most half word. `False` by Default.

#### Returns

- ***pyipcs.Hex***: 0 indexed half word at position `half_word`

---

### Hex.get_word

- **[Back to Hex Methods](#hex-methods)**

---

### get_word(*word*, *from_right=False*)

#### Description

- Get 0 indexed word. Default 0 index is from left side of hex string.

#### Parameters

- **word** *(int)*: 0 indexed word position.
- **from_right** *(bool, optional)*: If `True` will make 0 index the right most word. `False` by Default.

#### Returns

- ***pyipcs.Hex***: 0 indexed word at position `word`

---

### Hex.get_doubleword

- **[Back to Hex Methods](#hex-methods)**

---

### get_doubleword(*doubleword*, *from_right=False*)

#### Description

- Get 0 indexed doubleword. Default 0 index is from left side of hex string.

#### Parameters

- **doubleword** *(int)*: 0 indexed doubleword position.
- **from_right** *(bool, optional)*: If `True` will make 0 index the right most doubleword. `False` by Default.

#### Returns

- ***pyipcs.Hex***: 0 indexed doubleword at position `doubleword`

---

### Hex.to_int

- **[Back to Hex Methods](#hex-methods)**

---

### to_int()

#### Description

- Convert hex to an integer.

#### Returns

- ***int***: Hex integer.

---

### Hex.to_str

- **[Back to Hex Methods](#hex-methods)**

---

### to_str()

#### Description

- Convert `Hex` object to a hex string.

#### Returns

- ***str***: Hex string.

---

### Hex.to_char_str

- **[Back to Hex Methods](#hex-methods)**

---

### to_char_str(*encoding="ibm1047"*)

#### Description

- Convert hex to character string.
- If there is an error reading the hex string to characters, will return empty string(`""`).

#### Parameters

- **encoding** *(str, optional)*: Encoding to use to decode hex string. Default is `"ibm1047"`.

#### Returns

- ***str***: Character string.

---

### Hex.concat

- **[Back to Hex Methods](#hex-methods)**

---

### concat(*other*)

#### Description

- Concatenate with other `Hex` Object.

#### Parameters

- **other** *(pyipcs.Hex|Iterable)*: other `Hex` object or Iterable of `Hex` objects to concatenate to the end of the current `Hex` object. Disregard sign of this variable in concatenation.

#### Returns

- ***pyipcs.Hex***: Concatenated `Hex` Object.

---

### Hex.resize

- **[Back to Hex Methods](#hex-methods)**

---

### resize(*new_bit_length*)

#### Description

- Convert hex string to new bit length.
- Will either pad hex string with 0s or truncate string at bit length.

#### Parameters

- **new_bit_length** *(int)*: New length of string in bits.

#### Returns

- ***pyipcs.Hex***: Hex with new bit length.

---

### Hex.bit_len_no_pad

- **[Back to Hex Methods](#hex-methods)**

---

### bit_len_no_pad()

#### Description

- Determine bit length of hex string, not including leading 0s.

#### Returns

- ***int***: Length in bits of hex string, not including leading 0s.

---

### Hex.bit_len

- **[Back to Hex Methods](#hex-methods)**

---

### bit_len()

#### Description

- Determine bit length of hex string, including leading 0s.

#### Returns

- ***int***: Length in bits of hex string, including leading 0s.

---

### Hex.turn_on_bit

- **[Back to Hex Methods](#hex-methods)**

---

### turn_on_bit(*bit_position*, *from_right=False*)

#### Description

- Turn on bit at 0 indexed bit position. Default 0 index is from left side of hex string.

#### Parameters

- **bit_position** *(int)*: 0 indexed bit position.
- **from_right** *(bool, optional)*: If `True` will make 0 index the right most bit. `False` by Default.

#### Returns

- ***pyipcs.Hex***: Hex with bit at bit_position on

---

### Hex.turn_off_bit

- **[Back to Hex Methods](#hex-methods)**

---

### turn_off_bit(*bit_position*, *from_right=False*)

#### Description

- Turn off bit at 0 indexed bit position. Default 0 index is from left side of hex string.

#### Parameters

- **bit_position** *(int)*: 0 indexed bit position.
- **from_right** *(bool, optional)*: If `True` will make 0 index the right most bit. `False` by Default

#### Returns

- ***pyipcs.Hex***: Hex with bit at bit_position off.

---

### Hex.check_bit

- **[Back to Hex Methods](#hex-methods)**

---

### check_bit(*bit_position*, *from_right=False*)

#### Description

- Check bit at 0 indexed bit position. Default 0 index is from left side of hex string.

#### Parameters

- **bit_position** *(int)*: 0 indexed bit position.
- **from_right** *(bool, optional)*: If `True` will make 0 index the right most bit. `False` by Default.

#### Returns

- ***bool***: `True` if bit is on, `False` if it is off.

---
---

## IpcsSession Object

- **[Back to Top](#pyipcs-readme)**
- **[Methods](#ipcssession-methods)**
- **[IpcsAllocations Object](#ipcsallocations-object)**
- **[DumpDirectory Object](#dumpdirectory-object)**
- **[SetDef Custom Subcmd Object](#setdef-custom-subcmd-object)**

---

### *class* pyipcs.IpcsSession(*hlq=None*, *directory=None*, *allocations={"IPCSPARM": ["SYS1.PARMLIB"], "SYSPROC": ["SYS1.SBLSCLI0"],}*)

**Bases:** *object*

### Description

- Manages TSO allocations, session EXECs and DDIRs, and controls settings for IPCS Session.

### Parameters

- **hlq** *(str|None, optional)*: High level qualifier where opened pyIPCS session is or will be under. pyIPCS session includes z/OS MVS datasets for pyIPCS EXECs and DDIRs. High level qualifier has a max length of 16 characters excluding `"."`. By default is `None` which will set the high level qualifier as your userid.

- **directory** *(str|None, optional)*: File system directory where IPCS session directories and files will be placed. By default is `None` which will set the directory as the current working directory of executed file.

- **allocations** *(dict[str,str|list[str]], optional)*: Dictionary of allocations where keys are DD names and values are string data set allocation requests or lists of cataloged datasets. The default allocations are dataset SYS1.PARMLIB for DD name IPCSPARM and dataset SYS1.SBLSCLI0 for DD name SYSPROC.

### Attributes

- **userid** *(str)*: z/OS system userid for current user.
- **hlq** *(str)*: High level qualifier where opened pyIPCS session is or will be under. pyIPCS session includes z/OS MVS datasets for pyIPCS EXECs and DDIRs.
- **directory** *(str)*: File system directory where IPCS session directories and files will be placed. These include subcommand output files and other logs.
- **active** *(bool)*: `True` if IPCS session is active, `False` if not active.
- **aloc** *(pyipcs.IpcsAllocations)*: Manages TSO allocations for your IPCS session. [IpcsAllocations Object](#ipcsallocations-object).
- **ddir** *(pyipcs.DumpDirectory)*: Manages dump directory(DDIR) functionality for your IPCS session. [DumpDirectory Object](#dumpdirectory-object).
- **uid** *(str|None)*: Unique ID for open pyIPCS session. `None` if pyIPCS session is not active.
- **hlq_full** *(str|None)*: Full high level qualifier for open pyIPCS session. `None` if pyIPCS session is not active.
- **directory_full** (str|None): Full directory where pyIPCS files for the open session will be placed. `None` if pyIPCS session is not active.

---

### IpcsSession Methods

- **[Back to IpcsSession Object](#ipcssession-object)**
- **[open](#ipcssessionopen)**
- **[close](#ipcssessionclose)**
- **[init_dump](#ipcssessioninit_dump)**
- **[set_dump](#ipcssessionset_dump)**
- **[evaluate](#ipcssessionevaluate)**

---

### IpcsSession.open

- **[Back to IpcsSession Methods](#ipcssession-methods)**

---

### open()

#### Description

- Opens IPCS/TSO Session.
- Create pyIPCS temporary datasets necessary for pyIPCS operations.

#### Returns

- ***None***

---

### IpcsSession.close

- **[Back to IpcsSession Methods](#ipcssession-methods)**

---

### close()

#### Description

- Closes IPCS/TSO Session.
- Deletes pyIPCS temporary EXECs and temporary DDIRs.

#### Returns

- ***None***

---

### IpcsSession.init_dump

- **[Back to IpcsSession Methods](#ipcssession-methods)**

---

### init_dump(*dsname*, *ddir=""*, *use_cur_ddir=False*)

#### Description

- Initialize/Set dump `dsname` under dump directory `ddir` and return Dump object.
- Will set IPCS session DDIR to `ddir`.
- Will set IPCS default `DSNAME` to `dsname`

#### Parameters

- **dsname** *(str)*: Dump dataset name.
- **ddir** *(str, optional)*: Dump directory. If an empty string, dump will be initialized under temporary DDIR.
- **use_cur_ddir** *(bool, optional)*: Use current session DDIR. Will use the IpcsSession attribute `ddir` to initialize the dump under. This will take precedence over this function's `ddir` parameter. Default is `False`.

#### Returns

- ***pyipcs.Dump***

---

### IpcsSession.set_dump

- **[Back to IpcsSession Methods](#ipcssession-methods)**

---

### set_dump(*dump*)

#### Description

- Set IPCS session DDIR to Dump object DDIR.
- Set IPCS default `DSNAME` to Dump object dataset name.

#### Parameters

- **dump** *(pyipcs.Dump)*

#### Returns

- ***None***

---

### IpcsSession.evaluate

- **[Back to IpcsSession Methods](#ipcssession-methods)**

---

### evaluate(*hex_address*, *dec_offset*, *dec_length*)

#### Description

- Read data from dump. Similar to EVALUATE subcommand in REXX.
- Make sure to set correct defaults `DSNAME`, `ASID`, and `DSPNAME` prior to calling this method.
- [EVALUATE Subcommand](https://www.ibm.com/docs/en/zos/3.1.0?topic=instruction-evaluate-subcommand)

#### Parameters

- **hex_address** *(pyipcs.Hex|str|int)*: Starting hex address to read from.
- **dec_offset** *(int)*: Byte offset from the starting address in decimal.
- **dec_length** *(int)*: Byte length of data to access in decimal.

#### Returns

- ***pyipcs.Hex***: Hex object representing the data at the specified address.

---
---

## IpcsAllocations Object

- **[Back to Top](#pyipcs-readme)**
- **[Back to IpcsSession Object](#ipcssession-object)**
- **[Methods](#ipcsallocations-methods)**

---

**Bases:** *object*

### Description

- Manages TSO allocations for IPCS Session.

---

### IpcsAllocations Methods

- **[Back to IpcsAllocations Object](#ipcsallocations-object)**
- **[get](#ipcsallocationsget)**
- **[set](#ipcsallocationsset)**
- **[drop](#ipcsallocationsdrop)**
- **[update](#ipcsallocationsupdate)**
- **[clear](#ipcsallocationsclear)**

---

### IpcsAllocations.get

- **[Back to IpcsAllocations Methods](#ipcsallocations-methods)**

---

### get()

#### Description

- Get TSO allocations for your IPCS session.

#### Returns

- ***dict[str,str|list[str]]***: Returns dictionary of all allocations where keys are DD names and values are string data set allocation requests or lists of cataloged datasets.

---

### IpcsAllocations.set

- **[Back to IpcsAllocations Methods](#ipcsallocations-methods)**

---

### set(*dd_name*, *specification*, *extend=False*)

#### Description

- Set a single TSO allocation for your IPCS session.

#### Parameters

- **dd_name** *(str)*
- specification *(str|list[str])*: String data set allocation request or list of cataloged datasets.
- **extend** *(bool, optional)*: If `True` and DD name `dd_name` already exists, will add list of datasets from `specification` to `dd_name`. Default is `False`.

#### Returns

- ***None***

---

### IpcsAllocations.drop

- **[Back to IpcsAllocations Methods](#ipcsallocations-methods)**

---

### drop(*dd_name*)

#### Description

- Remove a specific TSO allocation from your IPCS session by DD name if it exists.

#### Parameters

- **dd_name** *(str)*

#### Returns

- ***None***

---

### IpcsAllocations.update

- **[Back to IpcsAllocations Methods](#ipcsallocations-methods)**

---

### update(*new_allocations*, *clear=True*, *extend=False*)

#### Description

- Update multiple TSO allocations for your IPCS session.

#### Parameters

- **new_allocations** *(dict[str,str|list[str]])*: Dictionary of allocations where keys are DD names and values are string data set allocation requests or lists of cataloged datasets.
- **clear** *(bool, optional)*: If `True` will clear all allocations before update. Default is `True`.
- **extend** *(bool, optional)*: If `True`, and `clear` is `False`, and DD name already exists, will add list of datasets from specification to DD name. Default is `False`.

#### Returns

- ***None***

---

### IpcsAllocations.clear

- **[Back to IpcsAllocations Methods](#ipcsallocations-methods)**

---

### clear()

#### Description

- Clear all TSO allocations for your IPCS session.

#### Returns

- ***None***

---
---

## DumpDirectory Object

- **[Back to Top](#pyipcs-readme)**
- **[Back to IpcsSession Object](#ipcssession-object)**
- **[Methods](#dumpdirectory-methods)**
- **[SetDef Custom Subcmd Object](#setdef-custom-subcmd-object)**

---

**Bases:** *object*

### Description

- Manages dump directory(DDIR) for IPCS Session

### Attributes

- **dsname** *(str|None)*: Dataset name of dump directory for your IPCS session. `None` if dump directory is not set.

---

### DumpDirectory Methods

- **[Back to DumpDirectory Object](#dumpdirectory-object)**
- **[use](#dumpdirectoryuse)**
- **[create](#dumpdirectorycreate)**
- **[create_tmp](#dumpdirectorycreate_tmp)**
- **[presets](#dumpdirectorypresets)**
- **[sources](#dumpdirectorysources)**
- **[defaults](#dumpdirectorydefaults)**

---

### DumpDirectory.use

- **[Back to DumpDirectory Methods](#dumpdirectory-methods)**

---

### use(*dsname*)

#### Description

- **dsname** *(str)*: Dump directory that will be set as the session's DDIR.

#### Returns

- ***None***

---

### DumpDirectory.create

- **[Back to DumpDirectory Methods](#dumpdirectory-methods)**

---

### create(*dsname*, ***kwargs*)

#### Description

- Create dump directory.
- Uses `BLSCDDIR` CLIST to create DDIR.
- Adding additional keyword arguments will override pyIPCS DDIR presets.
- [BLSCDDIR CLIST](https://www.ibm.com/docs/en/zos/3.1.0?topic=execs-blscddir-clist-create-dump-directory)

#### Parameters

- **dsname** *(str)*
- **kwargs** *(dict, optional)*: Additional parameters (see other parameters)

#### Other Parameters

- **dataclas** *(str, optional)*
- **mgmtclas** *(str, optional)*
- **ndxcisz** *(int, optional)*
- **records** *(int, optional)*
- **storclas** *(str, optional)*
- **volume** *(str, optional)*
- **blscddir_params** *(str, optional)*: String of `BLSCDDIR` parameters. Write parameters as you would in regular IPCS (ex: `"NDXCISZ(4096)"`).

#### Returns

- ***None***

---

### DumpDirectory.create_tmp

- **[Back to DumpDirectory Methods](#dumpdirectory-methods)**

---

### create_tmp(***kwargs*)

#### Description

- Create temporary dump directory. Will be deleted on IPCS session close.
- Uses `BLSCDDIR` CLIST to create DDIR.
- Adding additional keyword arguments will override pyIPCS DDIR presets.
- [BLSCDDIR CLIST](https://www.ibm.com/docs/en/zos/3.1.0?topic=execs-blscddir-clist-create-dump-directory)

#### Parameters

- **kwargs** *(dict, optional)*: Additional parameters (see other parameters)

#### Other Parameters

- **dataclas** *(str, optional)*
- **mgmtclas** *(str, optional)*
- **ndxcisz** *(int, optional)*
- **records** *(int, optional)*
- **storclas** *(str, optional)*
- **volume** *(str, optional)*
- **blscddir_params** *(str, optional)*: String of `BLSCDDIR` parameters. Write parameters as you would in regular IPCS (ex: `"NDXCISZ(4096)"`).

#### Returns

- ***None***

---

### DumpDirectory.presets

- **[Back to DumpDirectory Methods](#dumpdirectory-methods)**

---

### presets(***kwargs*)

#### Description

- Presets for dump directory creation.
- Parameters that will be added to BLSCDDIR for pyIPCS dump directory creation.
- Input optional parameters to change presets.
- [BLSCDDIR CLIST](https://www.ibm.com/docs/en/zos/3.1.0?topic=execs-blscddir-clist-create-dump-directory)

#### Parameters

- **kwargs** *(dict, optional)*: Additional parameters (see other parameters)

#### Other Parameters

- **dataclas** *(str, optional)*: Specifies the data class for the new directory. If you omit this parameter, there is no data class specified for the new directory.
- **mgmtclas** *(str, optional)*: Specifies the management class for the new directory. If you omit this parameter, there is no management class specified for the new directory.
- **ndxcisz** *(int, optional)*: Specifies the control interval size for the index portion of the new directory. If you omit this parameter, the IBM-supplied default is 4096 bytes.
- **records** *(int, optional)*: Specifies the number of records you want the directory to accommodate. If you omit this parameter, the IBM-supplied default is 5000; your installation's default might vary.
- **storclas** *(str, optional)*: Specifies the storage class for the new directory. If you omit this parameter, there is no storage class specified for the new directory.
- **volume** *(str, optional)*: Specifies the VSAM volume on which the directory should reside. If you omit DATACLAS, MGMTCLAS, STORCLAS, and VOLUME, the IBM-supplied default is VSAM01. Otherwise, there is no IBM-supplied default.
- **blscddir_params** *(str, optional)*: String of `BLSCDDIR` parameters. Write parameters as you would in regular IPCS (ex: `"NDXCISZ(4096)"`).

#### Returns

- ***None***

---

### DumpDirectory.sources

- **[Back to DumpDirectory Methods](#dumpdirectory-methods)**

---

### sources()

#### Description

- Get dataset names of the sources described in the current dump directory of your IPCS session.
- Uses the `LISTDUMP` IPCS subcommand.
- [LISTDUMP Subcommand](https://www.ibm.com/docs/en/zos/3.2.0?topic=subcommands-listdump-subcommand-list-dumps-in-dump-directory)

#### Returns

- ***list[str]***: Returns list of dataset names of the sources described in current the dump directory of your IPCS session.

---

### DumpDirectory.defaults

- **[Back to DumpDirectory Methods](#dumpdirectory-methods)**

---

### defaults(***kwargs*)

#### Description

- Get/Set default values for certain parameters on IPCS subcommands for your IPCS session.
- Uses the `SETDEF LIST` IPCS subcommand.
- IPCS uses the new default value for both your current session and any subsequent sessions in which you use the same user dump directory, until you change the value.
- Note that pyIPCS only sets global defaults.
- [SETDEF Subcommand](https://www.ibm.com/docs/en/zos/3.1.0?topic=subcommands-setdef-subcommand-set-defaults)

#### Parameters

- **kwargs** *(dict, optional)*: Additional parameters (see other parameters)

#### Other Parameters

- **confirm** *(bool, optional)*: `True` for `CONFIRM` parameter. `False` for `NOCONFIRM` parameter.
- **dsname** *(str|None, optional)*: String dataset name to be used for `DSNAME` parameter. `None` for `NODSNAME` parameter.
- **display** *(list[str], optional)*:  List of sub parameters to be used for `DISPLAY` parameter. Possible values in the list can include `"MACHINE"`, `"REMARK"`, `"REQUEST"`, `"STORAGE"`, `"SYMBOL"`, `"ALIGN"`, `"NOMACHINE"`, `"NOREMARK"`, `"NOREQUEST"`, `"NOSTORAGE"`, `"NOSYMBOL"`, `"NOALIGN"`.
- **flag** *(str, optional)*: String severity to be used for `FLAG` parameter. Possible string options include `ERROR`, `INFORMATIONAL`, `SERIOUS`|`SEVERE`, `TERMINATING`, `WARNING`.
- **length** (pyipcs.Hex|str|int, optional): pyipcs.Hex object or string or int to be used for `LENGTH` parameter.
- **pds** (bool, optional): `True` for `PDS` parameter. `False` for `NOPDS` parameter.
- **asid** *(pyipcs.Hex|str|int, optional)*: pyipcs.Hex object or string or int to be used for `ASID` parameter.
- **dspname** *(str, optional)*: String dataspace name to be used for `DSPNAME` parameter.
- **setdef_params** *(str, optional)*: String of `SETDEF` parameters. Write parameters as you would in regular IPCS (ex: `"ACTIVE LENGTH(4)"`).

#### Returns

- ***pyipcs.SetDef***: Custom `SETDEF` Subcmd Object. [SetDef Custom Subcmd Object](#setdef-custom-subcmd-object)

---
---

## SetDef Custom Subcmd Object

- **[Back to Top](#pyipcs-readme)**
- **[Back to IpcsSession Object](#ipcssession-object)**
- **[Back to DumpDirectory Object](#dumpdirectory-object)**

---

**Bases:** *pyipcs.Subcmd*

### Description

- SetDef Custom Subcmd Object
- Runs `SETDEF` with `LIST` parameter and other parameters
- [SETDEF subcommand](https://www.ibm.com/docs/en/zos/3.1.0?topic=subcommands-setdef-subcommand-set-defaults)
- [Address processing parameters](https://www.ibm.com/docs/en/zos/3.1.0?topic=parameter-address-processing-parameters)
- Can generate SetDef object using `pyipcs.IpcsSession.ddir.defaults(..)`
- Only Global Defaults impact the pyIPCS session.

### Attributes

- **data** *(dict)*: Global Defaults. Keys may not appear if information is unknown or unavailable.
  - **"confirm"** *(bool)*: `True` for `CONFIRM`. `False` for `NOCONFIRM`.
  - **"dsname"** *(str|None)*: String dataset name for parameter `DSNAME`. `None` for `NODSNAME`.
  - **"display"** *(list[str]|None)*: List of sub parameters for `DISPLAY` parameter. `None` if `DISPLAY` is not in output. Possible values in the list can include `"MACHINE"`, `"REMARK"`, `"REQUEST"`, `"STORAGE"`, `"SYMBOL"`, `"ALIGN"`, `"NOMACHINE"`, `"NOREMARK"`, `"NOREQUEST"`, `"NOSTORAGE"`, `"NOSYMBOL"`, `"NOALIGN"`.
  - **"flag"** *(str|None)*: String severity for parameter `FLAG`. `None` if `FLAG` is not in output. Possible string options include `"ERROR"`, `"INFORMATIONAL"`, `"SERIOUS"|"SEVERE"`, `"TERMINATING"`, `"WARNING"`.
  - **"length"** *(pyipcs.Hex|None)*: pyipcs.Hex object for parameter `LENGTH`. `None` if `LENGTH` is not in output.
  - **"pds"** *(bool)*: `True` for `PDS`. `False` for `NOPDS`.
  - **"asid"** *(pyipcs.Hex|None)*: pyipcs.Hex object for parameter `ASID`. `None` if `ASID` is not in output.
  - **"dspname"** *(str|None)*: String dataspace name for parameter `DSPNAME`. `None` if `DSPNAME` is not in output.

---
---

## DumpHeader Object

- **[Back to Top](#pyipcs-readme)**
- **[Dump Object](#dump-object)**

---

### *class* pyipcs.DumpHeader(*dsname*)

**Bases:** *dict*

### Description

- Custom Dictionary with info about a dump from the dump header.
- Does not require dump initialization to instantiate object.
- Reference dump header either with `header = DumpHeader(YOUR.DUMP.DSNAME)` or referencing `pyipcs.Dump.header`. [Dump Object](#dump-object)
- Keys may not appear if information is unknown or unavailable.

### Parameters

- **dsname** *(str)*: Dump Dataset Name.

### Keys

- **"dump_type"** *(str)*: `"SAD"`, `"SVCD"`, `"TDMP"`, `"SYSM"`, or `"SLIP"`
- **"sysname"** *(str)*
- **"date_local"** *(str)*
- **"time_local"** *(str)*
- **"title"** *(str)*
- **"original_dump_dsn"** *(str)*
- **"version"** *(int)*: For example z/OS version `3` release `1`
- **"release"** *(int)*: For example z/OS version `3` release `1`
- **"sdrsn"** *(str)*
- **"complete_dump"** *(bool)*
- **"home_jobname"** *(str)*
- **"primary"** *(pyipcs.Hex)*
- **"secondary"** *(pyipcs.Hex)*
- **"home"** *(pyipcs.Hex)*
- **"sdwa_asid"** *(pyipcs.Hex)*
- **"sdwa_address"** *(pyipcs.Hex)*
- **"blocks_allocated_decimal"** *(int)*
- **"remote_sysname"** *(str)*: Appears only if `remote_dump=True`
- **"remote_dump"** *(bool)*
- **"processor_serial_number"** *(str)*
- **"processor_model_number"** *(str)*

### Notes

- The following keys are unknown or unavailable if `dump_type="SAD"`:
  - **"home_jobname"**
  - **"primary"**
  - **"secondary"**
  - **"home"**
  - **"sdwa_asid"**
  - **"sdwa_address"**
  - **"blocks_allocated_decimal"**
  - **"remote_sysname"**
  - **"remote_dump"**

---
---

## Dump Object

- **[Back to Top](#pyipcs-readme)**
- **[Dump Methods](#dump-methods)**

---

**Bases:** *object*

### Description

- Initializes a z/OS dump and stores general information.
- Can create a Dump object using `pyipcs.IpcsSession.init_dump()`

### Attributes

- **dsname** *(str)*: Dump dataset name.
- **ddir** *(str)*: Dump directory when dump was initialized.
- **header** *(pyipcs.DumpHeader)*: Custom dictionary object containing information about the dump from the dump header. [DumpHeader Object](#dumpheader-object)
- **data** *(dict)*: Dictionary containing general information about the dump from various subcommands. Editable by user to store additional info about a dump. Keys may not appear if information is unknown or unavailable.
  - **"sliptrap"** *(str)*: Included in `data` dictionary if the dump is a SLIP dump. Obtained from `LIST SLIPTRAP` subcommand.
  - **"ipl_date_local"** *(str)*: Known if CSA is dumped.
      Obtained from `IPLDATA` subcommand.
  - **"ipl_time_local"** *(str)*: Known if CSA is dumped. Obtained from `IPLDATA` subcommand.
  - **"asids_dumped"** *(list[pyipcs.Hex])*: List of ASIDs that were dumped. Obtained from `CBF RTCT` subcommand.
  - **"asids_all"** *(list[dict])*: Info about all asids on the system at the time of the dump. List of dictionaries containing the hex asid, string jobname, and ASCB address. Obtained from `SELECT ALL` subcommand.
    - **"asid"** *(pyipcs.Hex)*
    - **"jobname"** *(str)*
    - **"ascb_addr"** *(pyipcs.Hex)*
  - **"storage_areas"** *(list[dict])*: Info about dumped storage areas. Contains dataspace information. Obtained from `LISTDUMP` subcommand with `DSNAME` and `SELECT` parameters.
    - **"asid"** *(pyipcs.Hex)*
    - **"total_bytes"** *(pyipcs.Hex|None)*: Total number of bytes dumped for ASID in hex. `None` if total_bytes for ASID is not defined in `LISTDUMP`.
    - **"sumdump"** *(pyipcs.Hex)*: Number of SUMMARY DUMP Data bytes dumped in hex.
    - **"dataspaces"** *(dict)*: Dictionary where the keys are the string dataspace names. Values are `Hex` objects containing the number of bytes dumped for dataspace.

---

### Dump Methods

- **[Back to Dump Object](#dump-object)**
- **[asid_to_jobname](dumpasid_to_jobname)**
- **[jobname_to_asid](dumpjobname_to_asid)**
- **[asid_to_ascb_addr](dumpasid_to_ascb_addr)**

---

### Dump.asid_to_jobname

- **[Back to Dump Methods](#dump-methods)**

---

### asid_to_jobname(*asid*)

#### Description

- Get Jobname from ASID.
- Obtained info from `SELECT ALL` subcommand.

#### Parameters

- **asid** *(pyipcs.Hex|str|int)*

#### Returns

- ***str|None***: Jobname associated with ASID or `None` if ASID is not found.

---

### Dump.jobname_to_asid

- **[Back to Dump Methods](#dump-methods)**

---

### jobname_to_asid(*jobname*)

#### Description

- Get ASID from Jobname.
- Obtained info from `SELECT ALL` subcommand.

#### Parameters

- **jobname** *(str)*

#### Returns

- ***list[pyipcs.Hex]***: List of ASIDs associated with `jobname`.

---

### Dump.asid_to_ascb_addr

- **[Back to Dump Methods](#dump-methods)**

---

### asid_to_ascb_addr(*asid*)

#### Description

- Get ASCB address from ASID.
- Obtained info from `SELECT ALL` subcommand.

#### Parameters

- **asid** *(pyipcs.Hex|str|int)*

#### Returns

- ***pyipcs.Hex|None***: ASCB address associated with ASID or `None` if ASID is not found.

---
---

## Subcmd Object

- **[Back to Top](#pyipcs-readme)**
- **[Extracting and Parsing Subcommand Output](#extracting-and-parsing-subcommand-output)**
- **[Subcmd Methods](#subcmd-methods)**
- **[Creating Custom Subcmd Objects](#creating-custom-subcmd-objects)**

---

### *class* pyipcs.Subcmd(*session*, *subcmd*, *outfile=False*, *keep_file=False*, *auth=False*)

**Bases:** *object*

#### Description

- Runs IPCS subcommand and stores output in string or file.

#### Parameters

- **session** *(pyipcs.IpcsSession)*
- **subcmd** *(str)*: IPCS subcommand to run.
- **outfile** *(bool, optional)*: If `True`, will create and store output in directory `[pyipcs.IpcsSession.directory_full]/subcmd_output/`. File would then be specified in `outfile` attribute of Subcmd object. If `False`, stores output in string specified in `output` attribute of Subcmd object. Default is `False`.
- **keep_file** *(bool, optional)*: If `True` preserves subcommand output file after program execution. If `False` deletes subcommand output file after program execution. Default is `False`.
- **auth** *(bool, optional)*: If `True`, subcommand will be run from an authorized environment. Default is `False`.

#### Attributes

- **subcmd** *(str)*: IPCS subcommand that was ran.
- **outfile** *(str|None)*: File containing subcommand output. `None` if `outfile` parameter in constructor was set to `False` or if file was deleted with `pyipcs.Subcmd.delete_file()` method.
- **output** *(str)*: Returns string containing the entire subcommand output.
- **keep_file** *(bool)*: If `True` preserves subcommand output file after program execution. If `False` deletes subcommand output file after program execution. Editable by user.
- **rc** *(int)*: Return code from running subcommand.
- **data** *(dict)*: Editable by user to store additional info about a IPCS subcommand. Initially empty.

---

### Extracting and Parsing Subcommand Output

- **[Back to Subcmd Object](#subcmd-object)**

---

- **There are a few methods of extracting data from subcommand output**
  - **Find Methods**: Find the index of a particular string within subcommand output.
    - `Subcmd.find`
    - `Subcmd.rfind`
  - **Get Field Methods**: Get a particular value within subcommand output based on a label that precedes the value.
    - `Subcmd.get_field`
    - `Subcmd.get_field2`
    - `Subcmd.rget_field`
    - `Subcmd.rget_field2`
  - **Direct Indexing**

    ```python
    subcmd = Subcmd(session, "STATUS REGISTERS")
    # indexed_output = string of portion of subcommand output
    indexed_output = subcmd[10:20]
    ```

---

### Subcmd Methods

- **[Back to Subcmd Object](#subcmd-object)**
- **[find](#subcmdfind)**
- **[rfind](#subcmdrfind)**
- **[get_field](#subcmdget_field)**
- **[get_field2](#subcmdget_field2)**
- **[rget_field](#subcmdrget_field)**
- **[rget_field2](#subcmdrget_field2)**
- **[delete_file](#subcmddelete_file)**

---

### Subcmd.find

- **[Back to Subcmd Methods](#subcmd-methods)**

---

### find(*substring*, *start=0*, *end=None*)

#### Description

- Find the first occurrence of a substring. Returns `-1` if the value is not found.

#### Parameters

- **substring** *(str)*: Substring to search for.
- **start** *(int, optional)*: Index where to start the search. Default is `0`.
- **end** *(int|None, optional)*: Index where to end the search. Default is `None` for the end of the output.

#### Returns

- ***int***: Output index where substring was found. `-1` if substring was not found.

---

### Subcmd.rfind

- **[Back to Subcmd Methods](#subcmd-methods)**

---

### rfind(*substring*, *start=0*, *end=None*)

#### Description

- Find the last occurrence of a substring. Returns `-1` if the value is not found.

#### Parameters

- **substring** *(str)*: Substring to search for.
- **start** *(int, optional)*: Index where to end the reverse search. Default is `0`.
- **end** *(int|None, optional)*: Index where to start the reverse search. Default is `None` for the end of the output.

#### Returns

- ***int***: Output index where substring was found. `-1` if substring was not found.

---

### Subcmd.get_field

- **[Back to Subcmd Methods](#subcmd-methods)**

---

### get_field(*label*, *end_string*, *separator=""*, *start=0*, *end=None*, *to_hex=False*)

#### Description

- Attempts to get the field value from the output based on a label, separator, and end string.

#### Parameters

- **label** *(str)*: The label of the field.
- **end_string** *(str)*: End string that indicates the end of the value.
- **separator** *(str, optional)*: The separator between the label and the value.
- **start** *(int, optional)*: Index where to start the search. Default is `0`.
- **end** *(int|None, optional)*: Index where to end the search. Default is `None` for the end of the output.
- **to_hex** *(bool, optional)*: Return value as pyipcs.Hex if `to_hex` is `True`. Default is `False` for returning a string.

#### Returns

- ***list***: A list `[value (str|pyipcs.Hex), start (int), end (int)]` where `subcmd[start:end] == value`. `[None, -1, -1]` if field is not found.

---

### Subcmd.get_field2

- **[Back to Subcmd Methods](#subcmd-methods)**

---

### get_field2(*label*, *length*, *separator=""*, *start=0*, *end=None*, *to_hex=False*)

#### Description

- Attempts to get the field value from the output based on a label, separator, and field length.

#### Parameters

- **label** *(str)*: The label of the field.
- **length** *(int)*: Length of the value to get.
- **separator** *(str, optional)*: The separator between the label and the value.
- **start** *(int, optional)*: Index where to start the search. Default is `0`.
- **end** *(int|None, optional)*: Index where to end the search. Default is `None` for the end of the output.
- **to_hex** *(bool, optional)*: Return value as pyipcs.Hex if `to_hex` is `True`. Default is `False` for returning a string.

#### Returns

- ***list***: A list `[value (str|pyipcs.Hex), start (int), end (int)]` where `subcmd[start:end] == value`. `[None, -1, -1]` if field is not found.

---

### Subcmd.rget_field

- **[Back to Subcmd Methods](#subcmd-methods)**

---

### rget_field(*label*, *end_string*, *separator=""*, *start=0*, *end=None*, *to_hex=False*)

#### Description

- Attempts to get the field value in a reverse search from the output based on a label, separator, and end string.

#### Parameters

- **label** *(str)*: The label of the field.
- **end_string** (str): End string that indicates the end of the value.
- **separator** *(str, optional)*: The separator between the label and the value.
- **start** *(int, optional)*: Index where to end the reverse search. Default is `0`.
- **end** *(int|None, optional)*: Index where to start the reverse search. Default is `None` for the end of the output.
- **to_hex** *(bool, optional)*: Return value as pyipcs.Hex if `to_hex` is `True`. Default is `False` for returning a string.

#### Returns

- ***list***: A list `[value (str|pyipcs.Hex), start (int), end (int)]` where `subcmd[start:end] == value`. `[None, -1, -1]` if field is not found.

---

### Subcmd.rget_field2

- **[Back to Subcmd Methods](#subcmd-methods)**

---

### rget_field2(*label*, *length*, *separator=""*, *start=0*, *end=None*, *to_hex=False*)

#### Description

- Attempts to get the field value in a reverse search from the output based on a label, separator, and field length.

#### Parameters

- **label** *(str)*: The label of the field.
- **length** *(int)*: Length of the value to get.
- **separator** *(str, optional)*: The separator between the label and the value.
- **start** *(int, optional)*: Index where to end the reverse search. Default is `0`.
- **end** *(int|None, optional)*: Index where to start the reverse search. Default is `None` for the end of the output.
- **to_hex** *(bool,optional)*. Return value as pyipcs.Hex if `to_hex` is `True`. Default is `False` for returning a string.

---

### Subcmd.delete_file

- **[Back to Subcmd Methods](#subcmd-methods)**

---

### delete_file()

#### Description

- Method to preemptively delete file associated with subcommand. Will not be able to index into file output after completion.

#### Returns

- ***None***

---
---

## Creating Custom Subcmd Objects

- **[Back to Top](#pyipcs-readme)**
- **[Back to Subcmd Object](#subcmd-object)**

---

- pyIPCS allows users to create custom `Subcmd` objects for specific subcommands and or specific issues.

- Users can use the `data` attribute of the `Subcmd` objects to store additional info.

### Creating a Custom Subcmd Object for IPCS Subcommand `YOUR SUBCMD`

```python
from pyipcs import IpcsSession, Subcmd

class YourSubcmd(Subcmd):

    def __init__(self, session:IpcsSession) -> None:

        # Call constructor from original Subcmd object
        super().__init__(session, "YOUR SUBCMD")

        # Store additional info in data dict attribute
        self.data["data_key"] = "data_value"  


session = IpcsSession()
session.open()

# String dataset name of z/OS dump

dsname = ...

dump = session.init_dump(dsname)

# Run 'YOUR SUBCMD' with custom Subcmd object

your_subcmd = YourSubcmd(session)

# Will print 'data_value'

print(your_subcmd.data["data_key"])

session.close()

```

---
---

## Util Functions

- **[Back to Top](#pyipcs-readme)**
- **[is_dump](#pyipcsutilis_dump)**
- **[psw_scrunch](#pyipcsutilpsw_scrunch)**
- **[psw_parse](#pyipcsutilpsw_parse)**
- **[opcode](#pyipcsutilopcode)**
- **[addr_key](#pyipcsutiladdr_key)**
- **[addr_fetch_protected](#pyipcsutiladdr_fetch_protected)**
- **[is_hex](#pyipcsutilis_hex)**
- **[IpcsJsonEncoder](#pyipcsutilipcsjsonencoder)**

---

### How To Import Util Functionality

```python
from pyipcs.util import *
```

---

### pyipcs.util.is_dump

- **[Back To Util Functions](#util-functions)**

---

### is_dump(*dsname*)

#### Description

- Determine whether dataset is a z/OS dump
- Will recall dataset if it exists.

#### Parameters

- **dsname** *(str)*: z/OS dataset name

#### Returns

- ***bool***

---

### pyipcs.util.psw_scrunch

- **[Back To Util Functions](#util-functions)**

---

### psw_scrunch(*psw*)

#### Description

- Scrunch 128 bit PSW to 64 bits
- If 64 bit PSW is inputted as argument return PSW as is

#### Parameters

- **psw** *(pyipcs.Hex)*: 128 bit PSW or 64 bit PSW

#### Returns

- ***pyipcs.Hex***: 64 bit PSW

---

### pyipcs.util.psw_parse

- **[Back To Util Functions](#util-functions)**

---

### psw_parse(*psw*)

#### Description

- Obtain data from PSW.

#### Parameters

- **psw** *(pyipcs.Hex)*: 128 bit PSW or 64 bit PSW.

#### Returns

- ***dict***: data from PSW
  - **"enabled"** *(bool|None)*:  `True` for Enabled for I/O and External Interrupts if bit 6 and 7 are on. `False` for Disabled for I/O and External Interrupts if they are both off. `None` if one of either bit 6 or 7 is on and one is off.
  - **"key"** *(int)*: PSW key.
  - **"privileged"** *(bool)*: `True` for supervisor state(privileged). `False` for problem program state(unprivileged)
  - **"asc_mode"** *(str)*: One of either `"PRIMARY"`, `"AR"`, `"SECONDARY"`, or `"HOME"`.
  - **"cc"** *(int)*: Condition code.
  - **"amode"** *(int|None)*: Either `24`, `31`, `64`, or `None` if invalid.
  - **"instr_addr"** *(pyipcs.Hex)*: Instruction address.

---

### pyipcs.util.opcode

- **[Back To Util Functions](#util-functions)**

---

### opcode(*session*, *instr*)

#### Description

- Get mnemonic of instruction.
- Runs `OPCODE` subcommand.

#### Parameters

- **session** *(pyipcs.Session)*
- **instr** *(str|int|pyipcs.Hex)*: Instruction to get mnemonic from.

#### Returns

- ***str|None***: Instruction mnemonic. Returns `None` if `OPCODE` subcommand returns with non-zero return code or mnemonic can't be found.

---

### pyipcs.util.addr_key

- **[Back To Util Functions](#util-functions)**

---

### addr_key(*session*, *storage_addr*)

#### Description

- Get storage key of storage address.
- Runs `LIST` subcommand with the `DISPLAY` parameter.
- Make sure to set correct defaults `DSNAME`, `ASID`, and `DSPNAME` prior to calling this function.

#### Parameters

- **session** *(pyipcs.IpcsSession)*
- **storage_addr** *(str|int|pyipcs.Hex)*: Storage Address.

#### Returns

- ***int|None***: Storage key. Returns `None` if `LIST` subcommand with the `DISPLAY` parameter subcommand returns with non-zero return code or key can't be determined.

---

### pyipcs.util.addr_fetch_protected

- **[Back To Util Functions](#util-functions)**

---

### addr_fetch_protected(*session*, *storage_addr*)

#### Description

- Return if storage address is fetch protected.
- Runs `LIST` subcommand with the `DISPLAY` parameter.
- Make sure to set correct defaults `DSNAME`, `ASID`, and `DSPNAME` prior to calling this function.

#### Parameters

- **session** *(pyipcs.IpcsSession)*
- **storage_addr** *(str|int|pyipcs.Hex)*: Storage Address.

#### Returns

- ***bool***: `True` if storage_addr is fetch protected, `False` if not. Returns `None` if `LIST` subcommand with the `DISPLAY` parameter subcommand returns with non-zero return code or fetch protected can't be determined.

---

### pyipcs.util.is_hex

- **[Back To Util Functions](#util-functions)**

---

### is_hex(*hex_str*)

#### Description

- Check if string is hex

#### Parameters

- **hex_str** *(str)*

#### Returns

- ***bool***: `True` if string is hex, `False` if not.

---

### pyipcs.util.IpcsJsonEncoder()

- **[Back To Util Functions](#util-functions)**

---

### *class* pyipcs.util.IpcsJsonEncoder()

**Bases:** *json.JSONEncoder*

#### Description

- Custom pyIPCS JSON Encoder.
- Can be specified in the `cls` parameter of `json.dump` and `json.dumps` functions to convert `Hex`, `Dump`, and `Subcmd` objects to JSON.

---
---

## Converting pyIPCS Objects to JSON

- **[Back to Top](#pyipcs-readme)**

---

- pyIPCS objects can be converted to JSON using the [IpcsJsonEncoder](#pyipcsutilipcsjsonencoder) object from the `util` library.

<br>

- **Examples:**

```python
import json
from pyipcs import Hex, IpcsSession, Subcmd
from pyipcs.util import IpcsJsonEncoder

# Setup

dsname = ...
session = IpcsSession()
dump = session.init_dump(dsname)
subcmd = Subcmd(session, "STATUS REGISTERS")

# Convert Hex, Dump, and Subcmd objects to JSON strings

hex_json = json.dumps( { "Key": Hex("1") }, cls=IpcsJsonEncoder)

dump_json = json.dumps(dump, cls=IpcsJsonEncoder)

subcmd_json = json.dumps(subcmd, cls=IpcsJsonEncoder)

# Write Subcmd JSON to file

with open("output.json", "w") as f:
    json.dump(subcmd, f, cls=IpcsJsonEncoder)

```

- `Hex` JSON

```python
{
  "__ipcs_type__": "Hex"
  "value" (str)
}
```

- `Dump` JSON:

```python
{
  "__ipcs_type__": "Dump"
  "dsname" (str)
  "ddir" (str)
  "header" (str)
  "data" (dict)
}
```

- `Subcmd` JSON

```python
{
  "__ipcs_type__": "Subcmd"
  "subcmd" (str)
  "outfile" (str|None)
  "output" (str),
  "keep_file" (bool)
  "rc" (int)
  "data" (dict)
}
```
