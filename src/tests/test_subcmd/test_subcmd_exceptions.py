"""
Test suite for Subcmd exceptions

Tests:
```
    test_not_open_funcs():
        Test running functions while session is not open

    test_delete_file_reference():
        Test referencing file output after delete file has been called
```
"""

# pylint: disable=duplicate-code
import pytest
from pyipcs import Subcmd
from ..conftest import NO_TEST_DUMPS

if NO_TEST_DUMPS:
    pytest.skip("No test z/OS dumps set", allow_module_level=True)


def test_not_open_funcs(opened_session, single_test_dump):
    """
    Object:
        Subcmd
    Description:
        Test running functions while session is not open
    """
    opened_session.init_dump(single_test_dump)

    opened_session.close()

    with pytest.raises(Exception):
        Subcmd(opened_session, "SETDEF LIST")
    with pytest.raises(Exception):
        Subcmd(opened_session, "STATUS REGISTERS")


def test_delete_file_reference(opened_session, single_test_dump):
    """
    Object:
        Subcmd
    Description:
        Test referencing file output after delete file has been called
    """
    opened_session.init_dump(single_test_dump)
    subcmd = Subcmd(opened_session, "STATUS REGISTERS", outfile=True)
    subcmd.delete_file()
    # pylint: disable=pointless-statement
    with pytest.raises(Exception):
        subcmd[1]
    with pytest.raises(Exception):
        subcmd[1:5]
    with pytest.raises(Exception):
        subcmd.find("TEST")
    with pytest.raises(Exception):
        subcmd.rfind("TEST")
    with pytest.raises(Exception):
        len(subcmd)
    # pylint: enable=pointless-statement
