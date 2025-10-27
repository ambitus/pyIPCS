"""
Custom Subcommand Object Example

Description
-----------
Create a Custom Subcommand Object for `STATUS REGISTERS` and store PSW in `data`. 

Usage
-----
custom_subcmd.py <dump_dsname>

Example
-------
custom_subcmd.py YOUR.DUMP.DSNAME

"""

import sys
from pyipcs import IpcsSession, Subcmd

class StatusRegisters(Subcmd):
    """
    `STATUS REGISTERS` Custom Subcommand Object. Store PSW.
    """
    def __init__(self, session:IpcsSession) -> None:

        # Call constructor from original Subcmd object

        super().__init__(session, "STATUS REGISTERS")

        # Label that indicates start of PSW value

        psw_label = "PSW="

        # End string that indicates end of PSW value

        psw_end = "\n"

        self.data["psw"], _, _ = self.get_field(psw_label, psw_end, to_hex=True)

def main():
    """
    Main entry point of the script.
    """

    if len(sys.argv) != 2:
        print("Usage: python custom_subcmd.py <dump_dsname>")
        sys.exit("Error: Exactly one argument must be provided.")

    # Dump Dataset Name

    dsname = sys.argv[1]

    # Create IpcsSession object

    session = IpcsSession()

    # Open IPCS Session

    session.open()

    # Initialize Dump and Set as Current Dump for Session

    print("BEGIN DUMP INITIALIZATION")

    session.init_dump(dsname)

    print("END DUMP INITIALIZATION")

    # Run IPCS Subcommand using Custom Subcommand Object

    subcmd = StatusRegisters(session)

    # Print Results
    print()
    print(f"z/OS Dump Dataset: '{dsname}'")
    print()
    print(f"PSW from 'STATUS REGISTERS': X'{subcmd.data["psw"]}'")

    # Close IPCS session

    session.close()

if __name__ == "__main__":
    main()
