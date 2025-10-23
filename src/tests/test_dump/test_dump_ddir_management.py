"""
Test suite for dump usage and dump related DDIR usage

Test
----
test_init_dump
    Test IpcsSession.init_dump

test_set_dump
    Test IpcsSession.set_dump

"""
# pylint: disable=redefined-outer-name
import pytest
from pyipcs import IpcsSession, Subcmd
from ..conftest import TEST_ALLOCATIONS, TEST_DUMPS
from ..mock_subcmd_jcl import mock_subcmd_jcl

@pytest.fixture(scope="session")
def mock_status_registers():
    """
    Returns MockSubcmd of STATUS REGISTERS for single test dump
    """

    jcl_session = IpcsSession(allocations=TEST_ALLOCATIONS)
    jcl_session.open()

    jcl_session.init_dump(TEST_DUMPS[0])

    mock_subcmd = mock_subcmd_jcl(
        test_ddir=jcl_session.ddir.dsname,
        test_allocations=TEST_ALLOCATIONS,
        test_subcmds=["STATUS REGISTERS"],
        test_dsname=TEST_DUMPS[0]
    )[0]

    jcl_session.close()

    return mock_subcmd

@pytest.fixture(scope="function")
def test_ddir(test_hlq, test_allocations):
    """
    Test DDIR
    """
    test_ddir_ret = test_hlq + ".TEST.DDIR"
    test_ddir_session = IpcsSession(allocations=test_allocations)
    test_ddir_session.ddir.create(test_ddir_ret, use=False)
    yield test_ddir_ret
    test_ddir_session.ddir._delete(test_ddir_ret)


def test_init_dump(open_session_default, test_dump_single, test_ddir, mock_status_registers):
    """
    Test IpcsSession.init_dump
    """

    # ======================
    # Test standard call
    # ======================

    open_session_default.init_dump(test_dump_single)

    assert Subcmd(open_session_default, "STATUS REGISTERS").output == mock_status_registers.output

    assert open_session_default.ddir.defaults().data["dsname"] == test_dump_single

    open_session_default.close()

    # ======================
    # Test ddir param
    # ======================

    open_session_default.open()

    open_session_default.init_dump(test_dump_single, ddir=test_ddir)

    assert open_session_default.ddir.dsname == test_ddir

    assert open_session_default.ddir.defaults().data["dsname"] == test_dump_single

    assert Subcmd(open_session_default, "STATUS REGISTERS").output == mock_status_registers.output

    open_session_default.close()

    # ==========================
    # Test use_cur_ddir param
    # ==========================

    open_session_default.open()

    init_ddir = open_session_default.ddir.dsname

    open_session_default.init_dump(test_dump_single, use_cur_ddir=True)

    assert open_session_default.ddir.dsname == init_ddir

    assert open_session_default.ddir.defaults().data["dsname"] == test_dump_single

    assert Subcmd(open_session_default, "STATUS REGISTERS").output == mock_status_registers.output

    open_session_default.close()


def test_set_dump(open_session_default, test_dump_single, test_ddir, mock_status_registers):
    """
    Test IpcsSession.set_dump
    """

    dump = open_session_default.init_dump(test_dump_single, ddir=test_ddir)

    assert Subcmd(open_session_default, "STATUS REGISTERS").output == mock_status_registers.output

    open_session_default.close()
    open_session_default.open()

    open_session_default.set_dump(dump)

    assert open_session_default.ddir.dsname == test_ddir

    assert open_session_default.ddir.defaults().data["dsname"] == test_dump_single

    assert Subcmd(open_session_default, "STATUS REGISTERS").output == mock_status_registers.output
