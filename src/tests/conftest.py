# pylint: disable=unspecified-encoding
"""
conftest for pytest
"""

import os
import json
import shutil
import pytest
from zoautil_py import datasets
from pyipcs import IpcsSession

# ===================================
# TEST SETTINGS
# ===================================

# Import Settings
with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json"), "r"
) as json_file:
    TEST_SETTINGS = json.load(json_file)

# Test z/OS dump dsnames to use for tests
# Default is empty list
TEST_DUMPS = TEST_SETTINGS["TEST_DUMPS"]

# Allocations to use for opened IPCS session during tests
# Default: { "IPCSPARM" : ["SYS1.PARMLIB"], "SYSPROC" : ["SYS1.SBLSCLI0"] }
TEST_ALLOCATIONS = TEST_SETTINGS["TEST_ALLOCATIONS"]

# Current z/OS userid
USERID = datasets.get_hlq() if datasets.get_hlq() else os.getenv("USER", "TEMP")

# Will pass this as the IpcsSession attribute hlq for tests
# Default is [userid].PYTEST
# If a high level qualifier is set in settings.json, then the tests will use that temp location
if not TEST_SETTINGS["TEST_HLQ"]:
    TEST_HLQ = f"{USERID}.PYTEST"
else:
    TEST_HLQ = TEST_SETTINGS["TEST_HLQ"]

TEST_DIRECTORY = TEST_SETTINGS["TEST_DIRECTORY"]

# Variable to mark whether there are test dumps
NO_TEST_DUMPS = not TEST_DUMPS

# ===================================
# TEST FIXTURES
# ===================================


def pytest_generate_tests(metafunc):
    """
    Generates parameterized test for each z/OS dump
    """
    if "test_dump" in metafunc.fixturenames:
        metafunc.parametrize("test_dump", TEST_DUMPS)


@pytest.fixture
def single_test_dump():
    """
    Fixture for single dump dsname
    """
    if NO_TEST_DUMPS:
        return None
    return TEST_DUMPS[0]


@pytest.fixture
def all_test_dumps():
    """
    Fixture for all dump dsnames
    """
    return TEST_DUMPS


@pytest.fixture
def opened_session():
    """
    Fixture for opened session with no params
    """
    session = IpcsSession(allocations=TEST_ALLOCATIONS)
    try:
        session.open()
        yield session
    finally:
        if session.active:
            session.close()
        session_dir = os.path.join(session.directory, "pyipcs_session")
        if os.path.exists(session_dir) and os.path.isdir(session_dir):
            shutil.rmtree(session_dir)


@pytest.fixture
def opened_session_hlq():
    """
    Fixture for opened session with param hlq
    """
    session = IpcsSession(allocations=TEST_ALLOCATIONS, hlq=TEST_HLQ)
    try:
        session.open()
        yield session
    finally:
        if session.active:
            session.close()
        session_dir = os.path.join(session.directory, "pyipcs_session")
        if os.path.exists(session_dir) and os.path.isdir(session_dir):
            shutil.rmtree(session_dir)


@pytest.fixture
def opened_session_directory(request):
    """
    Fixture for opened session with param directory

    Places under current working directory of the test function
    """
    test_directory = os.path.join(os.path.dirname(request.path), TEST_DIRECTORY)
    test_dir_exists = os.path.exists(test_directory) and os.path.isdir(test_directory)
    session = IpcsSession(
        allocations=TEST_ALLOCATIONS,
        directory=test_directory,
    )
    try:
        session.open()
        yield session
    finally:
        if session.active:
            session.close()
        session_dir = os.path.join(session.directory, "pyipcs_session")
        if not test_dir_exists:
            if os.path.exists(test_directory) and os.path.isdir(test_directory):
                shutil.rmtree(test_directory)
        else:
            if os.path.exists(session_dir) and os.path.isdir(session_dir):
                shutil.rmtree(session_dir)
