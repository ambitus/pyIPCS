"""
Basic Example

Description
-----------
Run basic pyIPCS functionality with a z/OS dump. 

Usage
-----
basic.py <dump_dsname>

Example
-------
basic.py YOUR.DUMP.DSNAME

"""

import sys
from pyipcs import IpcsSession, Subcmd

def main():
    """
    Main entry point of the script.
    """

    if len(sys.argv) != 2:
        print("Usage: python basic.py <dump_dsname>")
        sys.exit("Error: Exactly one argument must be provided.")

    # Dump Dataset Name

    dsname = sys.argv[1]

    # Create IpcsSession object
    # Manages settings for your IPCS session

    session = IpcsSession()

    # Open IPCS Session

    session.open()

    # Create Dump object `dump`
    # Initializes z/OS dump and stores general info

    print("BEGIN DUMP INITIALIZATION")

    dump = session.init_dump(dsname)

    print("END DUMP INITIALIZATION")

    # Print the dump title
    # "SAD", "SVCD", "TDMP", "SYSM", or "SLIP"

    if "dump_type" in dump.header:
        dump_type = dump.header["dump_type"]
    else:
        dump_type = "Dump Type Not Found"

    # Run IPCS subcommand against z/OS dump `dump` and store output

    subcmd = Subcmd(session, "STATUS REGISTERS")

    # Get portion of IPCS subcommand output

    first_20_chars = subcmd[:20]

    # Entire Subcommand Output

    full_output = subcmd.output

    # Print Results
    print()
    print(f"z/OS Dump Dataset: '{dsname}'")
    print()
    print(f"Dump Type: {dump_type}")
    print()
    print(f"First 20 Characters: {repr(first_20_chars)}")
    print()
    print("--- START FULL OUTPUT ---")
    print(full_output)
    print("--- END FULL OUTPUT --- ")

    # Close IPCS Session

    session.close()

if __name__ == "__main__":
    main()
