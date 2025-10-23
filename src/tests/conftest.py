"""
Settings for all pyIPCS tests
"""

import os
import json
import shutil
import copy
import pytest
from zoautil_py import datasets
from pyipcs import IpcsSession

# ======================================
# Import Settings from settings.json
# ======================================

# pylint: disable=unspecified-encoding
TEST_SETTINGS = {}

if os.path.exists(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")
):

    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json"), "r"
    ) as settings_file:
        TEST_SETTINGS = json.load(settings_file)

for pyipcs_test_setting in ["TEST_HLQ", "TEST_DIRECTORY", "TEST_ALLOCATIONS", "TEST_DUMPS"]:
    if pyipcs_test_setting not in TEST_SETTINGS:
        TEST_SETTINGS[pyipcs_test_setting] = None

# pylint: enable=unspecified-encoding

# ===================================
# TEST VARIABLES
# ===================================

# Current z/OS User ID

USERID = datasets.get_hlq() if datasets.get_hlq() else os.getenv("USER", "TEMP")

# Alternate Test High Level Qualifier
# IpcsSession attribute hlq
# Uses TEST_HLQ from settings.json if specified. Default is [userid].PYTEST

if not TEST_SETTINGS["TEST_HLQ"]:
    TEST_HLQ = f"{USERID}.PYTEST"
else:
    TEST_HLQ = TEST_SETTINGS["TEST_HLQ"]

# Test directory for subcommand output files
# Uses current test directory
if not TEST_SETTINGS["TEST_DIRECTORY"]:
    TEST_DIRECTORY = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "conftest_pyipcs_directory"
    )
else:
    TEST_DIRECTORY = TEST_SETTINGS["TEST_DIRECTORY"]

# Test Allocations
# Uses TEST_ALLOCATIONS from settings.json if specified.
# Default is default IpcSession allocations

if not TEST_SETTINGS["TEST_ALLOCATIONS"]:
    TEST_ALLOCATIONS = {"IPCSPARM": ["SYS1.PARMLIB"], "SYSPROC": ["SYS1.SBLSCLI0"]}
else:
    TEST_ALLOCATIONS = TEST_SETTINGS["TEST_ALLOCATIONS"]

# Test z/OS dump dataset names to use for tests
# Could be None or empty list

TEST_DUMPS = TEST_SETTINGS["TEST_DUMPS"]

# ===================================
# TEST FIXTURES/PARAMETERIZATION
# ===================================


@pytest.fixture
def userid():
    """
    Corresponds to USERID
    """
    return copy.deepcopy(USERID)


@pytest.fixture
def test_hlq():
    """
    Corresponds to TEST_HLQ
    """
    return copy.deepcopy(TEST_HLQ)


@pytest.fixture
def test_allocations():
    """
    Corresponds to TEST_ALLOCATIONS
    """
    return copy.deepcopy(TEST_ALLOCATIONS)


@pytest.fixture
def test_directory():
    """
    Corresponds to TEST_DIRECTORY
    """
    return copy.deepcopy(TEST_DIRECTORY)


# ================================
# Dump Fixtures/Parameterization
# ================================


def pytest_generate_tests(metafunc):
    """
    Generates parameterized test for each test dump
    """
    if "test_dump" in metafunc.fixturenames:
        if TEST_DUMPS:
            metafunc.parametrize("test_dump", TEST_DUMPS)
        else:
            metafunc.parametrize(
                "test_dump",
                [pytest.param(None, marks=pytest.mark.skip("No Test z/OS Dumps Specified"))],
            )


@pytest.fixture
def test_dump_single():
    """
    Corresponds to TEST_DUMPS[0]
    """
    if not TEST_DUMPS:
        pytest.skip("No Test z/OS Dumps Specified")
    return copy.deepcopy(TEST_DUMPS[0])


@pytest.fixture
def test_dump_list():
    """
    Corresponds to TEST_DUMPS
    """
    if not TEST_DUMPS:
        pytest.skip("No Test z/OS Dumps Specified 3")
    return copy.deepcopy(TEST_DUMPS)


# ==================================
# Session Fixtures/Parameterization
# ==================================


@pytest.fixture
def test_session(request):
    """
    Fixture to parameterize across all sessions
    """
    valid_sessions = [
        "open_session_default",
        "open_session_hlq",
        "open_session_directory",
    ]
    if request.param not in valid_sessions:
        raise ValueError(f"Invalid Test Session: '{request.param}'")
    return request.getfixturevalue(request.param)


@pytest.fixture
def open_session_default():
    """
    Fixture for open session with no params
    """
    session = IpcsSession(allocations=TEST_ALLOCATIONS)
    try:
        session.open()
        yield session
    finally:
        if session.active:
            session.close()
        session_dir = os.path.join(session.directory, "pyipcs_directory")
        if os.path.exists(session_dir) and os.path.isdir(session_dir):
            shutil.rmtree(session_dir)


@pytest.fixture
def open_session_hlq():
    """
    Fixture for open session with param hlq
    """
    session = IpcsSession(allocations=TEST_ALLOCATIONS, hlq=TEST_HLQ)
    try:
        session.open()
        yield session
    finally:
        if session.active:
            session.close()
        session_dir = os.path.join(session.directory, "pyipcs_directory")
        if os.path.exists(session_dir) and os.path.isdir(session_dir):
            shutil.rmtree(session_dir)


@pytest.fixture
def open_session_directory():
    """
    Fixture for opened session with param directory

    Places under current working directory of the test function
    """
    session = IpcsSession(
        allocations=TEST_ALLOCATIONS,
        directory=TEST_DIRECTORY,
    )
    try:
        session.open()
        yield session
    finally:
        if session.active:
            session.close()
        if os.path.exists(TEST_DIRECTORY):
            shutil.rmtree(TEST_DIRECTORY)
