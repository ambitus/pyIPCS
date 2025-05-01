"""
Subcmd Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import os
import json
import mmap
import re
import warnings
from ..hex_obj import Hex
from ..error_handling import SessionNotActiveError
from .subcmd_shell import run_ipcs_subcmd, run_ipcs_subcmd_outfile

if TYPE_CHECKING:
    from ..session import IpcsSession


class Subcmd:
    """
    Subcmd Object

    Runs IPCS subcommand and stores output in string or file.

    Attributes:
        subcmd (str):
            IPCS subcommand that was ran
        outfile (str|None):
            File containing subcommand output.
            `None` if `outfile` parameter in constructor was set to `False`
            or if file was deleted with `pyipcs.Subcmd.delete_file()` method.
        output (str):
            Returns string containing the entire subcommand output.
        keep_file (bool):
            If `True` preserves subcommand output file after program execution.
            If `False` deletes subcommand output file after program execution.
            Editable by user.
        rc (int):
            Return code from running subcommand.
        data (dict):
            Editable by user to store additional info about a IPCS subcommand. Initially empty.

    Methods:
    ```
        __init__(
            session: pyipcs.IpcsSession,
            subcmd: str,
            outfile: bool = False,
            keep_file: bool = False,
        ) -> None:
            Constructor for Subcmd Object

        find(substring: str, start: int = 0, end: int | None = None) -> int:
            Find the first occurrence of substring.
            Returns -1 if the value is not found.

        rfind(substring: str, start: int = 0, end: int | None = None) -> int:
            Find the last occurrence of substring. Returns -1 if the value is not found.

        get_field(
            label:str,
            end_string:str,
            separator:str="",
            start:int=0,
            end:int|None=None,
            to_hex:bool=False
        ) -> list:
            Attempts to get the field value from the output
            based on a label, separator, and end string.

        get_field2(
            label:str,
            length:int,
            separator:str="",
            start:int=0,
            end:int|None=None,
            to_hex:bool=False
        ) -> list:
            Attempts to get the field value from the output
            based on a label, separator, and field length.

        rget_field(
            label:str,
            end_string:str,
            separator:str="",
            start:int=0,
            end:int|None=None,
            to_hex:bool=False
        ) -> list:
            Attempts to get the field value in a reverse search from the output
            based on a label, separator, and end string.

        rget_field2(
            label:str,
            length:int,
            separator:str="",
            start:int=0,
            end:int|None=None,
            to_hex:bool=False
        ) -> list:
            Attempts to get the field value in a reverse search from the output
            based on a label, separator, and field length.

        delete_file() -> None:
            Function to preemptively delete file associated with subcommand.
            Will not be able to index into file output after completion.
    ```
    """

    def __init__(
        self,
        session: IpcsSession,
        subcmd: str,
        outfile: bool = False,
        keep_file: bool = False,
    ) -> None:
        """
        Constructor for Subcmd Object

        Runs IPCS subcommand and stores output in string or file

        Args:
            session (pyipcs.IpcsSession)
            subcmd (str):
                IPCS subcommand to run.
            outfile (bool):
                Optional. If `True`, will create and store output in directory
                `[pyipcs.IpcsSession.directory]/pyipcs_session/...`
                `...[time of session open]/subcmd_output/`.
                File would then be specified in `outfile` attribute of Subcmd object.
                If `False`, stores output in string
                specified in `output` attribute of Subcmd object. Default is `False`.
            keep_file (bool):
                Optional. If `True` preserves subcommand output file after program execution.
                If `False` deletes subcommand output file after program execution.
                Default is `False`.
        Returns:
            None
        """

        # ============================
        # Check if session is active
        # ============================
        if not session.active:
            raise SessionNotActiveError()

        # ==============================
        #  Type/Value Errors Check
        # ==============================

        if not isinstance(subcmd, str):
            raise TypeError(
                f"Argument 'subcmd' must be of type str, but got {type(subcmd)}"
            )
        if not isinstance(outfile, bool):
            raise TypeError(
                f"Argument 'outfile' must be of type bool, but got {type(outfile)}"
            )
        if not isinstance(keep_file, bool):
            raise TypeError(
                f"Argument 'keep_file' must be of type bool, but got {type(keep_file)}"
            )

        self.__subcmd = subcmd.upper().strip()
        self.__keep_file = keep_file
        self._encoding = "cp1047"

        # ====================
        # Log Running Subcmd
        # ====================

        session.logger.log(
            "SUBCMD",
            "RUNNING SUBCMD",
            extra={
                "subcmd": self.subcmd,
                "outfile": outfile,
                "keep_file": self.keep_file,
                "ddir": session.ddir,
                "allocations": session._allocations,
            },
        )

        # =============================
        # Set Subcommand Data Attribute
        # =============================

        self.data = {}

        # ===============================================
        # Run subcommand for string output or output file
        # ===============================================
        self.__session_directory = None
        self.__session_instance_directory = None
        self.__subcmd_output_directory = None
        self.__outfile = None
        self.__string_output = None

        # If outfile parameter is True create directories and store filename in `outfile` attribute
        if outfile:
            # ==========================
            # Create File Directories
            # ==========================

            # Session Directory
            self.__session_directory = os.path.join(
                session.directory, session._session_directory_name
            )
            # Instance Directory
            self.__session_instance_directory = os.path.join(
                self._session_directory, session._time_opened
            )
            # Subcommand Output Directory
            self.__subcmd_output_directory = os.path.join(
                self._session_instance_directory, "subcmd_output"
            )
            # Original Filepath (May change if this is a copy to filepath + (1)/(2)/etc.)
            self.__outfile = os.path.join(
                self._subcmd_output_directory,
                re.sub(r"[\/\0\?\*\:\ \']", "", self.subcmd.lower()),
            )
            self.__outfile += ".txt"

            # Create the Directories
            os.makedirs(self._subcmd_output_directory, exist_ok=True)

            # ============================================
            # Run the subcommand
            # ============================================
            subcmd_response = run_ipcs_subcmd_outfile(
                session, self.subcmd, self.outfile
            )
            self.__rc = subcmd_response["rc"]
            self.__outfile = subcmd_response["filepath"]

        # If outfile parameter is False store output in string in `output` attribute
        else:
            # ============================================
            # Run the subcommand
            # ============================================
            subcmd_response = run_ipcs_subcmd(session, self.subcmd)
            self.__rc = subcmd_response["rc"]
            self.__string_output = subcmd_response["output"]

        # ============================
        # Log Created Subcmd Object
        # ============================

        session.logger.log(
            "SUBCMD",
            "CREATED SUBCMD OBJECT",
            extra={
                "subcmd": self.subcmd,
                "rc": self.rc,
                "outfile": self.outfile,
                "keep_file": self.keep_file,
                "ddir": session.ddir,
                "allocations": session._allocations,
            },
        )

    def __str__(self) -> str:
        return json.dumps(self._to_json(), indent=4)

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key):
        if self.__string_output is not None:
            return self.__string_output[key]
        if self.outfile is None:
            raise RuntimeError("Attempt to reference deleted subcommand output file")
        with (
            open(self.outfile, "r+b") as bin_obj,
            mmap.mmap(bin_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj,
        ):
            if isinstance(key, slice):
                return mmap_obj[key].decode(self._encoding)
            if key < 0:
                key = len(self) + key
            return mmap_obj[key : key + 1].decode(self._encoding)

    def __len__(self) -> int:
        if self.__string_output is not None:
            return len(self.__string_output)
        if self.outfile is None:
            raise RuntimeError("Attempt to reference deleted subcommand output file")
        with (
            open(self.outfile, "r+b") as bin_obj,
            mmap.mmap(bin_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj,
        ):
            return mmap_obj.size()

    def find(self, substring: str, start: int = 0, end: int | None = None) -> int:
        """
        Find the first occurrence of a substring. Returns `-1` if the value is not found.

        Args:
            substring (str):
                Substring to search for.
            start (int):
                Optional. Index where to start the search. Default is `0`.
            end (int|None):
                Optional. Index where to end the search.
                Default is `None` for the end of the output.
        Returns:
            int: Output index where substring was found. `-1` if substring was not found.
        """
        if not isinstance(substring, str):
            raise TypeError(
                f"Argument 'substring' must be of type str, but got {type(substring)}"
            )
        if not isinstance(start, int):
            raise TypeError(
                f"Argument 'start' must be of type int, but got {type(start)}"
            )
        if not isinstance(end, int) and not isinstance(end, type(None)):
            raise TypeError(
                f"Argument 'end' must be of type int, but got {type(start)}"
            )

        if self.__string_output is not None:
            if end is None:
                return self.__string_output.find(substring, start)
            return self.__string_output.find(substring, start, end)
        if self.outfile is None:
            raise RuntimeError("Attempt to reference deleted subcommand output file")
        with (
            open(self.outfile, "r+b") as bin_obj,
            mmap.mmap(bin_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj,
        ):
            if end is None:
                return mmap_obj.find(substring.encode(self._encoding), start)
            return mmap_obj.find(substring.encode(self._encoding), start, end)

    def rfind(self, substring: str, start: int = 0, end: int | None = None) -> int:
        """
        Find the last occurrence of a substring. Returns `-1` if the value is not found.

        Args:
            substring (str):
                Substring to search for
            start (int):
                Optional. Index where to end the reverse search. Default is `0`.
            end (int|None):
                Optional. Index where to start the reverse search.
                Default is `None` for the end of the output.
        Returns:
            int: Output index where substring was found. `-1` if substring was not found
        """
        if not isinstance(substring, str):
            raise TypeError(
                f"Argument 'substring' must be of type str, but got {type(substring)}"
            )
        if not isinstance(start, int):
            raise TypeError(
                f"Argument 'start' must be of type int, but got {type(start)}"
            )
        if not isinstance(end, int) and not isinstance(end, type(None)):
            raise TypeError(
                f"Argument 'end' must be of type int, but got {type(start)}"
            )

        if self.__string_output is not None:
            if end is None:
                return self.__string_output.rfind(substring, start)
            return self.__string_output.rfind(substring, start, end)
        if self.outfile is None:
            raise RuntimeError("Attempt to reference deleted subcommand output file")
        with (
            open(self.outfile, "r+b") as bin_obj,
            mmap.mmap(bin_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj,
        ):
            if end is None:
                return mmap_obj.rfind(substring.encode(self._encoding), start)
            return mmap_obj.rfind(substring.encode(self._encoding), start, end)

    def get_field(
        self,
        label: str,
        end_string: str,
        separator: str = "",
        start: int = 0,
        end: int | None = None,
        to_hex: bool = False,
    ) -> list:
        """
        Attempts to get the field value from the output based on a label, separator, and end string.

        Args:
            label (str):
                The label of the field.
            end_string (str):
                End string that indicates end of value.
            separator (str):
                Optional. The separator between the label and the value.
            start (int):
                Optional. Index where to start the search. Default is `0`.
            end (int|None):
                Optional. Index where to end the search.
                Default is `None` for the end of the output.
            to_hex (bool):
                Optional. Return value as pyipcs.Hex if `to_hex` is `True`.
                Default is `False` for returning a string.
        Returns:
            list : A list `[value (str|pyipcs.Hex), start (int), end (int)]`
                where `subcmd[start:end] == value`. `[None, -1, -1]` if field is not found.
        """
        if not isinstance(label, str):
            raise TypeError(
                f"Argument 'label' must be of type str, but got {type(label)}"
            )
        if not isinstance(end_string, str):
            raise TypeError(
                f"Argument 'end_string' must be of type str, but got {type(end_string)}"
            )
        if not isinstance(separator, str):
            raise TypeError(
                f"Argument 'separator' must be of type str, but got {type(separator)}"
            )
        if not isinstance(start, int):
            raise TypeError(
                f"Argument 'start' must be of type int, but got {type(start)}"
            )
        if not isinstance(end, int) and not isinstance(end, type(None)):
            raise TypeError(
                f"Argument 'end' must be of type int, but got {type(start)}"
            )
        if not isinstance(to_hex, bool):
            raise TypeError(
                f"Argument 'to_hex' must be of type bool, but got {type(to_hex)}"
            )

        if end is None:
            start_index = self.find(label, start)
        else:
            start_index = self.find(label, start, end)
        if start_index == -1:
            return [None, -1, -1]
        start_index += len(label) + len(separator)

        if end is None:
            end_index = self.find(end_string, start_index)
        else:
            end_index = self.find(end_string, start_index, end)
        if end_index == -1:
            return [None, -1, -1]

        if to_hex:
            return [Hex(self[start_index:end_index].strip()), start_index, end_index]
        return [self[start_index:end_index], start_index, end_index]

    def get_field2(
        self,
        label: str,
        length: int,
        separator: str = "",
        start: int = 0,
        end: int | None = None,
        to_hex: bool = False,
    ) -> list:
        """
        Attempts to get the field value from the output
        based on a label, separator, and field length.

        Args:
            label (str):
                The label of the field.
            length (int):
                Length of value to get.
            separator (str):
                Optional. The separator between the label and the value.
            start (int):
                Optional. Index where to start the search. Default is `0`.
            end (int|None):
                Optional. Index where to end the search.
                Default is `None` for the end of the output.
            to_hex (bool):
                Optional. Return value as pyipcs.Hex if `to_hex` is `True`.
                Default is `False` for returning a string.
        Returns:
            list : A list `[value (str|pyipcs.Hex), start (int), end (int)]`
                where `subcmd[start:end] == value`. `[None, -1, -1]` if field is not found.
        """
        if not isinstance(label, str):
            raise TypeError(
                f"Argument 'label' must be of type str, but got {type(label)}"
            )
        if not isinstance(length, int):
            raise TypeError(
                f"Argument 'length' must be of type int, but got {type(length)}"
            )
        if not isinstance(separator, str):
            raise TypeError(
                f"Argument 'separator' must be of type str, but got {type(separator)}"
            )
        if not isinstance(start, int):
            raise TypeError(
                f"Argument 'start' must be of type int, but got {type(start)}"
            )
        if not isinstance(end, int) and not isinstance(end, type(None)):
            raise TypeError(
                f"Argument 'end' must be of type int, but got {type(start)}"
            )
        if not isinstance(to_hex, bool):
            raise TypeError(
                f"Argument 'to_hex' must be of type bool, but got {type(to_hex)}"
            )

        if end is None:
            start_index = self.find(label, start)
        else:
            start_index = self.find(label, start, end)
        if start_index == -1:
            return [None, -1, -1]
        start_index += len(label) + len(separator)
        end_index = start_index + length

        if to_hex:
            return [Hex(self[start_index:end_index].strip()), start_index, end_index]
        return [self[start_index:end_index], start_index, end_index]

    def rget_field(
        self,
        label: str,
        end_string: str,
        separator: str = "",
        start: int = 0,
        end: int | None = None,
        to_hex: bool = False,
    ) -> list:
        """
        Attempts to get the field value in a reverse search from the output
        based on a label, separator, and end string.

        Args:
            label (str):
                The label of the field.
            end_string (str):
                End string that indicates end of value.
            separator (str):
                Optional. The separator between the label and the value.
            start (int):
                Optional. Index where to end the reverse search. Default is `0`.
            end (int|None):
                Optional. Index where to start the reverse search.
                Default is `None` for the end of the output.
            to_hex (bool):
                Optional. Return value as pyipcs.Hex if `to_hex` is `True`.
                Default is `False` for returning a string.
        Returns:
            list : A list `[value (str|pyipcs.Hex), start (int), end (int)]`
                where `subcmd[start:end] == value`. `[None, -1, -1]` if field is not found.
        """
        if not isinstance(label, str):
            raise TypeError(
                f"Argument 'label' must be of type str, but got {type(label)}"
            )
        if not isinstance(end_string, str):
            raise TypeError(
                f"Argument 'end_string' must be of type str, but got {type(end_string)}"
            )
        if not isinstance(separator, str):
            raise TypeError(
                f"Argument 'separator' must be of type str, but got {type(separator)}"
            )
        if not isinstance(start, int):
            raise TypeError(
                f"Argument 'start' must be of type int, but got {type(start)}"
            )
        if not isinstance(end, int) and not isinstance(end, type(None)):
            raise TypeError(
                f"Argument 'end' must be of type int, but got {type(start)}"
            )
        if not isinstance(to_hex, bool):
            raise TypeError(
                f"Argument 'to_hex' must be of type bool, but got {type(to_hex)}"
            )

        if end is None:
            start_index = self.rfind(label, start)
        else:
            start_index = self.rfind(label, start, end)
        if start_index == -1:
            return [None, -1, -1]
        start_index += len(label) + len(separator)

        if end is None:
            end_index = self.find(end_string, start_index)
        else:
            end_index = self.find(end_string, start_index, end)
        if end_index == -1:
            return [None, -1, -1]

        if to_hex:
            return [Hex(self[start_index:end_index].strip()), start_index, end_index]
        return [self[start_index:end_index], start_index, end_index]

    def rget_field2(
        self,
        label: str,
        length: int,
        separator: str = "",
        start: int = 0,
        end: int | None = None,
        to_hex: bool = False,
    ) -> list:
        """
        Attempts to get the field value in a reverse search from the output
        based on a label, separator, and field length.

        Args:
            label (str):
                The label of the field.
            length (int):
                Length of value to get.
            separator (str):
                Optional. The separator between the label and the value.
            start (int):
                Optional. Index where to end the reverse search. Default is `0`.
            end (int|None):
                Optional. Index where to start the reverse search.
                Default is `None` for the end of the output.
            to_hex (bool).
                Optional. Return value as pyipcs.Hex if `to_hex` is `True`.
                Default is `False` for returning a string.
        Returns:
            list : A list `[value (str|pyipcs.Hex), start (int), end (int)]`
                where `subcmd[start:end] == value`. `[None, -1, -1]` if field is not found.
        """
        if not isinstance(label, str):
            raise TypeError(
                f"Argument 'label' must be of type str, but got {type(label)}"
            )
        if not isinstance(length, int):
            raise TypeError(
                f"Argument 'length' must be of type int, but got {type(length)}"
            )
        if not isinstance(separator, str):
            raise TypeError(
                f"Argument 'separator' must be of type str, but got {type(separator)}"
            )
        if not isinstance(start, int):
            raise TypeError(
                f"Argument 'start' must be of type int, but got {type(start)}"
            )
        if not isinstance(end, int) and not isinstance(end, type(None)):
            raise TypeError(
                f"Argument 'end' must be of type int, but got {type(start)}"
            )
        if not isinstance(to_hex, bool):
            raise TypeError(
                f"Argument 'to_hex' must be of type bool, but got {type(to_hex)}"
            )

        if end is None:
            start_index = self.rfind(label, start)
        else:
            start_index = self.rfind(label, start, end)
        if start_index == -1:
            return [None, -1, -1]
        start_index += len(label) + len(separator)
        end_index = start_index + length

        if to_hex:
            return [Hex(self[start_index:end_index].strip()), start_index, end_index]
        return [self[start_index:end_index], start_index, end_index]

    def delete_file(self) -> None:
        """
        Method to preemptively delete file associated with subcommand.
        Will not be able to index into file output after completion.

        Returns:
            None
        """
        if self.outfile is None:
            warnings.warn(
                "Subcommand output file was either already deleted or never existed"
            )
            return

        # ===========================================================
        # Check if file exists, delete it, and set outfile to None
        # ===========================================================
        if os.path.exists(self.outfile) and os.path.isfile(self.outfile):
            os.remove(self.outfile)
            self.__outfile = None

        # ===============================================
        # Check if directories exist and delete if empty
        # ===============================================
        if (
            os.path.exists(self._subcmd_output_directory)
            and os.path.isdir(self._subcmd_output_directory)
            and not os.listdir(self._subcmd_output_directory)
        ):
            os.rmdir(self._subcmd_output_directory)
            self.__subcmd_output_directory = None

        if (
            os.path.exists(self._session_instance_directory)
            and os.path.isdir(self._session_instance_directory)
            and not os.listdir(self._session_instance_directory)
        ):
            os.rmdir(self._session_instance_directory)
            self.__session_instance_directory = None
        if (
            os.path.exists(self._session_directory)
            and os.path.isdir(self._session_directory)
            and not os.listdir(self._session_directory)
        ):
            os.rmdir(self._session_directory)
            self.__session_directory = None

    @property
    def subcmd(self) -> str:
        """
        Attribute subcmd
        """
        return self.__subcmd

    @property
    def outfile(self) -> str | None:
        """
        Attribute outfile
        """
        return self.__outfile

    @property
    def output(self) -> str | None:
        """
        Attribute output
        """
        return self[:]

    @property
    def keep_file(self) -> bool:
        """
        Attribute keep file
        """
        return self.__keep_file

    @keep_file.setter
    def keep_file(self, value):
        if not isinstance(value, bool):
            raise TypeError(
                f"Attribute 'keep_file' must be of type bool, but got {type(value)}"
            )
        self.__keep_file = value

    @property
    def rc(self) -> int:
        """
        Attribute rc
        """
        return self.__rc

    @property
    def _session_directory(self) -> str | None:
        """
        Protected Attribute _session_directory

        Session directory
        """
        return self.__session_directory

    @property
    def _session_instance_directory(self) -> str | None:
        """
        Protected Attribute _session_instance_directory

        Session instance directory - dependent on when session was opened
        """
        return self.__session_instance_directory

    @property
    def _subcmd_output_directory(self) -> str | None:
        """
        Protected Attribute _subcmd_output_directory

        Directory where subcommand output files are stored
        """
        return self.__subcmd_output_directory

    def _to_json(self) -> dict:
        """
        Converts Subcmd object attributes into dictionary.
        pyipcs.Hex keys and values are replaced with strings.

        Returns:
            dict: Subcmd object dictionary
                where pyipcs.Hex keys and values are replaced with strings
            ```
                'subcmd' (str)
                'outfile' (str|None)
                'output' (str|None)
                'rc' (int)
                'data' (dict)
            ```
        """

        subcommand_json = {
            "subcmd": self.subcmd,
            "outfile": self.outfile,
            "output": self.output,
            "rc": self.rc,
        }

        def data_to_json(data):
            # pylint: disable=duplicate-code
            if isinstance(data, dict):
                return {
                    data_to_json(key): data_to_json(value)
                    for key, value in data.items()
                }
            if isinstance(data, list):
                return [data_to_json(item) for item in data]
            if isinstance(data, (str, int, float, bool, type(None))):
                return data
            if isinstance(data, Hex):
                return data.to_str()
            raise TypeError(
                "data dictionary attribute contains invalid json type "
                + f"- contains type '{type(data)}'"
            )
            # pylint: enable=duplicate-code

        subcommand_json["data"] = data_to_json(self.data)

        return subcommand_json

    def __del__(self):
        if hasattr(self, "outfile") and self.outfile is not None and not self.keep_file:
            self.delete_file()
