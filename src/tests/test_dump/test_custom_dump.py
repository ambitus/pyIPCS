"""
Test suite for custom Dump object

Tests
-----
test_custom_dump
    Test custom Dump Object
"""

from pyipcs import IpcsSession, Dump


class MyDumpObject(Dump):
    """
    Custom Test Dump Object
    """

    # Set up constructor for new Dump object
    def __init__(self, session: IpcsSession, dsname: str, ddir: str = "") -> None:

        # Call constructor from original Dump object
        super().__init__(session, dsname, ddir)

        # Store additional info in data dict attribute
        self.data["new_dump_data_key"] = "new_dump_data_value"


def test_custom_dump(open_session_default, test_dump_single):
    """
    Test custom Dump Object
    """
    my_dump_object = MyDumpObject(open_session_default, test_dump_single)
    assert my_dump_object.data["new_dump_data_key"] == "new_dump_data_value"
