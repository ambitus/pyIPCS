# pyIPCS User Guide

- __[Introduction](#introduction)__
- __[Managing pyIPCS Temporary EXECs and Temporary DDIRs](#managing-pyipcs-temporary-execs-and-temporary-ddirs)__
- __[Managing Subcommand Output Files and Log Files](#managing-subcommand-output-files-and-log-files)__
- __[Managing TSO Allocations](#managing-tso-allocations)__
- __[Initializing a Dump and Managing Dump Directories](#initializing-a-dump-and-managing-dump-directories)__
- __[Using the pyIPCS Hex Object](#using-the-pyipcs-hex-object)__
- __[Running IPCS Subcommands and Storing Output](#running-ipcs-subcommands-and-storing-output)__
- __[Subcmd Indexing, Find, and Get Field Methods](#subcmd-indexing-find-and-get-field-methods)__
- __[Retrieving Raw Dump Data](#retrieving-raw-dump-data)__

---
---

## Introduction

- __[Back to Top](#pyipcs-user-guide)__
- __[Example Scripts](#example-scripts)__
- __[Hex Object](#hex-object)__
- __[IpcsSession Object](#ipcssession-object)__
- __[Dump Object](#dump-object)__
- __[Subcmd Object](#subcmd-object)__

---

### Example Scripts

- __[Back to Top](#pyipcs-user-guide)__
- __[Back to Introduction](#introduction)__
- __[Run IPCS subcommand against single z/OS dump](#run-ipcs-subcommand-against-single-zos-dump)__
- __[Run IPCS subcommands against multiple z/OS dumps](#run-ipcs-subcommands-against-multiple-zos-dumps)__

---

#### Run IPCS subcommand against single z/OS dump

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

#### Run IPCS subcommands against multiple z/OS dumps

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

### Hex Object

- __[Back to Top](#pyipcs-user-guide)__
- __[Back to Introduction](#introduction)__

---

```python

x = Hex("A")
y = Hex(10)
z = x + y
```

- Manages hex variables in an IPCS environment
- Supports a variety of arithmetic, logical, and bitwise operations

---

### IpcsSession Object

- __[Back to Top](#pyipcs-user-guide)__
- __[Back to Introduction](#introduction)__

---

```python

session = IpcsSession()
```

- Manages TSO allocations, temporary EXECs and DDIRs, and controls settings for an IPCS Session.
<br>

- Use the `open` method to open your IPCS Session.
- Use the `close` method to close your IPCS Session.
  - While you can explicitly call the `close` method, pyIPCS will also close the IPCS Session after program execution on deletion of the `IpcsSession` object.
<br>

- You can set the TSO allocations for IPCS Session through the `allocations` parameter and the `set_allocation` and `update_allocations` methods.
<br>

- You can set the DDIR associated with the session using the method `set_ddir` which will be reflected in the `ddir` attribute.
<br>

- IPCS session defaults can be viewed using the `get_defaults` method and set defaults using the `set_defaults` method.
<br>

- During the current IPCS Session, the IpcsSession object will create temporary EXECs, temporary DDIRs, and other files.
  - The location of temporary EXECs, temporary DDIRs, and other files are customizable using the `hlq` and `directory` parameters.

---

### Dump Object

- __[Back to Top](#pyipcs-user-guide)__
- __[Back to Introduction](#introduction)__

---

```python

session = IpcsSession()
dump = session.init_dump("MY.DUMP.DSNAME")
```

- Can create dump object using `IpcsSession` method `init_dump`.
- Initializes a z/OS dump and stores general information.
- Can specify a specific dump directory using the optional `ddir` parameter
  - If no DDIR is specified, pyIPCS will create and use temporary DDIR.
<br>

- The `IpcsSession` methods `init_dump` and `set_dump` will set the session's DDIR and the IPCS `DSNAME` default so that subcommands can be run against a specific dump.
<br>

- Stores general info about the z/OS dump within the `data` dictionary attribute gathered from the dump header and a few other IPCS subcommands.
  - The `data` dictionary attribute is editable by the user to store additional information

---

### Subcmd Object

- __[Back to Top](#pyipcs-user-guide)__
- __[Back to Introduction](#introduction)__

---

```python
subcmd = Subcmd(session, "STATUS REGISTERS")
```

- Runs IPCS subcommand and stores output in string or file.
<br>

- You can set the optional parameter `outfile` to `True` to have the output be stored in a file if the subcommand output is too large or you would like to preserve the output.
  - Set the optional parameter `keep_file` to `True` to preserve subcommand file output after program execution and the deletion of the `Subcmd` object.
  - Can explicitly call the `delete_file` method to delete the subcommand output file before deletion of `Subcmd` object.
<br>

- The `IpcsSession` methods `init_dump` and `set_dump` will set the session's DDIR and the IPCS `DSNAME` default so that subcommands can be run against a specific dump.
<br>

- Can directly index into `Subcmd` object to grab portion of subcommand output, regardless if the output is stored in a string or file.
  - Can use the editable `data` dictionary attribute to store important info from the subcommand output.

---
---

## Managing pyIPCS Temporary EXECs and Temporary DDIRs

- __[Back to Top](#pyipcs-user-guide)__

---

- In order to perform operations the `IpcsSession` object creates temporary EXECs and temporary DDIRs, while the IPCS Session is open.

```python

from pyipcs import Hex, IpcsSession, Dump, Subcmd
from pyipcs.util import *

session = IpcsSession()

# Creates temporary EXECs for pyIPCS operations
session.open()

# String dataset name of z/OS dump
dsname = ...

# ddir parameter is not specified -> temporary DDIR is created and dump is initialized
dump = session.init_dump(dsname)
```

<br>

- The high level qualifier of these temporary EXECs and temporary DDIRs is reflected in the `hlq` attribute
<br>

- __Default HLQ For Temporary EXECs and DDIRs is your z/OS system userid__
<br>

- __Example:__
  - __z/OS userid: `MYUSER`__

```python

from pyipcs import Hex, IpcsSession, Dump, Subcmd
from pyipcs.util import *

session = IpcsSession()

session.open()

# Will print 'MYUSER'
print(session.hlq)
```

<br>

- You can change this location using the corresponding `hlq` parameter

```python

from pyipcs import Hex, IpcsSession, Dump, Subcmd
from pyipcs.util import *

session = IpcsSession(hlq="NEW.HLQ")

session.open()

# Will print 'NEW.HLQ'
print(session.hlq)
```

<br>

- Temporary EXECs and temporary DDIRs will be deleted after program execution on deletion of the `IpcsSession` object, or after the IPCS Session is closed.

```python

session = IpcsSession()

# Creates temporary EXECs for pyIPCS operations
session.open()

# Deletes temporary EXECs and temporary DDIRs
session.close()

# Open IPCS Session again and create temporary EXECs for pyIPCS operations
session.open()

# Program is finished: Close IPCS Session and delete temporary EXECs and temporary DDIRs
```

---
---

## Managing Subcommand Output Files

- __[Back to Top](#pyipcs-user-guide)__

---

- IPCS subcommand output can be stored in files by setting the optional parameter `outfile` to `True` in the `Subcmd` object

```python

# Subcommand output file is created
subcmd = Subcmd(session, "STATUS REGISTERS", outfile=True)
```

<br>

- The directory containing these subcommand output files and log files is reflected in the `directory` attribute of the `IpcsSession` object

<br>

- __Default `IpcsSession` Directory: `Current Working Directory`__
<br>

- __Example:__
  - __pyIPCS Script: `/path/to/file/pyipcs_script.py`__

```python

from pyipcs import Hex, IpcsSession, Dump, Subcmd
from pyipcs.util import *

session = IpcsSession()

session.open()

# Will print '/path/to/file/'
print(session.directory)
```

- You can change this location using the corresponding `directory` parameter

```python

from pyipcs import Hex, IpcsSession, Dump, Subcmd
from pyipcs.util import *

session = IpcsSession(directory="/new/path/")

session.open()

# Will print '/new/path/'
print(session.directory) 
```

<br>

- __Subcommand Output Directory:__ `[pyipcs.IpcsSession.directory]/pyipcs_session/[time of session open]/subcmd_output/`
- __Log File Directory:__ `[pyipcs.IpcsSession.directory]/pyipcs_session/[time of session open]/logs/`

<br>

- Subcommand output files will not be deleted and will be preserved after program execution on deletion of the `Subcmd` object if the `keep_file` optional parameter is set to `True`.

```python

# Subcommand output file is created and keep_file is set to True
subcmd = Subcmd(session, "STATUS REGISTERS", outfile=True, keep_file=True)

# Program is finished: Preserve subcommand output file
```

<br>

- If the `keep_file` parameter is set to `False` (`keep_file` is set to `False` by default), and the `outfile` parameter is set to `True`, the subcommand output file will be deleted after program execution on deletion of the `Subcmd` object.

```python

# Subcommand output file is created but keep_file is set to False by default
subcmd = Subcmd(session, "STATUS REGISTERS", outfile=True)

# Program is finished: Delete subcommand output file
```

<br>

- You can also explicitly delete the subcommand output file with the `delete_file` method of the `Subcmd` object. Note that you will not be able to reference subcommand output after execution of this function. The `delete_file` method will take precedence over `keep_file=True` and will delete the file

```python

# Deletes subcommand output file associated with subcommand
subcmd.delete_file()
```

---
---

## Managing TSO Allocations

- __[Back to Top](#pyipcs-user-guide)__

---

- pyIPCS TSO allocations are represented as a Python dictionary with the keys as the DD names and the values as a string data set allocation request or list of cataloged data set names.
<br>

- __Default the TSO allocations for the IPCS session:__

```python

{
    "IPCSPARM" : ["SYS1.PARMLIB"],
    "SYSPROC" : ["SYS1.SBLSCLI0"]
}
```

- *__Note:__* pyIPCS will include other temporary datasets/EXECs under DD name SYSEXEC as well behind the scenes.

<br>

- __Generally, to call IPCS subcommands you must have `SYS1.PARMLIB` under DD name `IPCSPARM` and `SYS1.SBLSCLI0` under DD name `SYSPROC`__
  - __If the names/locations of `SYS1.PARMLIB` and `SYS1.SBLSCLI0` have changed, make sure this is reflected in your current IPCS session's allocations__

<br>

- You can use the following `IpcsSession` methods to customize your TSO allocations for your IPCS Session.
  - Using the optional `allocations` parameter in the `IpcsSession` constructor.
  - `set_allocation`
  - `update_allocations`
- You can view the current allocations for your IPCS Session with the `IpcsSession` method `get_allocations`.

---
---

## Initializing a Dump and Managing Dump Directories

- __[Back to Top](#pyipcs-user-guide)__

---

- You can use the `init_dump` method to initialize a z/OS dump under a specific DDIR using the `ddir` optional parameter.
<br>

- `init_dump` will return a `Dump` object

```python

# pyIPCS Session
session = IpcsSession()
session.open()

# String dataset name of z/OS dump
dsname = ...

# DDIR I want initialize z/OS dump dsname under
ddir = "MY.DDIR"

# Initialize z/OS dump under MY.DDIR and store general info
dump = session.init_dump(dsname, ddir=ddir)

# Will print 'MY.DDIR'
print(dump.ddir)
```

- In the above example, if `MY.DDIR` did not exist, it would first be created, then the z/OS dump would be initialized under that DDIR

<br>

- If the `ddir` parameter is not specified then a temporary DDIR will be used that will be placed under the high level qualifier `session.hlq + ".TEMPDDIR"`
  - Temporary DDIRs are deleted on session `close` or after the program has finished executing.

```python

# pyIPCS Session
session = IpcsSession()
session.open()

# String dataset name of z/OS dump
dsname1 = ...

# String dataset name of another z/OS dump
dsname2 = ...

# Initialize z/OS dumps with temporary ddirs
dump1 = session.init_dump(dsname1)
dump2 = session.init_dump(dsname2)

# Will print session.hlq + '.TEMPDDIR.N1'
print(dump1.ddir)

# Will print session.hlq + '.TEMPDDIR.N2'
print(dump2.ddir)

# Program Finished: IPCS Session closed and temporary DDIRs deleted
```

<br>

- You can use the `IpcsSession` method `create_ddir` to create an empty DDIR.
- You can use the `IpcsSession` method `create_temp_ddir` to create an empty temporary DDIR.
<br>

---
---

## Using the pyIPCS Hex Object

- __[Back to Top](#pyipcs-user-guide)__

---

- The pyIPCS `Hex` allows you to quickly and easily parse out hex values in IPCS output and perform operations against them
<br>

- Some pyIPCS objects will contain `Hex` attributes or parameters. Please refer to the documentation.
<br>

- Accepts strings or integers as input
- Can perform a variety of arithmetic, logical, and bitwise operations such as __+ , - , == , | , & , etc.__
- Supports negative hex values
- Wide variety of other functionality as well

```python
from pyipcs import Hex

x = Hex("A")
y = Hex(10)

z = x + y

if x == y:
    print("Hex values are equal")
else:
    print("Hex values are not equal")

```

<br>

---
---

## Running IPCS Subcommands and Storing Output

- __[Back to Top](#pyipcs-user-guide)__

---

- The `Subcmd` object accepts the `IpcsSession` object as its first parameter
<br>

- You can use the `IpcsSession` method `set_ddir` to edit which DDIR the subcommand will be run under
  - This is reflected in the `IpcsSession` attribute `set_ddir`
- You can use the `IpcsSession` method `set_defaults` to edit the IPCS `DSNAME` default so that subcommands can be run against a specific dump.
<br>

- The `IpcsSession` methods `init_dump` and `set_dump` will set both the DDIR and the default `DSNAME` at the same time to allow for running subcommands under a specific DDIR against a specific dump
<br>

- Subcommand output can be stored within a string or file depending on whether the optional `outfile` parameter is set to `True`
  - `outfile` set to `False` by default

```python

# Output is stored as a string
subcmd_string = Subcmd(session, "STATUS FAILDATA")

# Output is stored in a file
subcmd_file = Subcmd(session, "STATUS FAILDATA", outfile=True)
```

---
---

## Subcmd Indexing, Find, and Get Field Methods

- __[Back to Top](#pyipcs-user-guide)__
- __[Indexing](#indexing)__
- __[Find Methods](#find-methods)__
- __[Get Field Methods](#get-field-methods)__

---

### Indexing

- __[Back to Top](#pyipcs-user-guide)__
- __[Back to Subcmd Indexing, Find, and Get Field Methods](#subcmd-indexing-find-and-get-field-methods)__

---

- To grab portions of subcommand output there is the ability to directly index into the `Subcmd` object.
  - Whether the `Subcmd` object is using string or file output, indexing for subcommand output functions the same
  - Indexing into the `Subcmd` object returns a string

```python

# Runs IPCS subcommand and stores output in a string
subcmd_string = Subcmd(session, "STATUS REGISTERS")

# Runs IPCS subcommand and stores output in a file
subcmd_outfile = Subcmd(session, "STATUS REGISTERS", outfile=True)

# Can directly index into either to grab portions of subcommand output
# x and y are strings
x = subcmd_string[10:20]
y = subcmd_outfile[10:20]

# Will print 'True'
print(x == y)

```

<br>

- The `Subcmd` object also supports the `len` function to determine the length of the subcommand output

```python

len(subcmd_string)
len(subcmd_outfile)
```

---

### Find Methods

- __[Back to Top](#pyipcs-user-guide)__
- __[Back to Subcmd Indexing, Find, and Get Field Methods](#subcmd-indexing-find-and-get-field-methods)__

---

- The `Subcmd` object supports `find` and `rfind` methods
    Whether the `Subcmd` object is using string or file output, the find methods for subcommand output functions are the same
<br>

#### Output for Example IPCS Subcommand `MY SUBCMD`

```markdown
MY OUTPUT
```

#### Using Find Methods for Example IPCS Subcommand `MY SUBCMD`

```python

# Create Subcmd object for subcommand 'YOUR SUBCMD'
subcmd = Subcmd(session, "MY SUBCMD")

# Use the find method of the Subcmd object
x = subcmd.find("UT")

# Will print 4
print(x)

# Use the rfind method of the Subcmd object
y = subcmd.rfind("UT")

# Will print 7
print(y)
```

---

### Get Field Methods

- __[Back to Top](#pyipcs-user-guide)__
- __[Back to Subcmd Indexing, Find, and Get Field Methods](#subcmd-indexing-find-and-get-field-methods)__

---

- The `Subcmd` object supports the various get field methods to parse out important info from subcommand output:
  - `get_field`
  - `get_field2`
  - `rget_field`
  - `rget_field2`
<br>

#### Output for Example IPCS Subcommand `YOUR SUBCMD`

```markdown
HEX FIELD = FFF, STRING: ABCXYZ
```

#### Using the Get Field Methods for Example IPCS Subcommand `YOUR SUBCMD`

```python

# Create Subcmd object for subcommand 'YOUR SUBCMD'
subcmd = Subcmd(session, "YOUR SUBCMD")

# =================
# get_field method
# =================

# Get the field 'HEX FIELD' using get_field method
# ',' marks the end of the field
# ' = ' separates the field name from the value (separator optional parameter)
# Convert to hex value by setting to_hex optional parameter to 'True' (default is False)
x = subcmd.get_field("HEX FIELD", ",", separator=" = ", to_hex=True) 

# Will print the hex value 'FFF'
# x is of type pyipcs.Hex
print(x[0])

# =================
# get_field2 method
# =================

# Get the field 'STRING' using get_field2 method
# The field has a length of 6
# ': ' separates the field name from the value (separator optional parameter)
# DO NOT convert to hex value by having to_hex optional parameter to 'False' (default is False)
y = subcmd.get_field2("STRING", 6, separator=": ") 

# Will print the string value 'ABCXYZ'
# y is of type str
print(y[0]) 
```

---
---

## Retrieving Raw Dump Data

- __[Back to Top](#pyipcs-user-guide)__

---

- The `IpcsSession` method `evaluate` reads raw data from dump. Functions similar to the `EVALUATE` subcommand in REXX.
- __[Evaluate Subcommand](https://www.ibm.com/docs/en/zos/3.1.0?topic=instruction-evaluate-subcommand)__
<br>

- `evaluate` method returns a `Hex` object
- Make sure to set correct defaults `DSNAME`, `ASID`, and `DSPNAME` prior to calling this method.
<br>

### Dump Data At ASID `X'12'` At Address `X'01234567'`

```markdown
89ABCDEF
```

### Using the `evaluate` method to retrieve data

```python

session = IpcsSession()
session.open()

# Dump dataset name
dsname = ...

# Use init_dump to set DSNAME default
dump = session.init_dump(dsname)

# Use set_defaults to set ASID of X'12'
session.set_defaults(asid=Hex("12"))

# X'01234567' is the hex address
# 0 is the byte offset in decimal
# 2 is the byte length to grab in decimal
x = session.evaluate("01234567", 0, 2)

# Will print X'89AB'
# x is of type pyipcs.Hex
print(x)

# X'01234567' is the hex address
# 2 is the byte offset in decimal
# 1 is the byte length to grab in decimal
y = session.evaluate(Hex("01234567"), 2, 1)

# Will print X'CD'
# y is of type pyipcs.Hex
print(y)
```
