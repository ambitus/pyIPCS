"""
Test IPCS utility functions
"""

import pytest
from zoautil_py import datasets

from pyipcs._util import check_dataset_exists
from pyipcs.ipcs import find_field, rfind_field, is_dump


def test_is_dump_nonexistent(hlq):
    """A data set that does not exist is not a dump."""
    dsname = f"{hlq}.MISSING.DSN"
    assert not check_dataset_exists(dsname)
    assert is_dump(dsname) is False


def test_is_dump_non_dump_dataset(temp_dsname):
    """A regular data set (wrong record length) is not a dump."""
    datasets.create(temp_dsname, dataset_type="SEQ")
    datasets.write(temp_dsname, content="NOT A DUMP")
    assert is_dump(temp_dsname) is False


def test_is_dump_wrong_header(temp_dsname):
    """A data set with dump attributes whose first record is not 'DR2' is not a dump."""
    datasets.create(
        temp_dsname,
        dataset_type="SEQ",
        record_format="FB",
        record_length=4160,
        block_size=4160,
    )
    datasets.write(temp_dsname, content="XXX")
    assert is_dump(temp_dsname) is False


@pytest.mark.dump
def test_is_dump_dump(dump_dsname):
    """The provided test dump is a dump."""
    assert is_dump(dump_dsname) is True


# Indexes: "key=" at 0 and 16, "def=" at 8, "end" at 24, length 27
TEXT = "key=ABC def=XYZ key=123 end"


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        # Default end is the next space
        ({"start_str": "key="}, (4, 7)),
        ({"start_str": "def="}, (12, 15)),
        # length
        ({"start_str": "def=", "length": 2}, (12, 14)),
        ({"start_str": "key=", "length": 3}, (4, 7)),
        ({"start_str": "def=", "length": 0}, (12, 12)),
        # end_str
        ({"start_str": "def=", "end_str": " key"}, (12, 15)),
        ({"start_str": "def=", "end_str": "!"}, (12, -1)),
        # start_str not found
        ({"start_str": "nope"}, (-1, -1)),
        ({"start_str": "nope", "length": 2}, (-1, -1)),
        # No space after start_str, length past the end of text
        ({"start_str": "end"}, (27, -1)),
        ({"start_str": "end", "length": 1}, (27, -1)),
        # start / end search bounds
        ({"start_str": "key=", "start": 5}, (20, 23)),
        ({"start_str": "key=", "start": 17}, (-1, -1)),
        ({"start_str": "key=", "end": 10}, (4, 7)),
        ({"start_str": "key=", "end": 6}, (4, -1)),
        ({"start_str": "key=", "end": 3}, (-1, -1)),
        ({"start_str": "key=", "length": 3, "end": 7}, (4, 7)),
        ({"start_str": "key=", "length": 3, "end": 6}, (4, -1)),
        ({"start_str": "key=", "length": 4, "end": 7}, (4, -1)),
    ],
)
def test_find_field(kwargs, expected):
    """find_field returns the first matching field bounds."""
    assert find_field(TEXT, **kwargs) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        # Default end is the next space
        ({"start_str": "key="}, (20, 23)),
        ({"start_str": "def="}, (12, 15)),
        # length
        ({"start_str": "key=", "length": 2}, (20, 22)),
        ({"start_str": "key=", "length": 4}, (20, 24)),
        ({"start_str": "key=", "length": 8}, (20, -1)),
        # end_str
        ({"start_str": "key=", "end_str": " end"}, (20, 23)),
        ({"start_str": "key=", "end_str": "!"}, (20, -1)),
        # start_str not found
        ({"start_str": "nope"}, (-1, -1)),
        # No space after start_str
        ({"start_str": "end"}, (27, -1)),
        # start / end search bounds
        ({"start_str": "key=", "end": 19}, (4, 7)),
        ({"start_str": "key=", "end": 22}, (20, -1)),
        ({"start_str": "key=", "start": 16}, (20, 23)),
        ({"start_str": "key=", "start": 17}, (-1, -1)),
    ],
)
def test_rfind_field(kwargs, expected):
    """rfind_field returns the last matching field bounds."""
    assert rfind_field(TEXT, **kwargs) == expected


def test_find_field_slices_field():
    """The returned tuple slices out the text in between."""
    begin, end = find_field(TEXT, "key=")
    assert TEXT[begin:end] == "ABC"
    begin, end = rfind_field(TEXT, "key=")
    assert TEXT[begin:end] == "123"
    begin, end = find_field(TEXT, "def=", end_str=" key")
    assert TEXT[begin:end] == "XYZ"


def test_find_field_empty_text():
    """Searching empty text finds nothing."""
    assert find_field("", "a") == (-1, -1)
    assert rfind_field("", "a") == (-1, -1)


@pytest.mark.parametrize("func", [find_field, rfind_field])
def test_find_field_length_and_end_str(func):
    """Providing both length and end_str raises ValueError."""
    with pytest.raises(ValueError):
        func(TEXT, "key=", length=2, end_str=" ")
