"""
Test IpcsDdir constructor
"""

from pyipcs import IpcsDdir
from pyipcs.driver import default_driver_dsname, validate_driver
from pyipcs._util import check_dataset_exists, tso_profile_prefix


def test_ddir_init_default(ddir_dsname, allocations, ddir_parms):
    """Test default IpcsDdir constructor"""
    default_driver = default_driver_dsname()
    assert not check_dataset_exists(default_driver)
    assert not check_dataset_exists(ddir_dsname)

    # Create DDIR
    with IpcsDdir(ddir_dsname, allocations=allocations, ddir_parms=ddir_parms) as ddir:
        assert ddir.dsname == ddir_dsname
        assert check_dataset_exists(ddir_dsname)
        assert ddir.driver == default_driver
        validate_driver(default_driver)

    # Check DDIR and driver persist after DDIR creation
    assert check_dataset_exists(ddir_dsname)
    validate_driver(default_driver)

    # Check we can reuse DDIR and driver
    with IpcsDdir(ddir_dsname, allocations=allocations, ddir_parms=ddir_parms) as ddir:
        assert ddir.dsname == ddir_dsname
        assert check_dataset_exists(ddir_dsname)
        assert ddir.driver == default_driver
        validate_driver(default_driver)


def test_ddir_init_existing(default_ddir, allocations, ddir_parms):
    """Test IpcsDdir constructor with an existing DDIR."""
    assert check_dataset_exists(default_ddir.dsname)

    with IpcsDdir(
        default_ddir.dsname, allocations=allocations, ddir_parms=ddir_parms
    ) as ddir:
        assert ddir.dsname == default_ddir.dsname
        assert ddir.response is None


def test_ddir_init_custom_driver(ddir_dsname, driver_dsname, allocations, ddir_parms):
    """Test IpcsDdir constructor with a custom driver."""
    assert not check_dataset_exists(driver_dsname)
    assert not check_dataset_exists(ddir_dsname)

    # Create DDIR
    with IpcsDdir(
        ddir_dsname,
        driver=driver_dsname,
        allocations=allocations,
        ddir_parms=ddir_parms,
    ) as ddir:
        assert ddir.dsname == ddir_dsname
        assert check_dataset_exists(ddir_dsname)
        assert ddir.driver == driver_dsname
        validate_driver(driver_dsname)

    # Check DDIR and driver persist after DDIR creation
    assert check_dataset_exists(ddir_dsname)
    validate_driver(driver_dsname)

    # Check we can reuse DDIR and driver
    with IpcsDdir(
        ddir_dsname,
        driver=driver_dsname,
        allocations=allocations,
        ddir_parms=ddir_parms,
    ) as ddir:
        assert ddir.dsname == ddir_dsname
        assert check_dataset_exists(ddir_dsname)
        assert ddir.driver == driver_dsname
        validate_driver(driver_dsname)


def test_ddir_init_delete(ddir_dsname, allocations, ddir_parms):
    """Test IpcsDdir constructor with delete parameter set to ``True``"""
    default_driver = default_driver_dsname()
    assert not check_dataset_exists(default_driver)
    assert not check_dataset_exists(ddir_dsname)

    # Create DDIR using with
    with IpcsDdir(
        ddir_dsname, allocations=allocations, ddir_parms=ddir_parms, delete=True
    ) as ddir:
        assert ddir.dsname == ddir_dsname
        assert check_dataset_exists(ddir_dsname)

    # Check DDIR is deleted
    assert not check_dataset_exists(ddir_dsname)

    # Create DDIR using regular construction
    ddir = IpcsDdir(
        ddir_dsname, allocations=allocations, ddir_parms=ddir_parms, delete=True
    )
    assert ddir.dsname == ddir_dsname
    assert check_dataset_exists(ddir_dsname)

    # Delete object and check DDIR does not exist
    del ddir
    assert not check_dataset_exists(ddir_dsname)


def test_ddir_temp(hlq, allocations, ddir_parms):
    """Test temp_ddir classmethod alternate IpcsDdir constructor"""

    with IpcsDdir.temp_ddir(allocations=allocations, ddir_parms=ddir_parms) as ddir:
        temp_ddir_dsname = ddir.dsname
        assert temp_ddir_dsname.startswith(tso_profile_prefix())
        assert check_dataset_exists(temp_ddir_dsname)
    assert not check_dataset_exists(temp_ddir_dsname)

    with IpcsDdir.temp_ddir(
        hlq=hlq, allocations=allocations, ddir_parms=ddir_parms
    ) as ddir:
        temp_ddir_dsname = ddir.dsname
        assert temp_ddir_dsname.startswith(hlq)
        assert check_dataset_exists(temp_ddir_dsname)
    assert not check_dataset_exists(temp_ddir_dsname)

    # Test multiple temp DDIRs existing at once
    with IpcsDdir.temp_ddir(allocations=allocations, ddir_parms=ddir_parms) as ddir1:
        with IpcsDdir.temp_ddir(
            allocations=allocations, ddir_parms=ddir_parms
        ) as ddir2:
            temp_ddir_dsname1 = ddir1.dsname
            temp_ddir_dsname2 = ddir2.dsname
            assert temp_ddir_dsname1 != temp_ddir_dsname2
            assert check_dataset_exists(temp_ddir_dsname1)
            assert check_dataset_exists(temp_ddir_dsname2)
    assert not check_dataset_exists(temp_ddir_dsname1)
    assert not check_dataset_exists(temp_ddir_dsname2)
