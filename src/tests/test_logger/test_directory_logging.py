"""
Test suite for directory logging

Tests:
```
    test_session_default_records():
        Test with `SESSION` log level and default session log records.

    test_dump_default_records():
        Test with `DUMP` log level and default dump log records.

    test_subcmd_default_records():
        Test with `SUBCMD` log level and default subcmd log records.

    test_log_method():
        Test the `log` method     
```
"""

import os
import json
import pytest
from pyipcs import Subcmd
from ..conftest import NO_TEST_DUMPS, TEST_HLQ


def test_session_default_records(opened_session):
    """
    Object:
        IpcsLogger
    Description:
        Test with `SESSION` log level and default session log records.
    """
    try:
        opened_session.logger.set_directory_level("SESSION")

        # CREATE DDIR
        test_ddir = TEST_HLQ + ".TEST.DDIR"
        opened_session.create_ddir(test_ddir)

        # SET ALLOCATION
        opened_session.set_allocation("TESTDD", ["TEST.DATA.SET1", "TEST.DATA.SET2"])

        log_dict = get_all_records(opened_session.logger.logging_directory)

        assert list(log_dict.keys()) == ["session.log", "all.log"]
        assert all(
            all_record["level"] == "SESSION" for all_record in log_dict["all.log"]
        )
        assert all(
            session_record["level"] == "SESSION"
            for session_record in log_dict["session.log"]
        )

        # ====================
        # CREATE DDIR
        # ====================
        test_record_c_d = {
            "level": "SESSION",
            "message": "CREATE DDIR",
            "ddir": test_ddir,
        }
        assert any(
            record_match(all_record, test_record_c_d)
            for all_record in log_dict["all.log"]
        )
        assert any(
            record_match(session_record, test_record_c_d)
            for session_record in log_dict["session.log"]
        )

        # ========================
        # SET ALLOCATION
        # ========================
        test_record_set_a = {
            "level": "SESSION",
            "message": "SET ALLOCATION",
            "dd_name": "TESTDD",
            "specification": ["TEST.DATA.SET1", "TEST.DATA.SET2"],
        }
        assert any(
            record_match(all_record, test_record_set_a)
            for all_record in log_dict["all.log"]
        )
        assert any(
            record_match(session_record, test_record_set_a)
            for session_record in log_dict["session.log"]
        )

    finally:
        if not opened_session.active:
            opened_session.open()
        opened_session.ddir._delete(test_ddir)


