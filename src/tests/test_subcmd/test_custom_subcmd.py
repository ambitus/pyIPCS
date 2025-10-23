"""
Test suite for custom Subcmd object

Tests
-----
test_custom_subcmd
    Test custom Subcmd object

"""

from pyipcs import IpcsSession, Subcmd


class YourSubcmd(Subcmd):
    """
    Custom Test Subcmd Object
    """

    def __init__(
        self,
        session: IpcsSession,
    ) -> None:

        # Call constructor from original Subcmd object

        super().__init__(session, "SETDEF LIST")

        # Store additional info in data dict attribute

        self.data["new_subcmd_data_key"] = "new_subcmd_data_value"


def test_custom_subcmd(open_session_default):
    """
    Test custom Subcmd object
    """
    your_subcmd = YourSubcmd(open_session_default)
    assert your_subcmd.data["new_subcmd_data_key"] == "new_subcmd_data_value"
