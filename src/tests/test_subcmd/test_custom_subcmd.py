"""
Test suite for custom Subcmd object

Tests:
```
    test_custom_subcmd():
        Test custom Subcmd object
```
"""

from pyipcs import IpcsSession, Subcmd


class YourSubcmd(Subcmd):
    """
    Custom Test Subcmd Object
    """

    def __init__(
        self,
        session: IpcsSession,
        outfile: bool = False,
        keep_file: bool = False,
    ) -> None:

        # Call constructor from original Subcmd object
        super().__init__(
            session,
            "OPCODE D203E02C7624",
            outfile=outfile,
            keep_file=keep_file,
        )

        # Store additional info in data dict attribute
        self.data["new_subcmd_data_key"] = "new_submcd_data_value"


def test_custom_subcmd(opened_session):
    """
    Object:
        Subcmd
    Description:
        Test custom Subcmd object
    """
    your_subcmd = YourSubcmd(opened_session)
    assert your_subcmd.data["new_subcmd_data_key"] == "new_submcd_data_value"
