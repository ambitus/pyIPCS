# pyIPCS README

- __[Getting Started (Installation Guide)](#getting-started-installation-guide)__
- __[pyIPCS Versioning and Updates](#pyipcs-versioning-and-updates)__
- __[pyIPCS User Guide](#pyipcs-user-guide)__
- __[Report a Bug or Request a Feature](#report-a-bug-or-request-a-feature)__
- __[Contribute to pyIPCS](#contribute-to-pyipcs)__
- __Documentation__
  - __[Hex Object](#hex-object)__
  - __[IpcsSession Object](#ipcssession-object)__
  - __[Dump Object](#dump-object)__
  - __[Subcmd Object](#subcmd-object)__
  - __[Creating Custom Subcmd Objects](#creating-custom-subcmd-objects)__
  - __[SetDef Custom Subcmd Object](#setdef-custom-subcmd-object)__
  - __[Util Functions](#util-functions)__
  - __[pyIPCS Logging](#pyipcs-logging)__

---
---

## pyIPCS Version: `1.0.0`

- __To check your current pyIPCS version:__

```bash
pip show pyipcs
```

---
---

## Example Scripts

- __[Back to Top](#pyipcs-readme)__
- __[Run IPCS subcommand against single z/OS dump](#run-ipcs-subcommand-against-single-zos-dump)__
- __[Run IPCS subcommands against multiple z/OS dumps](#run-ipcs-subcommands-against-multiple-zos-dumps)__

---

### Run IPCS subcommand against single z/OS dump

- __[Back to Example Scripts](#example-scripts)__

```python

# Import pyIPCS objects and util functions
from pyipcs import Hex, IpcsSession, Subcmd
from pyipcs.util import *

# Create IpcsSession object
session = IpcsSession()

# Open IPCS Session
session.open()

# String dataset name of z/OS dump
dsname = ...

# Create Dump object `dump`
# Initializes z/OS dump and stores general info
dump = session.init_dump(dsname)

# Print the dump title
print(dump.data["title"])

# Run IPCS subcommand against z/OS dump `dump` and store output
subcmd = Subcmd(session, "STATUS REGISTERS")

# Print portion of IPCS subcommand output
print(subcmd[10:20])

# Close IPCS Session
session.close()
```

<br>

### Run IPCS subcommands against multiple z/OS dumps

- __[Back to Example Scripts](#example-scripts)__

```python

# Import pyIPCS objects and util functions
from pyipcs import Hex, IpcsSession, Subcmd
from pyipcs.util import *

# Create IpcsSession object
session = IpcsSession()

# Open IPCS Session
session.open()

# String datasets names of z/OS dumps
dsnameA = ...
dsnameB = ...

# Create Dump object `dumpA`
dumpA = session.init_dump(dsnameA)

# Run IPCS subcommand against z/OS dump `dumpA` and store output
subcmdA = Subcmd(session, "LIST TITLE")

# Create Dump object `dumpB`
dumpB = session.init_dump(dsnameB)

# Run IPCS subcommand against z/OS dump `dumpB` and store output
subcmdB = Subcmd(session, "LIST TITLE")

# Set session back to `dumpA`
session.set_dump(dumpA)

# Run IPCS subcommand against z/OS dump `dumpA` and store output
subcmdA2 = Subcmd(session, "STATUS REGISTERS")

# Close IPCS Session
session.close()
```

---
---

## Getting Started (Installation Guide)

- __[Back to Top](#pyipcs-readme)__

---

### [Getting Started](./GETTING_STARTED.md)

- __Contains information about:__
  - __Dependencies and Prerequisites__
  - __pyIPCS Installation__

---
---

## pyIPCS Versioning and Updates

- __[Back to Top](#pyipcs-readme)__

---

### Example Version: `1.2.3`

- __Major Version (`1`)__
  - Indicates a significant update.
  - Probable to include breaking changes that are not backward-compatible.
- __Minor Version (`2`)__
  - Adds new features or functionality.
  - Mostly backward-compatible with previous versions within the same major version.
- __Patch Version (`3`)__
  - Fixes bugs or makes small improvements.
  - Always backward-compatible.

#### [CHANGELOG.md](./CHANGELOG.md)

- __The Changelog file contains info on changes between each new version__

---
---

## pyIPCS User Guide

- __[Back to Top](#pyipcs-readme)__

---

### [User Guide](./USER_GUIDE.md)

- __To get the most out of pyIPCS, we strongly recommend checking out the User Guide.__
<br>

- __The User Guide provides:__
  - __Key Features:__ Learn about the core capabilities and functionality of the package.
  - __Best Practices:__ Discover tips and recommendations for optimal performance and maintainability.
  - __Advanced Features:__ Dive deeper into advanced functionality to unlock the full potential of the package.

---
---

## Report a Bug or Request a Feature

- __[Back to Top](#pyipcs-readme)__

---

- __To report a bug, or request a feature or other update, please open a new issue.__
  - Once you open an issue, there are templates for submitting a Bug Report, Feature Request, Documentation Update, or other requests you might have for pyIPCS

---
---

## Contribute to pyIPCS

- __[Back to Top](#pyipcs-readme)__

---

### [How to Contribute to pyIPCS](./CONTRIBUTING.md)

- __Follow the link above to get information on how to contribute to pyIPCS__

---
---

## Hex Object

- __[Back to Top](#pyipcs-readme)__
- __[Arithmetic, Logical, and Bitwise Operations With Hex Object](#arithmetic-logical-and-bitwise-operations-with-hex-object)__
- __[Methods](#hex-methods)__

---

### *class* pyipcs.Hex(*value*)

__Bases:__ *object*

#### Description

- Contains various methods and functionality to manage hex variables in an IPCS environment
- Accepts strings or integers as input

#### Args

- __value__ *(str|int)*: hex string or integer for hex value

---

### Arithmetic, Logical, and Bitwise Operations With Hex Object

- __[Back to Hex Object](#hex-object)__

---

- The `Hex` object supports a variety of arithmetic, logical, and bitwise operations
- These operations include:  __+ , - , * , / *(integer division)* , = , == , !=, < , <= , > , >= , % , | , &__

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

- __[Back to Hex Object](#hex-object)__
- __[sign](#hexsign)__
- __[unsigned](#hexsign)__
- __[get_nibble](#hexget_nibblenibble-from_right)__
- __[get_byte](#hexget_bytebyte-from_right)__
- __[get_half_word](#hexget_half_wordhalf_word-from_right)__
- __[get_word](#hexget_wordword-from_right)__
- __[get_doubleword](#hexget_doubleworddoubleword-from_right)__
- __[to_int](#hexto_int)__
- __[to_str](#hexto_str)__
- __[to_char_str](#hexto_char_str)__
- __[concat](#hexconcatother)__
- __[resize](#hexresizenew_bit_length)__
- __[bit_len_no_pad](#hexbit_len_no_pad)__
- __[bit_len](#hexbit_len)__
- __[turn_on_bit](#hexturn_on_bitbit_position-from_right)__
- __[turn_off_bit](#hexturn_off_bitbit_position-from_right)__
- __[check_bit](#hexcheck_bitbit_position-from_right)__

---

### Hex.sign()

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Get sign of hex value.

#### Returns

- __*str*__: `'-'` or `''` depending on whether Hex is positive or negative

---

### Hex.unsigned()

- __[Back to Hex Methods](#hex-methods)__  

#### Description

- Get unsigned hex value.

#### Returns

- __*pyipcs.Hex*__: unsigned Hex

---

### Hex.get_nibble(*nibble*, *from_right*)

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Get 0 indexed nibble. Default 0 index is from left side of hex string.

#### Args

- __nibble__ *(int)*: 0 indexed nibble position.
- __from_right__ *(bool)*: __Optional__. If `True` will make 0 index the right most nibble. `False` by Default.

#### Returns

- __*pyipcs.Hex*__: 0 indexed nibble at position `nibble`

---

### Hex.get_byte(*byte*, *from_right*)

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Get 0 indexed byte. Default 0 index is from left side of hex string.

#### Args

- __byte__ *(int)*: 0 indexed byte position.
- __from_right__ *(bool)*: __Optional__. If `True` will make 0 index the right most byte. `False` by Default.

#### Returns

- __*pyipcs.Hex*__: 0 indexed byte at position `byte`

---

### Hex.get_half_word(*half_word*, *from_right*)

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Get 0 indexed half word. Default 0 index is from left side of hex string.

#### Args

- __half_word__ *(int)*: 0 indexed half word position.
- __from_right__ *(bool)*: __Optional__. If `True` will make 0 index the right most half word. `False` by Default.

#### Returns

- __*pyipcs.Hex*__: 0 indexed half word at position `half_word`

---

### Hex.get_word(*word*, *from_right*)

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Get 0 indexed word. Default 0 index is from left side of hex string.

#### Args

- __word__ *(int)*: 0 indexed word position.
- __from_right__ *(bool)*: __Optional__. If `True` will make 0 index the right most word. `False` by Default.

#### Returns

- __*pyipcs.Hex*__: 0 indexed word at position `word`

---

### Hex.get_doubleword(*doubleword*, *from_right*)

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Get 0 indexed doubleword. Default 0 index is from left side of hex string.

#### Args

- __doubleword__ *(int)*: 0 indexed doubleword position.
- __from_right__ *(bool)*: __Optional__. If `True` will make 0 index the right most doubleword. `False` by Default.

#### Returns

- __*pyipcs.Hex*__: 0 indexed doubleword at position `doubleword`

---

### Hex.to_int()

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Convert hex to an integer.

#### Returns

- __*int*__: hex integer

---

### Hex.to_str()

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Convert `Hex` object to a hex string.

#### Returns

- __*str*__: hex string

---

### Hex.to_char_str()

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Convert hex to character string.
- If there is an error reading the hex string to characters, will return empty string('').

#### Args

- __encoding__ *(str)*: __Optional__. Encoding to use to decode hex string. Default is `'ibm1047'`.

#### Returns

- __*str*__: character string

---

### Hex.concat(*other*)

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Concatenate with other `Hex` Object

#### Args

- __other__ *(pyipcs.Hex|Iterable)*: other `Hex` object or Iterable of `Hex` objects to concatenate to the end of the current `Hex` object. Disregard sign of this variable in concatenation.

#### Returns

- __*pyipcs.Hex*__: Concatenated `Hex` Object

---

### Hex.resize(*new_bit_length*)

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Convert hex string to new bit length.
- Will either pad hex string with 0s or truncate string at bit length.

#### Args

- __new_bit_length__ *(int)*: new length of string in bits.

#### Returns

- __*pyipcs.Hex*__: hex with new bit length.

---

### Hex.bit_len_no_pad()

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Determine bit length of hex string, not including leading 0s.

#### Returns

- __*int*__: Length in bits of hex string, not including leading 0s

---

### Hex.bit_len()

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Determine bit length of hex string, including leading 0s.

#### Returns

- __*int*__: Length in bits of hex string, including leading 0s

---

### Hex.turn_on_bit(*bit_position*, *from_right*)

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Turn on bit at 0 indexed bit position. Default 0 index is from left side of hex string.

#### Args

- __bit_position__ *(int)*: 0 indexed bit position.
- __from_right__ *(bool)*: __Optional__. If `True` will make 0 index the right most bit. `False` by Default.

#### Returns

- __*pyipcs.Hex*__: hex with bit at bit_position on

---

### Hex.turn_off_bit(*bit_position*, *from_right*)

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Turn off bit at 0 indexed bit position. Default 0 index is from left side of hex string

#### Args

- __bit_position__ *(int)*: 0 indexed bit position
- __from_right__ *(bool)*: __Optional__. If `True` will make 0 index the right most bit. `False` by Default

#### Returns

- __*pyipcs.Hex*__: hex with bit at bit_position off

---

### Hex.check_bit(*bit_position*, *from_right*)

- __[Back to Hex Methods](#hex-methods)__

#### Description

- Check bit at 0 indexed bit position. Default 0 index is from left side of hex string.

#### Args

- __bit_position__ *(int)*: 0 indexed bit position.
- __from_right__ *(bool)*: __Optional__. If `True` will make 0 index the right most bit. `False` by Default.

#### Returns

- __*bool*__: `True` if bit is on, `False` if it is off

---
---

## IpcsSession Object

- __[Back to Top](#pyipcs-readme)__
- __[Methods](#ipcssession-methods)__

---

### *class* pyipcs.IpcsSession(*hlq*, *directory*, *allocations*)

__Bases:__ *object*

#### Description

- Manages TSO allocations, temporary EXECs and DDIRs, and controls settings for IPCS Session.

#### Args

- __hlq__ *(str|None)*: __Optional__. High level qualifier used for temporary z/OS MVS datasets for pyIPCS temporary EXECs and DDIRs. By default `None` is specified which will set the high level qualifier as your userid.
<br>

- __directory__ *(str|None)*: __Optional__. File system directory where IPCS session directories and files will be placed. By default `None` is specified which will set the directory as the current working directory of executed file.
<br>

- __allocations__ *(dict[str,str|list[str]])*: __Optional__. Dictionary of allocations where keys are DD names and values are string data set allocation requests or lists of cataloged datasets. The default allocations are dataset SYS1.PARMLIB for DD name IPCSPARM and dataset SYS1.SBLSCLI0 for DD name SYSPROC.

#### Attributes

- __userid__ *(str)*: z/OS system userid for current user.
- __hlq__ *(str)*: High level qualifier used for temporary z/OS MVS datasets for pyIPCS EXECs and DDIRs.
- __directory__ *(str)*: File system directory where IPCS session directories and files will be placed. These include subcommand output files and other logs.
- __active__ *(bool)*: `True` if IPCS session is active, `False` if not active.
- __ddir__ *(str|None)*: DDIR that IPCS will use to run subcommands. `None` if session is not active.
- __logger__ *(pyipcs.PyIPCSLogger)*: Manages logging for the pyIPCS session.

---

### IpcsSession Methods

- __[Back to IpcsSession Object](#ipcssession-object)__
- __[open](#ipcssessionopen)__
- __[close](#ipcssessionclose)__
- __[get_allocations](#ipcssessionget_allocations)__
- __[set_allocation](#ipcssessionset_allocationdd_name-specification)__
- __[update_allocations](#ipcssessionupdate_allocationsnew_allocations-clear_old_allocations)__
- __[create_ddir](#ipcssessioncreate_ddirddir)__
- __[create_temp_ddir](#ipcssessioncreate_temp_ddir)__
- __[set_ddir](#ipcssessionset_ddirddir)__
- __[get_defaults](#ipcssessionget_defaults)__
- __[set_defaults](#ipcssessionset_defaultsconfirm-dsname-nodsname-asid-dspname-other)__
- __[init_dump](#ipcssessioninit_dumpdsname-ddir)__
- __[set_dump](#ipcssessionset_dumpdump)__
- __[dsname_in_ddir](#ipcssessiondsname_in_ddirdsname)__
- __[evaluate](#ipcssessionevaluatehex_address-dec_offset-dec_length)__

---

### IpcsSession.open()

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Opens IPCS/TSO Session.
- Create pyIPCS temporary datasets necessary for pyIPCS operations.

#### Returns

- __*None*__

---

### IpcsSession.close()

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Closes IPCS/TSO Session.
- Deletes pyIPCS temporary EXECs and temporary DDIRs.

#### Returns

- __*None*__

---

### IpcsSession.get_allocations()

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Get allocations for your TSO environment.

#### Returns

- __*dict[str,str|list[str]]*__: Returns dictionary of all allocations where keys are DD names and values are string data set allocation requests or lists of cataloged datasets

---

### IpcsSession.set_allocation(*dd_name*, *specification*)

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Set a TSO allocation.
- If the specification is an empty list or empty string, will remove or not include DD name-specification pair within allocations

#### Args

- __dd_name__ *(str)*
- __specifications__ *(str|list[str])*: string data set allocation request or list of cataloged datasets

#### Returns

- __*None*__

---

### IpcsSession.update_allocations(*new_allocations*, *clear_old_allocations*)

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Update multiple TSO allocations.

#### Args

- __new_allocations__ *(dict[str,str|list[str]])*: Dictionary of allocations where keys are DD names and values are string data set allocation requests or lists of cataloged datasets.
- __clear_old_allocations__ *(bool)*: __Optional__. If `True`, will clear all old allocations before setting new allocations. Default is `True`.

#### Returns

- __*None*__

---

### IpcsSession.create_ddir(*ddir*)

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Create dump directory.

#### Args

- __ddir__ *(str)*: Dump directory that will be created

#### Returns

- __*None*__

---

### IpcsSession.create_temp_ddir()

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Create temporary dump directory. Will be deleted on session close.

#### Returns

- __*str*__: Temporary DDIR dataset name

---

### IpcsSession.set_ddir(*ddir*)

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Set `ddir` as the current dump directory for the session.

#### Args

__ddir__ *(str)*: Dump directory will be set as the sessions DDIR

#### Returns

- __*None*__

---

### IpcsSession.get_defaults()

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Run `SETDEF LIST` to get IPCS defaults.

#### Returns

- __*pyipcs.SetDef*__: Custom `SETDEF` Subcmd Object. `outfile` parameter is set to `False` for string output.

---

### IpcsSession.set_defaults(*confirm*, *dsname*, *nodsname*, *asid*, *dspname*, *other*)

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Runs `SETDEF` with `LIST` parameter and other parameters to set IPCS defaults
- [SETDEF subcommand](https://www.ibm.com/docs/en/zos/3.1.0?topic=subcommands-setdef-subcommand-set-defaults)
- [Address processing parameters](https://www.ibm.com/docs/en/zos/3.1.0?topic=parameter-address-processing-parameters)
- Only Global Defaults impact the pyIPCS session.

#### Args

- __confirm__ *(bool|None)*: __Optional__. `True` for `CONFIRM` parameter. `False` for `NOCONFIRM` parameter. Default is `None` to not include parameter in subcommand.
- __dsname__ *(str|None)*: __Optional__. String dataset name to be used for `DSNAME` parameter. Default is `None` to not include parameter in subcommand.
- __nodsname__ *(bool)*: __Optional__. `True` for `NODSNAME` parameter. Default is `False` to not include parameter in subcommand.
- __asid__ *(pyipcs.Hex|str|int|None)*: __Optional__. pyipcs.Hex object or string or int to be used for `ASID` parameter. Default is `None` to not include parameter in subcommand.
- __dspname__ *(str|None)*: __Optional__.
    String dataspace name to be used for `DSPNAME` parameter. Default is `None` to not include parameter in subcommand.
- __other__ *(str|None)*: __Optional__. String of other parameters to include in `SETDEF`. Write other parameters as you would in regular IPCS (ex: `'ACTIVE LENGTH(4)'`). Default is `None` to not include in subcommand.

#### Returns

- __*pyipcs.SetDef*__: Custom `SETDEF` Subcmd Object. `outfile` parameter is set to `False` for string output.

---

### IpcsSession.init_dump(*dsname*, *ddir*)

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Initialize/Set dump `dsname` under dump directory `ddir` and return Dump object.
- Will set IPCS session DDIR to `ddir`.
- Will set IPCS default `DSNAME` to `dsname`

#### Args

- __dsname__ *(str)*: Dump dataset name.
- __ddir__ *(str)*: __Optional__. Dump directory. If not specified, dump will be initialized under temporary DDIR.'
- __use_cur_ddir__ *(bool)*: __Optional__. Use current session DDIR. Will use the IpcsSession attribute `ddir` to initialize the dump under. This will take precedence over this function's `ddir` parameter. Default is `False`.

#### Returns

- __*pyipcs.Dump*__

---

### IpcsSession.set_dump(*dump*)

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Set IPCS session DDIR to Dump object DDIR.
- Set IPCS default `DSNAME` to Dump object dataset name.

#### Args

- __dump__ *(pyipcs.Dump)*

#### Returns

- __*None*__

---

### IpcsSession.dsname_in_ddir(*dsname*)

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Check if dataset is a source described in the current session DDIR.
- Used to check if a dump dataset was initialized under the current DDIR.

#### Args

- __dsname__ *(str)*: Dataset name.

#### Returns

- __*bool*__: `True` if dataset name a source described in the current DDIR, `False` if not.

---

### IpcsSession.evaluate(*hex_address*, *dec_offset*, *dec_length*)

- __[Back to IpcsSession Methods](#ipcssession-methods)__

#### Description

- Read data from dump. Similar to EVALUATE subcommand in REXX.
- Make sure to set correct defaults `DSNAME`, `ASID`, and `DSPNAME` prior to calling this method.
- [EVALUATE Subcommand](https://www.ibm.com/docs/en/zos/3.1.0?topic=instruction-evaluate-subcommand)

#### Args

- __hex_address__ *(pyipcs.Hex|str|int)*: Starting hex address to read from
- __dec_offset__ *(int)*: Byte offset from the starting address in decimal
- __dec_length__ *(int)*: Byte length of data to access in decimal

#### Returns

- __*pyipcs.Hex*__: Hex object representing the data at the specified address

---
---

## Dump Object

- __[Back to Top](#pyipcs-readme)__
- __[Dump Methods](#dump-methods)__

---
---

### *class* pyipcs.Dump(*session*, *dsname*, *ddir*)

__Bases:__ *object*

#### Description

- Initializes a z/OS dump and stores general information.
- Can create a Dump object using `pyipcs.IpcsSession.init_dump()`
<br>

- __On Dump object initialization:__
  - Sets regular or temporary DDIR for dump and parses out general info about dump from various subcommands
  - Initializes/Sets dump `dsname` under dump directory `ddir`.
  - Will set IPCS `session` DDIR to `ddir`.
  - Will set IPCS default `DSNAME` to `dsname`

#### Args

- __session__ *(pyipcs.IpcsSession)*: IPCS Session.
- __dsname__ *(str)*: Dump dataset name.
- __ddir__ *(str)*: __Optional__. Dump directory. If not specified, dump will be initialized under temporary DDIR which will be deleted on session close.
- __use_cur_ddir__ *(bool)*: __Optional__. Use current session DDIR. Will use the IpcsSession attribute `ddir` to initialize the dump under. This will take precedence over this function's `ddir` parameter. Default is `False`.

#### Attributes

- __dsname__ *(str)*: Dump dataset name.
- __ddir__ *(str|None)*: Dump directory when dump was initialized.
- __data__ *(dict)*: Dictionary containing general data about the dump. Editable by user to store additional info about a dump. __If Dump object cannot find or parse one of the `data` dictionary items below, the item will not be included in the `data` dictionary.__
  - `'dump_type'` (str): 'SAD', 'SVCD', 'TDMP', 'SYSM', or 'SLIP'
  - `'sysname'` *(str)*
  - `'date_local'` *(str)*
  - `'time_local'` *(str)*
  - `'title'` *(str)*
  - `'original_dump_dsn'` *(str)*
  - `'version'` *(int)*: For example z/OS version `3` release `1`
  - `'release'` *(int)*: For example z/OS version `3` release `1`
  - `'sdrsn'` *(str)*
  - `'complete_dump'` *(bool)*
  - `'home_jobname'` *(str)*: Not included if `'dump_type'=='SAD'`.
  - `'primary'` *(pyipcs.Hex)*: Not included if `'dump_type'=='SAD'`.
  - `'secondary'` *(pyipcs.Hex)*: Not included if `'dump_type'=='SAD'`.
  - `'home'` *(pyipcs.Hex)*: Not included if `'dump_type'=='SAD'`.
  - `'sdwa_asid'` *(pyipcs.Hex)*: Not included if `'dump_type'=='SAD'`.
  - `'sdwa_address'` *(pyipcs.Hex)*: Not included if `'dump_type'=='SAD'`.
  - `'blocks_allocated_decimal'` *(int)*: Not included if `'dump_type'=='SAD'`.
  - `'remote_sysname'` *(str)*: Included only if `'remote_dump'==True`. Not included if `'dump_type'=='SAD'`.
  - `'remote_dump'` *(bool)*: Not included if `'dump_type'=='SAD'`.
  - `'processor_serial_number'` *(str)*
  - `'processor_model_number'` *(str)*
  - `'sliptrap'` *(str)*: Included in `data` dictionary if `'dump_type'=='SLIP'`. Obtained from `LIST SLIPTRAP` subcommand.
  - `'ipl_date_local'` *(str)*: Included in 'data' dictionary if CSA is dumped. Obtained from `IPLDATA` subcommand.
  - `'ipl_time_local'` *(str)*: Included in 'data' dictionary if CSA is dumped. Obtained from `IPLDATA` subcommand.
  - `'asids_dumped'` *(list[pyipcs.Hex])*: list of ASIDs that were dumped. Obtained from `CBF RTCT` subcommand.
  - `'asids_all'` *(dict)*: Info about all asids on the system at the time of the dump. Keys are the hex ASIDs on the system and values are a dictionary containing the string jobname and ASCB address. Obtained from `SELECT ALL` subcommand.
  - `pyipcs.Hex(ASID)` *(dict)*:
    - `'jobname'` *(str)*
    - `'ascb_addr'` *(pyipcs.Hex)*
  - `'storage_areas'` *(dict)*: Info about dumped storage areas. Obtained from `LISTDUMP` subcommand with parameters `DSNAME` and `SELECT`.
    - `pyipcs.Hex(ASID)` *(dict)*
      - `'total_bytes'` *(pyipcs.Hex|None)* : Total number of bytes dumped for ASID in hex. `None` if total_bytes for ASID is not defined in `LISTDUMP`.
      - `'sumdump'` *(pyipcs.Hex)*: Number of SUMMARY DUMP Data bytes dumped in hex.
      - `'dataspaces'` *(dict)*:`{ str(Dataspace Name) : pyipcs.Hex(Number of bytes dumped for dataspace in hex) }`

---

### Dump Methods

- __[Back to Dump Object](#dump-object)__
- __[asid_to_jobname](#dumpasid_to_jobnameasid)__
- __[jobname_to_asid](#dumpjobname_to_asidjobname)__
- __[asid_to_ascb_addr](#dumpasid_to_ascbaddrasid)__

---

### Dump.asid_to_jobname(*asid*)

- __[Back to Dump Methods](#dump-methods)__

#### Description

- Get Jobname from ASID.
- Obtained info from `SELECT ALL` subcommand

#### Args

- __asid__ *(pyipcs.Hex|str|int)*

#### Returns

- __*str|None*__: Jobname associated with ASID or `None` if ASID is not found

---

### Dump.jobname_to_asid(*jobname*)

- __[Back to Dump Methods](#dump-methods)__

#### Description

- Get ASID from Jobname.
- Obtained info from `SELECT ALL` subcommand

#### Args

- __jobname__ *(str)*

#### Returns

- __*list[pyipcs.Hex]*__: List of ASIDs associated with `jobname`

---

### Dump.asid_to_ascbaddr(*asid*)

- __[Back to Dump Methods](#dump-methods)__

#### Description

- Get ASCB address from ASID.
- Obtained info from `SELECT ALL` subcommand

#### Args

- __asid__ *(pyipcs.Hex|str|int)*

#### Returns

- __*pyipcs.Hex|None*__: ASCB address associated with ASID or `None` if ASID is not found

---
---

## Subcmd Object

- __[Back to Top](#pyipcs-readme)__
- __[Extracting and Parsing Subcommand Output](#extracting-and-parsing-subcommand-output)__
- __[Subcmd Methods](#subcmd-methods)__

---

### *class* pyipcs.Subcmd(*session*, *subcmd*, *outfile*, *keep_file*)

__Bases:__ *object*

#### Description

- Runs IPCS subcommand and stores output in string or file.

#### Args

- __session__ *(pyipcs.IpcsSession)*
- __subcmd__ *(str)*: IPCS subcommand to run.
- __outfile__ *(bool)*: __Optional__. If `True`, will create and store output in directory `[pyipcs.IpcsSession.directory]/pyipcs_session/[time of session open]/subcmd_output/`. File would then be specified in `outfile` attribute of Subcmd object. If `False`, stores output in string specified in `output` attribute of Subcmd object. Default is `False`.
- __keep_file__ *(bool)*: __Optional__. If `True` preserves subcommand output file after program execution. If `False` deletes subcommand output file after program execution. Default is `False`.

#### Attributes

- __subcmd__ *(str)*: IPCS subcommand that was ran
- __outfile__ *(str|None)*: File containing subcommand output. `None` if `outfile` parameter in constructor was set to `False` or if file was deleted with `pyipcs.Subcmd.delete_file()` method.
- __output__ *(str)*: Returns string containing the entire subcommand output.
- __keep_file__ *(bool)*: If `True` preserves subcommand output file after program execution. If `False` deletes subcommand output file after program execution. Editable by user.
- __rc__ *(int)*: Return code from running subcommand.
- __data__ *(dict)*: Editable by user to store additional info about a IPCS subcommand. Initially empty.

---

### Extracting and Parsing Subcommand Output

- __[Back to Subcmd Object](#subcmd-object)__

---

#### Refer to User Guide Section - [Subcmd Indexing, Find, and Get Field Methods](./USER_GUIDE.md#subcmd-indexing-find-and-get-field-methods)

- __*Provides More Detailed Explanation*__

<br>

- __Indexing:__

```python
subcmd = Subcmd(session, "STATUS REGISTERS")
# indexed_output = string of portion of subcommand output
indexed_output = subcmd[10:20]
```

- __Find and Get Field Methods:__
  - *Listed in __[Subcmd Methods](#subcmd-methods)__*

---

### Subcmd Methods

- __[Back to Subcmd Object](#subcmd-object)__
- __[find](#subcmdfindsubstring-start-end)__
- __[rfind](#subcmdrfindsubstring-start-end)__
- __[get_field](#subcmdget_fieldlabel-end_string-separator-start-end-to_hex)__
- __[get_field2](#subcmdget_field2label-length-separator-start-end-to_hex)__
- __[rget_field](#subcmdrget_fieldlabel-end_string-separator-start-end-to_hex)__
- __[rget_field2](#subcmdrget_field2label-length-separator-start-end-to_hex)__
- __[delete_file](#subcmddelete_file)__

---

### Subcmd.find(*substring*, *start*, *end*)

- __[Back to Subcmd Methods](#subcmd-methods)__

#### Description

- Find the first occurrence of a substring. Returns `-1` if the value is not found.

#### Args

- __substring__ *(str)*: Substring to search for.
- __start__ *(int)*: __Optional__. Index where to start the search. Default is `0`.
- __end__ *(int|None)*: __Optional__. Index where to end the search. Default is `None` for the end of the output.

#### Returns

- __*int*__: Output index where substring was found. `-1` if substring was not found.

---

### Subcmd.rfind(*substring*, *start*, *end*)

- __[Back to Subcmd Methods](#subcmd-methods)__

#### Description

- Find the last occurrence of a substring. Returns `-1` if the value is not found.

#### Args

- __substring__ *(str)*: Substring to search for
- __start__ *(int)*: __Optional__. Index where to end the reverse search. Default is `0`.
- __end__ *(int|None)*: __Optional__. Index where to start the reverse search. Default is `None` for the end of the output.

#### Returns

- __*int*__: Output index where substring was found. `-1` if substring was not found.

---

### Subcmd.get_field(*label*, *end_string*, *separator*, *start*, *end*, *to_hex*)

- __[Back to Subcmd Methods](#subcmd-methods)__

#### Description

- Attempts to get the field value from the output based on a label, separator, and end string.

#### Args

- __label__ *(str)*: The label of the field.
- __end_string__ *(str)*: End string that indicates end of value.
- __separator__ *(str)*: __Optional__. The separator between the label and the value.
- __start__ *(int)*: __Optional__. Index where to start the search. Default is `0`.
- __end__ *(int|None)*: __Optional__. Index where to end the search. Default is `None` for the end of the output.
- __to_hex__ *(bool)*: __Optional__. Return value as pyipcs.Hex if `to_hex` is `True`. Default is `False` for returning a string.

#### Returns

- __*list*__: A list `[value (str|pyipcs.Hex), start (int), end (int)]` where `subcmd[start:end] == value`. `[None, -1, -1]` if field is not found.

---

### Subcmd.get_field2(*label*, *length*, *separator*, *start*, *end*, *to_hex*)

- __[Back to Subcmd Methods](#subcmd-methods)__

#### Description

- Attempts to get the field value from the output based on a label, separator, and field length.

#### Args

- __label__ *(str)*: The label of the field.
- __length__ *(int)*: Length of value to get.
- __separator__ *(str)*: __Optional__. The separator between the label and the value.
- __start__ *(int)*: __Optional__. Index where to start the search. Default is `0`.
- __end__ *(int|None)*: __Optional__. Index where to end the search. Default is `None` for the end of the output.
- __to_hex__ *(bool)*: __Optional__. Return value as pyipcs.Hex if `to_hex` is `True`. Default is `False` for returning a string.

#### Returns

- __*list*__: A list `[value (str|pyipcs.Hex), start (int), end (int)]` where `subcmd[start:end] == value`. `[None, -1, -1]` if field is not found.

---

#### Subcmd.rget_field(*label*, *end_string*, *separator*, *start*, *end*, *to_hex*)

- __[Back to Subcmd Methods](#subcmd-methods)__

#### Description

- Attempts to get the field value in a reverse search from the output based on a label, separator, and end string.

#### Args

- __label__ *(str)*: The label of the field.
- __end_string__ (str): End string that indicates end of value.
- __separator__ *(str)*: __Optional__. The separator between the label and the value.
- __start__ *(int)*: __Optional__. Index where to end the reverse search. Default is `0`.
- __end__ *(int|None)*: __Optional__. Index where to start the reverse search. Default is `None` for the end of the output.
- __to_hex__ *(bool)*: __Optional__. Return value as pyipcs.Hex if `to_hex` is `True`. Default is `False` for returning a string.

#### Returns

- __*list*__: A list `[value (str|pyipcs.Hex), start (int), end (int)]` where `subcmd[start:end] == value`. `[None, -1, -1]` if field is not found.

---

#### Subcmd.rget_field2(*label*, *length*, *separator*, *start*, *end*, *to_hex*)

- __[Back to Subcmd Methods](#subcmd-methods)__

#### Description

- Attempts to get the field value in a reverse search from the output based on a label, separator, and field length.

#### Args

- __label__ *(str)*: The label of the field.
- __length__ *(int)*: Length of value to get.
- __separator__ *(str)*: __Optional__. The separator between the label and the value.
- __start__ *(int)*: __Optional__. Index where to end the reverse search. Default is `0`.
- __end__ *(int|None)*: __Optional__. Index where to start the reverse search. Default is `None` for the end of the output.
- __to_hex__ *(bool)*. __Optional__. Return value as pyipcs.Hex if `to_hex` is `True`. Default is `False` for returning a string.

---

#### Subcmd.delete_file()

- __[Back to Subcmd Methods](#subcmd-methods)__

#### Description

- Method to preemptively delete file associated with subcommand. Will not be able to index into file output after completion.

#### Returns

- __*None*__

---
---

## Creating Custom Subcmd Objects

- __[Back to Top](#pyipcs-readme)__

---

- pyIPCS allows users to create custom `Subcmd` objects for specific issues and subcommands.
<br>

- Users can use the `data` attribute of the `Subcmd` objects to store additional info.
<br>

### Creating a Custom Subcmd Object for IPCS Subcommand `YOUR SUBCMD`

```python
from pyipcs import IpcsSession, Subcmd

class YourSubcmd(Subcmd):

    def __init__(
        self, 
        session:IpcsSession, 
        outfile:bool=False,
        keep_file:bool=False,
    ) -> None:

        # Call constructor from original Subcmd object
        super().__init__(
            session,
            "YOUR SUBCMD",
            outfile=outfile,
            keep_file=keep_file,   
        )

        # Store additional info in data dict attribute
        self.data["new_subcmd_data_key"] = "new_subcmd_data_value"  


session = IpcsSession()
session.open()

# String dataset name of z/OS dump
dsname = ...

dump = session.init_dump(dsname)

# Run 'YOUR SUBCMD' with custom Subcmd object
your_subcmd = YourSubcmd(session)

# Will print 'new_subcmd_data_value'
print(your_subcmd.data["new_subcmd_data_key"])

session.close()
```

---
---

## SetDef Custom Subcmd Object

- __[Back to Top](#pyipcs-readme)__

---

### *class* pyipcs.SetDef(*session*, *confirm*, *dsname*, *nodsname*, *asid*, *dspname*, *other*, *outfile*, *keep_file*)

__Bases:__ *pyipcs.Subcmd*

#### Description

- Runs SETDEF with LIST parameter and other parameters
- [SETDEF subcommand](https://www.ibm.com/docs/en/zos/3.1.0?topic=subcommands-setdef-subcommand-set-defaults)
- [Address processing parameters](https://www.ibm.com/docs/en/zos/3.1.0?topic=parameter-address-processing-parameters)
- Can create a pyipcs.SetDef object using `pyipcs.IpcsSession.get_defaults()` and `pyipcs.IpcsSession.set_defaults()`
- Only Global Defaults impact the pyIPCS session.

#### Args

- __session__ *(pyipcs.IpcsSession)*
- __confirm__ *(bool|None)*: __Optional__. `True` for `CONFIRM` parameter. `False` for `NOCONFIRM` parameter. Default is `None` to not include parameter in subcommand.
- __dsname__ *(str|None)*: __Optional__. String dataset name to be used for `DSNAME` parameter. Default is `None` to not include parameter in subcommand.
- __nodsname__ *(bool)*: __Optional__. `True` for `NODSNAME` parameter. Default is `False` to not include parameter in subcommand.
- __asid__ *(pyipcs.Hex|str|int|None)*: __Optional__. pyipcs.Hex object or string or int to be used for `ASID` parameter. Default is `None` to not include parameter in subcommand.
- __dspname__ *(str|None)*: __Optional__. String dataspace name to be used for `DSPNAME` parameter. Default is `None` to not include parameter in subcommand.
- __other__ *(str|None)*: __Optional__. String of other parameters to include in `SETDEF`. Write other parameters as you would in regular IPCS (ex: `'ACTIVE LENGTH(4)'`). Default is `None` to not include in subcommand.
- __outfile__ *(bool)*: __Optional__.
- __keep_file__ *(bool)*: __Optional__.

#### Attributes

- __subcmd__ *(str)*: `SETDEF` subcommand that was ran
- __outfile__ *(str|None)*
- __output__ *(str|None)*
- __keep_file__ *(bool)*
- __rc__ *(int)*
- __data__ *(dict)*: Global Defaults. If Global Defaults are not found in the output the `data` dictionary will be empty.
  - `'confirm'` *(bool)*: `True` for parameter `CONFIRM`. `False` for parameter `NOCONFIRM`.
  - `'dsname'` *(str|None)*: String dataset name for parameter DSNAME. `None` for parameter `NODSNAME`.
  - `'asid'` *(pyipcs.Hex|None)*: pyipcs.Hex object for parameter `ASID`. `None` if parameter `ASID` is not included.
  - `'dspname'` *(str|None)*: String dataspace name for parameter `DSPNAME`. `None` if parameter `DSPNAME` is not included.

---
---

## Util Functions

- __[Back to Top](#pyipcs-readme)__
- __[is_dump](#pyipcsutilis_dumpdsname)__
- __[dump_header_data](#pyipcsutildump_header_datadsname)__
- __[psw_scrunch](#pyipcsutilpsw_scrunchpsw)__
- __[psw_parse](#pyipcsutilpsw_parsepsw)__
- __[opcode](#pyipcsutilopcodesession-instr)__
- __[addr_key](#pyipcsutiladdr_keysession-storage_addr)__
- __[addr_fetch_protected](#pyipcsutiladdr_fetch_protectedsession-storage_addr)__
- __[is_hex](#pyipcsutilis_hexhex_str)__

---

### How To Import Util Functions

```python
from pyipcs.util import *
```

---

### pyipcs.util.is_dump(*dsname*)

- __[Back To Util Functions](#util-functions)__

#### Description

- Determine whether dataset is a z/OS dump

#### Args

- __dsname__ *(str)*: z/OS dataset name

#### Returns

- __*bool*__

---

### pyipcs.util.dump_header_data(*dsname*)

- __[Back To Util Functions](#util-functions)__

#### Description

- Obtain info about z/OS dump from dump header without the need to create a Dump object

#### Args

- __dsname__ *(str)*: z/OS dataset name

#### Returns

- __*dict*__: Info about z/OS dump obtained from dump header
  - `'dump_type'` (str): 'SAD', 'SVCD', 'TDMP', 'SYSM', or 'SLIP'
  - `'sysname'` *(str)*
  - `'date_local'` *(str)*
  - `'time_local'` *(str)*
  - `'title'` *(str)*
  - `'original_dump_dsn'` *(str)*
  - `'version'` *(int)*: For example z/OS version `3` release `1`
  - `'release'` *(int)*: For example z/OS version `3` release `1`
  - `'sdrsn'` *(str)*
  - `'complete_dump'` *(bool)*
  - `'home_jobname'` *(str)*: Not included if `'dump_type'=='SAD'`.
  - `'primary'` *(pyipcs.Hex)*: Not included if `'dump_type'=='SAD'`.
  - `'secondary'` *(pyipcs.Hex)*: Not included if `'dump_type'=='SAD'`.
  - `'home'` *(pyipcs.Hex)*: Not included if `'dump_type'=='SAD'`.
  - `'sdwa_asid'` *(pyipcs.Hex)*: Not included if `'dump_type'=='SAD'`.
  - `'sdwa_address'` *(pyipcs.Hex)*: Not included if `'dump_type'=='SAD'`.
  - `'blocks_allocated_decimal'` *(int)*: Not included if `'dump_type'=='SAD'`.
  - `'remote_sysname'` *(str)*: Included only if `'remote_dump'==True`. Not included if `'dump_type'=='SAD'`.
  - `'remote_dump'` *(bool)*: Not included if `'dump_type'=='SAD'`.
  - `'processor_serial_number'` *(str)*
  - `'processor_model_number'` *(str)*

---

### pyipcs.util.psw_scrunch(*psw*)

- __[Back To Util Functions](#util-functions)__

#### Description

- Scrunch 128 bit PSW to 64 bits
- If 64 bit PSW is inputted as argument return PSW as is

#### Args

- __psw__ *(pyipcs.Hex)*: 128 bit PSW or 64 bit PSW

#### Returns

- __*pyipcs.Hex*__: 64 bit PSW

---

### pyipcs.util.psw_parse(*psw*)

- __[Back To Util Functions](#util-functions)__

#### Description

- Obtain data from PSW

#### Args

- __psw__ *(pyipcs.Hex)*: 128 bit PSW or 64 bit PSW

#### Returns

- __*dict*__: data from PSW
  - `'enabled'` *(bool|None)*: `True` for Enabled for I/O and External Interrupts if bit 6 and 7 are on. `False` for Disabled for I/O and External Interrupts if they are both off. `None` if one of either bit 6 or 7 is on and one is off.
  - `'key'` *(int)*: PSW key
  - `'privileged'` *(bool)*: `True` for supervisor state(privileged). `False` for problem program state(unprivileged)
  - `'asc_mode'` *(str)*: One of either `'PRIMARY'`, `'AR'`, `'SECONDARY'`, or `'HOME'`
  - `'cc'` *(int)*: Condition code
  - `'amode'` *(int|None)*: Either `24`, `31`, `64`, or `None` if invalid
  - `'instr_addr'` *(pyipcs.Hex)*: Instruction address

---

### pyipcs.util.opcode(*session*, *instr*)

- __[Back To Util Functions](#util-functions)__

#### Description

- Get mnemonic of instruction
- Runs `OPCODE` subcommand

#### Args

- __session__ *(pyipcs.Session)*
- __instr__ *(str|int|pyipcs.Hex)*: Instruction to get mnemonic from

#### Returns

- __*str|None*__: Instruction mnemonic. Returns `None` if `OPCODE` subcommand returns with non-zero return code or mnemonic can't be found.

---

### pyipcs.util.addr_key(*session*, *storage_addr*)

- __[Back To Util Functions](#util-functions)__

#### Description

- Get storage key of storage address.
- Runs `LIST` subcommand with the `DISPLAY` parameter.
- Make sure to set correct defaults `DSNAME`, `ASID`, and `DSPNAME` prior to calling this function.

#### Args

- __session__ *(pyipcs.IpcsSession)*
- __storage_addr__ *(str|int|pyipcs.Hex)*: Storage Address

#### Returns

- __*int|None*__: Storage key. Returns `None` if `LIST` subcommand with the `DISPLAY` parameter subcommand returns with non-zero return code or key can't be determined.

---

### pyipcs.util.addr_fetch_protected(*session*, *storage_addr*)

- __[Back To Util Functions](#util-functions)__

#### Description

- Return if storage address is fetch protected
- Runs `LIST` subcommand with the `DISPLAY` parameter.
- Make sure to set correct defaults `DSNAME`, `ASID`, and `DSPNAME` prior to calling this function.

#### Args

- __session__ *(pyipcs.IpcsSession)*
- __storage_addr__ *(str|int|pyipcs.Hex)*: Storage Address.

#### Returns

- __*bool*__: `True` if storage_addr is fetch protected, `False` if not. Returns `None` if `LIST` subcommand with the `DISPLAY` parameter subcommand returns with non-zero return code or fetch protected can't be determined.

---

### pyipcs.util.is_hex(*hex_str*)

- __[Back To Util Functions](#util-functions)__

#### Description

- Check if string is hex

#### Args

- __hex_str__ *(str)*

#### Returns

- __*bool*__: `True` if string is hex, `False` if not

---
---

## pyIPCS Logging

- __[Back to Top](#pyipcs-readme)__
- __[Logging Introduction](#logging-introduction)__
- __[PyIPCSLogger Object](#pyipcslogger-object)__

---

### Logging Introduction

- __[Back to pyIPCS Logging](#pyipcs-logging)__
- __[General Logging Information](#general-logging-information)__
- __[Log Levels](#log-levels)__
- __[Log Files](#log-files)__
- __[Default pyIPCS Log Records](#default-pyipcs-log-records)__
- __[How to Set Log Levels and Create Records](#how-to-set-log-levels-and-create-records)__

---

#### General Logging Information

- __[Back to Logging Introduction](#logging-introduction)__

---
<br>

- pyIPCS logging is enabled while the pyIPCS session is open
  - *Between calls of `pyipcs.IpcsSession.open()` and `pyipcs.IpcsSession.close()`*
<br>

- pyIPCS Logging is managed by the PyIPCSLogger object, which is stored in the attribute `pyipcs.IpcsSession.logger`
<br>

- __*All pyIPCS log records are outputted in JSON format*__

---

#### Log Levels

- __[Back to Logging Introduction](#logging-introduction)__

---

- There are two separate log levels for the pyIPCS session
  - __The Console Log Level__
  - __The Directory Log Level__
<br>

- __Console Log Level:__ Controls log level for records outputted to console.
- __Directory Log Level:__ Controls log level for records outputted to files. Log files are placed in directory `[pyipcs.IpcsSession.directory]/pyipcs_session/[time of session open]/logs/`
<br>

- __Use log level, `NO_LOG` to not display any records__
  - *The Console Log Level and Directory Log Level are `NO_LOG` by default*
<br>

- *__Note:__ Only records at the specified log level and higher priority will be processed*
<br>

- __Log levels and their priority:__

| Log Level | Priority |
| --- | --- |
| `DEBUG` | Lowest |
| `SUBCMD` | Lower |
| `DUMP` | V |
| `SESSION` | V |
| `INFO` | V |
| `WARNING` | V |
| `ERROR` | Higher|
| `CRITICAL` | Highest |

---

#### Log Files

- __[Back to Logging Introduction](#logging-introduction)__

---

- Files potentially contained in `../logs/` directory:
  - `error.log`
  - `session.log`
  - `dump.log`
  - `subcmd.log`
  - `all.log`

| Console/Log File | Records Processed |
| --- | --- |
| `error.log` | Log Levels: `WARNING`, `ERROR`, and `CRITICAL`|
| `session.log` | Log Level: `SESSION`|
| `dump.log` | Log Level: `DUMP`|
| `subcmd.log` | Log Level: `SUBCMD`|
| `all.log` | All Log Levels Excluding: `NO_LOG`|
| *console* | All Log Levels Excluding: `NO_LOG`|

- *__Note:__ in order for records to be processed the corresponding Directory or Console Log Level must also be met or be of lower priority*

---

#### Default pyIPCS Log Records

- __[Back to Logging Introduction](#logging-introduction)__

---

- __By default pyIPCS already has records for specific log levels:__

| Log Level | Messages |
| --- | --- |
| `SUBCMD` | `CREATED SUBCMD OBJECT`, `RUNNING SUBCMD`|
| `DUMP` | `CREATED DUMP OBJECT`, `START INITIALIZE DUMP`, `FINISH INITIALIZE DUMP`, `RUNNING DUMP OBJECT SUBCMDS`, `SET DUMP` |
| `SESSION` | `SET ALLOCATION`, `CREATE DDIR`, `SET DDIR`|
| `WARNING` | `CAUGHT WARNING` - All warnings using `warnings.warn()`|
| `ERROR` | `UNCAUGHT EXCEPTION` - All uncaught exceptions|

---

#### How to Set Log Levels and Create Records

- __[Back to Logging Introduction](#logging-introduction)__

---

- __Get the current Console Log Level and Directory Log Level:__

```python
session = IpcsSession()

session.open()

# Print Console Log Level: NO_LOG
print(session.logger.get_console_level())

# Print Directory Log Level: NO_LOG
print(session.logger.get_directory_level())

session.close()
```

- __Set current Console Log Level and Directory Log Level:__

```python
session = IpcsSession()

session.open()

# Set the Console Log Level
session.set_console_level("DUMP")

# Print Console Log Level: DUMP
print(session.logger.get_console_level())

# Set the Directory Log Level
session.set_console_level("SUBCMD")

# Print Directory Log Level: SUBCMD
print(session.logger.get_directory_level())

session.close()
```

- __Log Record:__

```python
session = IpcsSession()

# Set the Directory Log Level
session.set_directory_level("SUBCMD")

session.open()

# Print Directory Log Level: SUBCMD
print(session.logger.get_directory_level())

# Log Records: Will appear in subcmd.log and all.log: 

# Record = {"time": [record time], "level": "SUBCMD", "message": "TEST MESSAGE 1"}
session.logger.log("SUBCMD", "TEST MESSAGE 1")

# Record = {"time": [record time], "level": "SUBCMD", "message": "TEST MESSAGE 2", "test_key": "test_value"}
session.logger.log("SUBCMD", "TEST MESSAGE 2", extra={"test_key": "test_value"})

session.close()
```

---

### PyIPCSLogger Object

- __[Back to pyIPCS Logging](#pyipcs-logging)__
- __[PyIPCSLogger Methods](#pyipcslogger-methods)__

---

### *class* pyipcs.PyIPCSLogger

__Bases:__ *object*

#### Description

- Logging Object for pyIPCS
- Attribute `logger` of the IpcsSession object is of type `pyipcs.PyIPCSLogger` and manages logging for the pyIPCS session.

#### Attributes

- __logging_directory__ *(str)*: Directory where log files are placed in.

---

### PyIPCSLogger Methods

- __[Back to PyIPCSLogger Object](#pyipcslogger-object)__
- __[get_console_level](#pyipcsloggerget_console_level)__
- __[get_directory_level](#pyipcsloggerget_directory_level)__
- __[set_console_level](#pyipcsloggerset_console_levelnew_level)__
- __[set_directory_level](#pyipcsloggerset_directory_levelnew_level)__
- __[log](#pyipcsloggerloglevel-message-extra)__

---

### PyIPCSLogger.get_console_level()

- __[Back To PyIPCSLogger Methods](#pyipcslogger-methods)__

#### Description

- Get log level for records outputted to console.

#### Returns

- __*str*__: Log level. Will be one of `'DEBUG'`, `'SUBCMD'`, `'DUMP'`, `'SESSION'`, `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`, or `'NO_LOG'`

---

### PyIPCSLogger.get_directory_level()

- __[Back To PyIPCSLogger Methods](#pyipcslogger-methods)__

#### Description

- Get log level for records outputted to files.

#### Returns

- __*str*__: Log level. Will be one of `'DEBUG'`, `'SUBCMD'`, `'DUMP'`, `'SESSION'`, `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`, or `'NO_LOG'`

---

### PyIPCSLogger.set_console_level(*new_level*)

- __[Back To PyIPCSLogger Methods](#pyipcslogger-methods)__

#### Description

- Set log level for records outputted to console.

#### Args

- __new_level__ *(str)*: New log level. Should be one of `'DEBUG'`, `'SUBCMD'`, `'DUMP'`, `'SESSION'`, `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`, or `'NO_LOG'`

#### Returns

- __*None*__

---

### PyIPCSLogger.set_directory_level(*new_level*)

- __[Back To PyIPCSLogger Methods](#pyipcslogger-methods)__

#### Description

- Set log level for records outputted to files.

#### Args

- __new_level__ *(str)*: New log level. Should be one of `'DEBUG'`, `'SUBCMD'`, `'DUMP'`, `'SESSION'`, `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`, or `'NO_LOG'`

#### Returns

- __*None*__

---

### PyIPCSLogger.log(*level*, *message*, *extra*)

- __[Back To PyIPCSLogger Methods](#pyipcslogger-methods)__

#### Description

- Log a record with `message` and `level` in JSON.
- By default the record will include the time, `level`, and `message`.
- Can include extra key value pairs for the record using the optional `extra` parameter.

#### Args

- __level__ *(str)*: Log level. Should be one of `'DEBUG'`, `'SUBCMD'`, `'DUMP'`, `'SESSION'`, `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`, or `'NO_LOG'`
- __message__ *(str)*
- __extra__ *(dict)*: __Optional__. Extra key-value pairs to include in record. Should follow JSON format.

#### Returns

- __*None*__
