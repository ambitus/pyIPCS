"""
Test suite for zoautil_py related util functions

Tests:
```
    test_is_dump_dumps():
        Test is_dump util function with datasets that are z/OS dumps

    test_is_dump_not_dumps():
        Test is_dump util function with datasets that are not dumps
```
"""

# pylint: disable=duplicate-code
import warnings
import pytest
from zoautil_py import datasets, exceptions
from pyipcs.util import is_dump
from ..conftest import TEST_HLQ, NO_TEST_DUMPS


@pytest.fixture
def zos_dataset():
    """
    Fixture for Test z/OS Dataset
    """
    test_dataset_name = f"{TEST_HLQ}.TESTDATA"
    try:
        datasets.write(test_dataset_name, "PYIPCS TEST DATASET")
    except exceptions.DatasetWriteException as e:
        raise RuntimeError(
            "Dataset Write Error - Test Suite pyIPCS Dataset\n"
            + f"\nReturn Code: {e.response.rc}\n"
            + f"\nSTDOUT:\n\n {e.response.stdout_response}\n"
            + f"\nSTDERR:\n\n {e.response.stderr_response}\n"
        ) from e
    yield test_dataset_name
    rc = datasets.delete(test_dataset_name)
    if rc != 0:
        warnings.warn("Test Suite pyIPCS Dataset Not Deleted", UserWarning)


# pylint: enable=redefined-outer-name


def test_is_dump_dumps(test_dump):
    """
    Util Function:
        is_dump
    Description:
        Test is_dump util function with datasets that are z/OS dumps
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set")
    assert is_dump(test_dump)


# pylint: disable=redefined-outer-name
def test_is_dump_not_dumps(zos_dataset):
    """
    Util Function:
        is_dump
    Description:
        Test is_dump util function with datasets that are not dumps
    """
    assert not is_dump(zos_dataset)

    with pytest.raises(ValueError):
        is_dump("THIS.DOES.NOT.EXIST")


# pylint: enable=redefined-outer-name