def test_dump_default_records(opened_session, single_test_dump):
    """
    Object:
        IpcsLogger
    Description:
        Test with `DUMP` log level and default dump log records.
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set")
    try:
        opened_session.logger.set_directory_level("DUMP")

        test_ddir = TEST_HLQ + ".TEST.DDIR"
        opened_session.create_ddir(test_ddir)
        dump = opened_session.init_dump(single_test_dump, ddir=test_ddir)

        log_dict = get_all_records(opened_session.logger.logging_directory)

        assert list(log_dict.keys()) == ["session.log", "dump.log", "all.log"]
        assert all(
            all_record["level"] in ["SESSION", "DUMP"]
            for all_record in log_dict["all.log"]
        )
        assert all(
            session_record["level"] == "SESSION"
            for session_record in log_dict["session.log"]
        )
        assert all(
            dump_record["level"] == "DUMP" for dump_record in log_dict["dump.log"]
        )

        # =======================
        # START INITIALIZE DUMP
        # =======================
        test_record_s_i_d = {
            "level": "DUMP",
            "message": "START INITIALIZE DUMP",
            "dsname": dump.dsname,
            "ddir": dump.ddir,
        }
        assert any(
            record_match(all_record, test_record_s_i_d)
            for all_record in log_dict["all.log"]
        )
        assert any(
            record_match(dump_record, test_record_s_i_d)
            for dump_record in log_dict["dump.log"]
        )
        # =======================
        # FINISH INITIALIZE DUMP
        # =======================
        test_record_f_i_d = {
            "level": "DUMP",
            "message": "FINISH INITIALIZE DUMP",
            "dsname": dump.dsname,
            "ddir": dump.ddir,
        }
        assert any(
            record_match(all_record, test_record_f_i_d)
            for all_record in log_dict["all.log"]
        )
        assert any(
            record_match(dump_record, test_record_f_i_d)
            for dump_record in log_dict["dump.log"]
        )

        # =============================
        # RUNNING DUMP OBJECT SUBCMDS
        # =============================
        test_record_r_d_o_s = {
            "level": "DUMP",
            "message": "RUNNING DUMP OBJECT SUBCMDS",
            "dsname": dump.dsname,
            "ddir": dump.ddir,
        }
        assert any(
            record_match(all_record, test_record_r_d_o_s)
            for all_record in log_dict["all.log"]
        )
        assert any(
            record_match(dump_record, test_record_r_d_o_s)
            for dump_record in log_dict["dump.log"]
        )
        # =============================
        # CREATED DUMP OBJECT
        # =============================
        test_record_c_d_o = {
            "level": "DUMP",
            "message": "CREATED DUMP OBJECT",
            "dsname": dump.dsname,
            "ddir": dump.ddir,
        }
        assert any(
            record_match(all_record, test_record_c_d_o)
            for all_record in log_dict["all.log"]
        )
        assert any(
            record_match(dump_record, test_record_c_d_o)
            for dump_record in log_dict["dump.log"]
        )

        opened_session.close()
        opened_session.open()

        opened_session.set_dump(dump)

        log_dict = get_all_records(opened_session.logger.logging_directory)

        # ==================
        # SET DUMP
        # ==================
        test_record_s_d = {
            "level": "DUMP",
            "message": "SET DUMP",
            "dsname": dump.dsname,
            "ddir": dump.ddir,
        }
        assert any(
            record_match(all_record, test_record_s_d)
            for all_record in log_dict["all.log"]
        )
        assert any(
            record_match(dump_record, test_record_s_d)
            for dump_record in log_dict["dump.log"]
        )

    finally:
        if not opened_session.active:
            opened_session.open()
        opened_session.ddir._delete(test_ddir)


def test_subcmd_default_records(opened_session, single_test_dump):
    """
    Object:
        IpcsLogger
    Description:
        Test with `SUBCMD` log level and default subcmd log records.
    """
    if NO_TEST_DUMPS:
        pytest.skip("No test z/OS dumps set")

    opened_session.logger.set_directory_level("SUBCMD")

    dump = opened_session.init_dump(single_test_dump)

    subcmd = Subcmd(opened_session, "STATUS REGISTERS")

    log_dict = get_all_records(opened_session.logger.logging_directory)

    assert list(log_dict.keys()) == ["session.log", "dump.log", "subcmd.log", "all.log"]
    assert all(
        all_record["level"] in ["SESSION", "DUMP", "SUBCMD"]
        for all_record in log_dict["all.log"]
    )
    assert all(
        session_record["level"] == "SESSION"
        for session_record in log_dict["session.log"]
    )
    assert all(dump_record["level"] == "DUMP" for dump_record in log_dict["dump.log"])
    assert all(
        dump_record["level"] == "SUBCMD" for dump_record in log_dict["subcmd.log"]
    )

    # =======================
    # RUNNING SUBCMD
    # =======================
    test_record_r_s = {
        "level": "SUBCMD",
        "message": "RUNNING SUBCMD",
        "subcmd": subcmd.subcmd,
        "outfile": False,
        "keep_file": False,
        "ddir": dump.ddir,
        "allocations": opened_session.aloc.get(),
    }
    assert any(
        record_match(all_record, test_record_r_s) for all_record in log_dict["all.log"]
    )
    assert any(
        record_match(subcmd_record, test_record_r_s)
        for subcmd_record in log_dict["subcmd.log"]
    )

    # =======================
    # CREATED SUBCMD OBJECT
    # =======================
    test_record_c_s_o = {
        "level": "SUBCMD",
        "message": "CREATED SUBCMD OBJECT",
        "subcmd": subcmd.subcmd,
        "rc": subcmd.rc,
        "outfile": subcmd.outfile,
        "keep_file": subcmd.keep_file,
        "ddir": dump.ddir,
        "allocations": opened_session.aloc.get(),
    }
    assert any(
        record_match(all_record, test_record_c_s_o)
        for all_record in log_dict["all.log"]
    )
    assert any(
        record_match(subcmd_record, test_record_c_s_o)
        for subcmd_record in log_dict["subcmd.log"]
    )


def test_log_method(opened_session):
    """
    Object:
        IpcsLogger
    Description:
        Test the `log` method
    """
    opened_session.logger.set_directory_level("INFO")

    opened_session.logger.log("INFO", "TEST INFO MESSAGE")
    opened_session.logger.log("DEBUG", "TEST DEBUG MESSAGE")

    log_dict = get_all_records(opened_session.logger.logging_directory)

    assert list(log_dict.keys()) == ["all.log"]
    assert all(all_record["level"] == "INFO" for all_record in log_dict["all.log"])

    # ===============
    # INFO record 1
    # ===============
    test_record_1 = {
        "level": "INFO",
        "message": "TEST INFO MESSAGE",
    }
    assert any(
        record_match(all_record, test_record_1) for all_record in log_dict["all.log"]
    )

    logging_directory = opened_session.logger.logging_directory
    opened_session.close()
    opened_session.logger.log("INFO", "TEST INFO MESSAGE 2")

    log_dict = get_all_records(logging_directory)

    # ===============
    # INFO record 2
    # ===============
    test_record_2 = {
        "level": "INFO",
        "message": "TEST INFO MESSAGE 2",
    }
    assert not any(
        record_match(all_record, test_record_2) for all_record in log_dict["all.log"]
    )


# =====================
# Helper Functions
# =====================
def record_match(record: dict, test_record: dict):
    """
    Check if record matches answer keys and values

    Used to get not check `time`

    Args:
        record (dict): Log record
        test_record (dict): Key value pairs that should be in there to match
    Returns:
        bool: Determine whaether key value pairs in `test_record` are in record
    """
    test_record = json.loads(json.dumps(test_record))
    for key, value in test_record.items():
        if not key in record or not record[key] == value:
            return False
    return True


def get_all_records(logging_directory: str):
    """
    Get all records

    Args:
        logging_directory (str):
            Directory where logs are located
    Returns:
        dict[str, list[dict]]: Dictionary where keys are the log files
            and the values are a list of records
    """

    error_log = os.path.join(logging_directory, "error.log")
    session_log = os.path.join(logging_directory, "session.log")
    dump_log = os.path.join(logging_directory, "dump.log")
    subcmd_log = os.path.join(logging_directory, "subcmd.log")
    all_log = os.path.join(logging_directory, "all.log")

    log_dict = {}

    def add_log_to_dict(log_filepath, log_filename):
        if os.path.exists(log_filepath) and os.path.isfile(log_filepath):
            log_dict[log_filename] = []
            with open(log_filepath, "r", encoding="utf-8") as log_file_obj:
                for record in log_file_obj:
                    log_dict[log_filename].append(json.loads(record.strip()))

    add_log_to_dict(error_log, "error.log")
    add_log_to_dict(session_log, "session.log")
    add_log_to_dict(dump_log, "dump.log")
    add_log_to_dict(subcmd_log, "subcmd.log")
    add_log_to_dict(all_log, "all.log")
    return log_dict
