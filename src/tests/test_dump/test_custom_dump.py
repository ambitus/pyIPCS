"""
Test suite for custom Dump object

Tests:
```
    test_custom_dump():
        Test custom Dump Object
```
"""

import pytest
from pyipcs import IpcsSession, Dump
from ..conftest import NO_TEST_DUMPS

if NO_TEST_DUMPS:
    pytest.skip("No test z/OS dumps set", allow_module_level=True)


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


def test_custom_dump(opened_session, single_test_dump):
    """
    Object:
        Dump
    Description:
        Test custom Dump Object
    """
    my_dump_object = MyDumpObject(opened_session, single_test_dump)
    assert my_dump_object.data["new_dump_data_key"] == "new_dump_data_value"
