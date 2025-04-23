"""
Custom pyIPCS Exceptions and Warnings
"""

import warnings


class InvalidReturnCodeError(Exception):
    """
    Custom exception for invalid return code from an IPCS subcommand
    """

    def __init__(
        self, subcmd: str, output: str, rc: int, expected_rc: int, dsname: str = ""
    ):
        """
        Constructor for invalid return code exception

        If error code is as expected execution will continue
            but warning will be issued

        Args:
            subcmd (str): IPCS subcommand
            output (str): IPCS subcommand output
            rc (int): actual return code
            expected_rc (int): expected return code
            dsname (str): Optional. Dump dataset that IPCS subcommand was run against
        Returns:
            None
        """
        print(subcmd)
        if rc == expected_rc:
            warnings.warn(
                "pyIPCS Internal Code Error -"
                + "Called InvalidReturnCodeError when error code was expected\n"
                + f"IPCS Subcommand: {subcmd}\n"
                + f"Dataset Name: {dsname if dsname else 'None'}\n"
                + f"Return Code: {rc}\n"
                + f"Expected Return Code: {expected_rc}\n"
                + f"IPCS Subcommand Output:\n {output}"
            )
        else:
            super().__init__(
                "IPCS Subcommand Exited with Unexpected Return Code\n"
                + f"IPCS Subcommand: {subcmd}\n"
                + f"Dataset Name: {dsname if dsname else 'None'}\n"
                + f"Return Code: {rc}\n"
                + f"Expected Return Code: {expected_rc}\n"
                + f"IPCS Subcommand Output:\n {output}"
            )


class SessionNotActiveError(Exception):
    """
    Custom exception for IpcsSession not being active
    """

    def __init__(self):
        """
        Constructor for IpcsSession not being active exception

        Returns:
            None
        """
        super().__init__(
            "Function or method cannot be executed when IPCS Session is not active -"
            + " use pyipcs.IpcsSession.open()"
        )
