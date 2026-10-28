"""
Test various DDIR operations
"""

import pytest
from zoautil_py import datasets
from pyipcs._util import check_dataset_exists
from pyipcs.exceptions import DdirDeletedError


def test_ddir_delete(ddir_dsname, default_ddir):
    """Test IpcsDdir method delete"""
    assert check_dataset_exists(ddir_dsname)
    response = default_ddir.delete()
    assert response.rc == 0
    assert not check_dataset_exists(ddir_dsname)
    assert default_ddir.is_deleted
    with pytest.raises(DdirDeletedError):
        default_ddir.delete()
    with pytest.raises(DdirDeletedError):
        default_ddir.sources()
    with pytest.raises(DdirDeletedError):
        default_ddir.setdef_global()
    with pytest.raises(DdirDeletedError):
        default_ddir.run("SETDEF LIST")


@pytest.mark.dump
def test_ddir_dump_delete(ddir_dsname, dump, default_ddir, dump_ddir):
    """Test DDIR dump methods display DdirDeletedError"""
    assert check_dataset_exists(ddir_dsname)
    response = default_ddir.delete()
    assert response.rc == 0
    assert not check_dataset_exists(ddir_dsname)
    assert default_ddir.is_deleted
    with pytest.raises(DdirDeletedError):
        default_ddir.init_dump(dump)
    with pytest.raises(DdirDeletedError):
        default_ddir.copy_ddir(dump_ddir, dump)


def test_ddir_allocations(default_ddir):
    """Test IpcsDdir allocations"""
    new_allocations = {"PYTEST": ["PYTEST"]}
    default_ddir.set_allocations(new_allocations)
    assert default_ddir.allocations == new_allocations
    new_allocations["PYTEST2"] = ["PYTEST2"]
    assert default_ddir.allocations != new_allocations


def test_ddir_sources_empty(default_ddir):
    """Test IpcsDdir sources returns an empty list when no dumps are described"""
    assert default_ddir.sources() == []


@pytest.mark.dump
def test_copy_ddir_drop_dump(dump, default_ddir, dump_ddir):
    """Test DDIR source management"""
    assert not default_ddir.sources()
    assert dump.dsname in dump_ddir.sources()
    default_ddir.copy_ddir(dump_ddir, dump)
    assert dump.dsname in default_ddir.sources()
    default_ddir.drop_dump(dump.dsname)
    assert dump.dsname not in default_ddir.sources()


def test_ddir_setdef_global(default_ddir):
    """Test IpcsDdir setdef_global method"""
    response = default_ddir.setdef_global()
    assert response.rc < 8
    assert response.output.find("LENGTH(4)") != -1
    assert response.output.find(" CONFIRM") != -1

    response = default_ddir.setdef_global(defaults="LENGTH(8) NOCONFIRM")
    assert response.rc < 8
    assert response.output.find("LENGTH(8)") != -1
    assert response.output.find("NOCONFIRM") != -1

    response = default_ddir.setdef_global(defaults=["LENGTH(4)", "CONFIRM"])
    assert response.rc < 8
    assert response.output.find("LENGTH(4)") != -1
    assert response.output.find(" CONFIRM") != -1

    response = default_ddir.setdef_global(defaults=("LENGTH(8)", "NOCONFIRM"))
    assert response.rc < 8
    assert response.output.find("LENGTH(8)") != -1
    assert response.output.find("NOCONFIRM") != -1

    response = default_ddir.setdef_global(defaults={"LENGTH(4)", "CONFIRM"})
    assert response.rc < 8
    assert response.output.find("LENGTH(4)") != -1
    assert response.output.find(" CONFIRM") != -1


@pytest.mark.dump
def test_ddir_dump_setdef_global(dump, dump_ddir):
    """Test IpcsDdir setdef_global method dump parameter"""
    response = dump_ddir.setdef_global(defaults="NODSNAME")
    assert response.rc < 8
    assert response.output.find("NODSNAME") != -1

    response = dump_ddir.setdef_global(dump=dump)
    assert response.rc < 8
    assert response.output.find(f"DSNAME('{dump.dsname}')") != -1


def test_ddir_set_tasklib(temp_dsname, default_ddir):
    """set_tasklib stores names and the property returns a copy."""
    datasets.create(temp_dsname, dataset_type="PDS")
    default_ddir.set_tasklib([temp_dsname])
    assert default_ddir.tasklib == [temp_dsname]

    # Mutating the returned copy does not affect the DDIR's state
    copy = default_ddir.tasklib
    copy.append("EXTRA")
    assert default_ddir.tasklib == [temp_dsname]

    response = default_ddir.run("SETDEF LIST")
    assert response.rc < 8
    assert response.output.find("LENGTH(4)") != -1

    # Clear it
    default_ddir.set_tasklib(None)
    assert default_ddir.tasklib is None


def test_ddir_tasklib(temp_dsname, default_ddir):
    """An empty PDS set as tasklib doesn't break IPCS and output is still produced."""
    datasets.create(temp_dsname, dataset_type="PDS")
    default_ddir.set_tasklib([temp_dsname])
    assert default_ddir.tasklib == [temp_dsname]

    response = default_ddir.run("SETDEF LIST")
    assert response.rc < 8
    assert response.output.find("LENGTH(4)") != -1
