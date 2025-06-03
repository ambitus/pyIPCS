"""
IpcsLogger Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import logging
import os
import sys
import json
import traceback
import warnings

if TYPE_CHECKING:
    from .session import IpcsSession

# ===================
# pyIPCS Log Levels
# ===================

LOG_LEVEL = {
    "DEBUG": logging.DEBUG,
    "SUBCMD": 14,
    "DUMP": 15,
    "SESSION": 16,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
    "NO_LOG": 60,
}

# Add pyIPCS custom log level names
logging.addLevelName(LOG_LEVEL["SUBCMD"], "SUBCMD")
logging.addLevelName(LOG_LEVEL["DUMP"], "DUMP")
logging.addLevelName(LOG_LEVEL["SESSION"], "SESSION")

# ===============================
# pyIPCS Logging JSON Formatter
# ===============================


class JSONFormatter(logging.Formatter):
    """
    Converts records to JSON format
    """

    def format(self, record):
        """
        Supports adding any and all fields and converting it to JSON.
        """
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)
        return json.dumps(log_record)


# ========================
# pyIPCS Logging Filters
# ========================


class LogLevelsFilter(logging.Filter):
    """
    Filter to only allow a set of log levels to be captured
    """

    def __init__(self, allowed_levels: list[int]) -> None:
        """
        Args:
            allowed_levels list[int]: List of allowed log level values to capture
        Returns:
            None
        """
        super().__init__()
        self.allowed_levels = allowed_levels

    def filter(self, record) -> bool:
        """
        If the level number is in `allowed_levels`, then capture

        """
        return record.levelno in self.allowed_levels


class ExcludeLogLevelsFilter(logging.Filter):
    """
    Filter to exclude set of log levels from being captured
    """

    def __init__(self, excluded_levels: list[int]) -> None:
        """
        Args:
            excluded_levels list[int]: List of excluded log level values to not capture
        Returns:
            None
        """
        super().__init__()
        self.excluded_levels = excluded_levels

    def filter(self, record) -> bool:
        """
        If the level number is not in `excluded_levels`, then capture
        """
        return record.levelno not in self.excluded_levels


# ======================
# IpcsLogger Object
# ======================


class IpcsLogger:
    """
    Logging Object for pyIPCS

    Attribute `logger` of the IpcsSession object is of type `pyipcs.IpcsLogger`
    and manages logging for the pyIPCS session.

    Attributes:
        logging_directory (str):
            Directory where log files are placed in.

    Methods
    ```
        get_console_level() -> str:
            Get log level for records outputted to console.

        get_directory_level() -> str:
            Get log level for records outputted to files.

        set_console_level(new_level: str) -> None:
             Set log level for records outputted to console.

        set_directory_level(new_level: str) -> None:
            Set log level for records outputted to files.

        log(level: str, message: str, extra: dict = {}) -> None:
            Log a record with `message` and `level` in JSON.
            By default the record will include the time, `level`, and `message`.
            Can include extra key value pairs for the record using the optional `extra` parameter.
    ```
    """

    def __init__(self):
        """
        Constructor for IpcsLogger object

        Creates Logger objects

        Returns:
            None
        """
        # ==========================================
        # Create Logger Objects and set to NO_LOG
        # ==========================================

        self.__console_logger = logging.getLogger("PyIPCSConsoleLogger")
        self._console_logger.setLevel(LOG_LEVEL["NO_LOG"])

        self.__directory_logger = logging.getLogger("PyIPCSDirectoryLogger")
        self._directory_logger.setLevel(LOG_LEVEL["NO_LOG"])

        # =====================================
        # Set files and directories to `None`
        # =====================================
        self.__logging_directory = None
        self.__instance_json_file = None
        self.__instance_json_content = None

        # ===========================================
        # Save original showwarning and excepthook
        # ===========================================
        self.__original_showwarning = warnings.showwarning
        self.__original_excepthook = sys.excepthook

    def get_console_level(self) -> str:
        """
        Get log level for records outputted to console.

        Returns:
            str : Log level. Will be one of
                `'DEBUG'`, `'SUBCMD'`, `'DUMP'`, `'SESSION'`,
                `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`, or `'NO_LOG'`
        """
        return logging.getLevelName(self._console_logger.level)

    def get_directory_level(self) -> str:
        """
        Get log level for records outputted to files.

        Returns:
            str : Log level. Will be one of
                `'DEBUG'`, `'SUBCMD'`, `'DUMP'`, `'SESSION'`,
                `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`, or `'NO_LOG'`
        """
        return logging.getLevelName(self._directory_logger.level)

    def set_console_level(self, new_level: str) -> None:
        """
        Set log level for records outputted to console.

        Args:
            new_level (str):
                New log level. Should be one of
                `'DEBUG'`, `'SUBCMD'`, `'DUMP'`, `'SESSION'`,
                `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`, or `'NO_LOG'`
        Returns:
            None
        """
        if new_level not in LOG_LEVEL:
            raise ValueError(f"Invalid Log Level '{new_level}'")
        self._console_logger.setLevel(LOG_LEVEL[new_level])

    def set_directory_level(self, new_level: str) -> None:
        """
        Set log level for records outputted to files.

        Args:
            new_level (str):
                New log level. Should be one of
                `'DEBUG'`, `'SUBCMD'`, `'DUMP'`, `'SESSION'`,
                `'INFO'`, `'WARNING'`, `'ERROR'`, , `'CRITICAL'`, or `'NO_LOG'`
        Returns:
            None
        """
        if new_level not in LOG_LEVEL:
            raise ValueError(f"Invalid Log Level '{new_level}'")

        self._directory_logger.setLevel(LOG_LEVEL[new_level])

        # If the log level is:
        #   Higher priority than NO_LOG
        #   The IpcsLogger is open for logging
        #   The instance json does not exist
        # Then create instance json
        if (
            self._directory_logger.level < LOG_LEVEL["NO_LOG"]
            and self._instance_json_file is not None
            and not os.path.exists(self._instance_json_file)
        ):
            os.makedirs(self.logging_directory, exist_ok=True)
            with open(self._instance_json_file, "w", encoding="utf-8") as json_file_obj:
                json.dump(self._instance_json_content, json_file_obj, indent=4)

    def log(self, level: str, message: str, extra: dict = {}) -> None:
        """
        Log a record with `message` and `level` in JSON.

        By default the record will include the time, `level`, and `message`.
        Can include extra key value pairs for the record using the optional `extra` parameter.

        Args:
            level (str):
                Log level. Should be one of
                `'DEBUG'`, `'SUBCMD'`, `'DUMP'`, `'SESSION'`,
                `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`, or `'NO_LOG'`
            message (str)
            extra (dict):
                Optional. Extra key-value pairs to include in record. Should follow JSON format.
        Returns:
            None

        """
        if level not in LOG_LEVEL:
            raise ValueError(f"Invalid Log Level '{level}'")
        level_value = LOG_LEVEL[level]
        self._console_logger.log(level_value, message, extra={"extra_data": extra})
        self._directory_logger.log(level_value, message, extra={"extra_data": extra})

    @property
    def logging_directory(self) -> str | None:
        """
        Attribute logging_directory
        """
        return self.__logging_directory

    @property
    def _console_logger(self) -> logging.Logger:
        """
        Protected Attribute _console_logger

        Logger object for console.
        """
        return self.__console_logger

    @property
    def _directory_logger(self) -> logging.Logger:
        """
        Protected Attribute _directory_logger

        Logger object for files.
        """
        return self.__directory_logger

    @property
    def _instance_json_file(self) -> str | None:
        """
        Protected Attribute _instance_json_file

        Instance file containing config settings for session instance.
        """
        return self.__instance_json_file

    @property
    def _instance_json_content(self) -> dict | None:
        """
        Protected Attribute _instance_json_content

        Content to place in `instance_json_file`
        """
        return self.__instance_json_content

    @property
    def _original_showwarning(self):
        """
        Protected Attribute _original_showwarning

        _original_showwarning == original `warnings.showwarning`
        """
        return self.__original_showwarning

    @property
    def _original_excepthook(self):
        """
        Protected Attribute _original_excepthook

        _original_excepthook == original `sys.excepthook`
        """
        return self.__original_excepthook

    def _custom_showwarning(
        self, message, category, filename, lineno, file=None, line=None
    ):
        """
        Custom showwarning for IpcsLogger
        """

        log_record_data = {
            "warning_type": category.__name__,
            "warning_message": str(message),
            "file": filename,
            "line": lineno,
        }

        # Log warning in JSON format
        self.log("WARNING", "CAUGHT WARNING", extra=log_record_data)

        # If console level is lower priority level then `'WARNING'`:
        # Process warning the same way after
        if self._console_logger.level > LOG_LEVEL["WARNING"]:
            self._original_showwarning(message, category, filename, lineno, file, line)

    def _custom_excepthook(self, exc_type, exc_value, exc_traceback):
        """
        Custom excepthook for IpcsLogger
        """

        # Exclude KeyboardInterrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_traceback)
            return

        # Extract traceback details into list
        extracted_tb = traceback.extract_tb(exc_traceback)

        # Extract multiple steps in the traceback,
        # including function/method name where error occurs
        traceback_steps = [
            {"file": entry.filename, "line": entry.lineno, "function": entry.name}
            for entry in extracted_tb
        ]

        log_record_data = {
            "exception_type": exc_type.__name__,
            "exception_message": str(exc_value),
            "traceback_steps": traceback_steps,
        }

        # Log exception in JSON format
        self.log("ERROR", "UNCAUGHT EXCEPTION", extra=log_record_data)

        # If console level is lower priority level then `'ERROR'`:
        # Process exception the same way after
        if self._console_logger.level > LOG_LEVEL["ERROR"]:
            self._original_excepthook(exc_type, exc_value, exc_traceback)

    def _open_logging(self, session: IpcsSession) -> None:
        """
        Opens logging for the session instance. Adds logging handlers.

        Should only be called in `pyipcs.IpcsSession.open()`.

        Args:
            session (pyipcs.IpcsSession)
        Returns:
            None
        """
        # =======================================
        # Set Directory and Instance JSON File
        # =======================================

        # Logging Directory
        self.__logging_directory = os.path.join(
            session.directory,
            session._session_directory_name,
            session._time_opened,
            "logs",
        )

        # JSON for session instance file
        self.__instance_json_file = os.path.join(
            self.logging_directory, "session_instance.json"
        )

        # JSON for session instance content
        self.__instance_json_content = {
            "script": os.path.abspath(sys.argv[0]),
            "timed_opened": session._time_opened,
            "hlq": session.hlq,
            "directory": session.directory,
        }

        # If the log level is higher priority than NO_LOG create instance json
        if self._directory_logger.level < LOG_LEVEL["NO_LOG"]:
            os.makedirs(self.logging_directory, exist_ok=True)
            with open(self._instance_json_file, "w", encoding="utf-8") as json_file_obj:
                json.dump(self._instance_json_content, json_file_obj, indent=4)

        # ========================================
        # Set Console Logger Handler
        # ========================================

        # Console logging handler
        console_handler = logging.StreamHandler()
        console_handler.addFilter(ExcludeLogLevelsFilter([LOG_LEVEL["NO_LOG"]]))
        console_handler.setFormatter(JSONFormatter())
        self._console_logger.addHandler(console_handler)

        # ===============================
        # Set Directory Logger Handlers
        # ===============================

        # error.log handler
        error_handler = logging.FileHandler(
            os.path.join(self.logging_directory, "error.log"), delay=True
        )
        error_handler.addFilter(
            LogLevelsFilter(
                [LOG_LEVEL["CRITICAL"], LOG_LEVEL["ERROR"], LOG_LEVEL["WARNING"]]
            )
        )
        error_handler.setFormatter(JSONFormatter())
        self._directory_logger.addHandler(error_handler)

        # session.log handler
        session_handler = logging.FileHandler(
            os.path.join(self.logging_directory, "session.log"), delay=True
        )
        session_handler.addFilter(LogLevelsFilter([LOG_LEVEL["SESSION"]]))
        session_handler.setFormatter(JSONFormatter())
        self._directory_logger.addHandler(session_handler)

        # dump.log handler
        dump_handler = logging.FileHandler(
            os.path.join(self.logging_directory, "dump.log"), delay=True
        )
        dump_handler.addFilter(LogLevelsFilter([LOG_LEVEL["DUMP"]]))
        dump_handler.setFormatter(JSONFormatter())
        self._directory_logger.addHandler(dump_handler)

        # subcmd.log handler
        subcmd_handler = logging.FileHandler(
            os.path.join(self.logging_directory, "subcmd.log"), delay=True
        )
        subcmd_handler.addFilter(LogLevelsFilter([LOG_LEVEL["SUBCMD"]]))
        subcmd_handler.setFormatter(JSONFormatter())
        self._directory_logger.addHandler(subcmd_handler)

        # all.log handler
        all_handler = logging.FileHandler(
            os.path.join(self.logging_directory, "all.log"), delay=True
        )
        all_handler.addFilter(ExcludeLogLevelsFilter([LOG_LEVEL["NO_LOG"]]))
        all_handler.setFormatter(JSONFormatter())
        self._directory_logger.addHandler(all_handler)

        # ===================================================
        # Replace excepthook and showwarning and excepthook
        # ===================================================
        warnings.showwarning = self._custom_showwarning
        sys.excepthook = self._custom_excepthook

    def _close_logging(self) -> None:
        """
        Closes logging for the session instance. Clears logging handlers.

        Should only be called in `pyipcs.IpcsSession.close()`.
        """

        # =========================
        # Clear all handlers and reset di
        self.__logging_directory = None
        self.__instance_json_file = None
        self.__instance_json_content = None
        self._console_logger.handlers.clear()
        self._directory_logger.handlers.clear()

        # ===================================================
        # Restore excepthook and showwarning and excepthook
        # ===================================================
        warnings.showwarning = self._original_showwarning
        sys.excepthook = self._original_excepthook
