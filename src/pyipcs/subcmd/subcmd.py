"""
Subcmd Object
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path
import textwrap
from pprint import pformat
import mmap
import re
import warnings
import copy
from ..hex_obj import Hex
from ..error_handling import SessionNotActiveError
from .subcmd_shell import run_ipcs_subcmd, run_ipcs_subcmd_outfile

if TYPE_CHECKING:
    from ..session import IpcsSession


class Subcmd:
    """
    Subcmd Object

    Runs IPCS subcommand and stores output in string or file.

    Attributes
    ----------
    subcmd : str
        IPCS subcommand that was ran.

    outfile : str|None
        File containing subcommand output.
        `None` if `outfile` parameter in constructor was set to `False`
        or if file was deleted with `pyipcs.Subcmd.delete_file()` method.

    output : str
        Returns string containing the entire subcommand output.

    keep_file : bool
        If `True` preserves subcommand output file after program execution.
        If `False` deletes subcommand output file after program execution.
        Editable by user.

    rc : int
        Return code from running subcommand.
        
    data : dict
        Editable by user to store additional info about a IPCS subcommand. Initially empty.

    Methods
    -------
    __init__(session, subcmd, outfile=False, keep_file=False, auth=False,)
        Constructor for Subcmd Object

    find(substring, start=0, end=None)
        Find the first occurrence of substring.
        Returns -1 if the value is not found.

    rfind(substring, start=0, end=None)
        Find the last occurrence of substring. Returns `-1` if the value is not found.

    get_field(label, end_string, separator="", start=0, end=None, to_hex=False)
        Attempts to get the field value from the output
        based on a label, separator, and end string.

    get_field2(label, length, separator="", start=0, end=None,to_hex=False)
        Attempts to get the field value from the output
        based on a label, separator, and field length.

    rget_field(label, end_string, separator="", start=0, end=None, to_hex=False)
        Attempts to get the field value in a reverse search from the output
        based on a label, separator, and end string.

    rget_field2(label, length, separator="", start=0, end=None, to_hex=False)
        Attempts to get the field value in a reverse search from the output
        based on a label, separator, and field length.

    delete_file()
        Method to preemptively delete file associated with subcommand.
        Will not be able to index into file output after completion.

    """

    def __init__(
        self,
        session: IpcsSession,
        subcmd: str,
        outfile: bool = False,
        keep_file: bool = False,
        auth: bool = False,
    ) -> None:
        """
        Constructor for Subcmd Object

        Runs IPCS subcommand and stores output in string or file

        Parameters
        ----------
        session : pyipcs.IpcsSession

        subcmd : str
            IPCS subcommand to run.
        
        outfile : bool, optional
            If `True`, will create and store output in directory
            `[pyipcs.IpcsSession.directory_full]/subcmd_output/`.
            File would then be specified in `outfile` attribute of Subcmd object.
            If `False`, stores output in string
            specified in `output` attribute of Subcmd object. Default is `False`.
        
        keep_file : bool, optional
            If `True` preserves subcommand output file after program execution.
            If `False` deletes subcommand output file after program execution.
            Default is `False`.

        auth : bool, optional
            If `True`, subcommand will be run from an authorized environment. 
            Default is `False`.
        
        Returns
        -------
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

        # ============================================
        # Set Init Values for Subcommand Attributes
        # ============================================

        self._subcmd = subcmd.upper().strip()
        self._keep_file = keep_file

        self._encoding = "cp1047"
        self._session_directory = session.directory

        self._outfile = None
        self._string_output = None
        self._rc = None

        self.data = {}

        # ===============================================
        # Run subcommand for string output or output file
        # ===============================================

        # If outfile parameter is True create directories and store filename in `outfile` attribute
        if outfile:

            # ==========================
            # Create Filepath
            # ==========================

            filepath = self._create_outfile_path(session.directory_full)

            # ============================================
            # Run the subcommand
            # ============================================

            subcmd_response = run_ipcs_subcmd_outfile(
                session, self.subcmd, filepath, auth
            )
            self._rc = subcmd_response["rc"]
            self._outfile = subcmd_response["filepath"]

        # If outfile parameter is False store output in string in `output` attribute
        else:
            # ============================================
            # Run the subcommand
            # ============================================

            subcmd_response = run_ipcs_subcmd(session, self.subcmd, auth)
            self._rc = subcmd_response["rc"]
            self._string_output = subcmd_response["output"]

    def __pyipcs_json__(self) -> dict:
        """
        Convert Subcmd object for JSON format

        Returns
        -------
        dict: Dictionary representing Subcmd object
            - **"__ipcs_type__"** *(str)*
                `"Subcmd"`
            - **"subcmd"** (str)
            - **"outfile"** (str|None)
            - **"output"** (str)
            - **"keep_file" (bool)
            - **"rc"** (int)
            - **"data"** (dict)
        """
        return {
            "__ipcs_type__": "Subcmd",
            "subcmd": copy.deepcopy(self.subcmd),
            "outfile": copy.deepcopy(self.outfile),
            "output": copy.deepcopy(self.output),
            "keep_file": copy.deepcopy(self.keep_file),
            "rc": copy.deepcopy(self.rc),
            "data": copy.deepcopy(self.data),
        }

    def __str__(self) -> str:
        return (
            f"Subcmd(subcmd:'{self.subcmd}',"
            + " outfile:"
            + (f"{self.outfile}," if self.outfile is None else f"'{self.outfile}',")
            + f" rc:{self.rc})"
        )

    def __repr__(self) -> str:
        repr_output_title = "output"
        repr_output = pformat(self.output[:500])
        if len(self) > 500:
            repr_output_title = "output(First 500 chars)"
            repr_output += " [continued...]"
        return (
            "Subcmd("
            + f"\n  subcmd:\n    \'{self.subcmd}\'"
            + "\n  outfile:"
            + (
                f"\n    {self.outfile}"
                if self.outfile is None
                else f"\n    \'{self.outfile}\'"
            )
            + f"\n  rc:\n    {self.rc}"
            + f"\n  keep_file:\n    {self.keep_file}"
            + f"\n  {repr_output_title}:\n{textwrap.indent(repr_output, '    ')}"
            + f"\n  data:\n{textwrap.indent(pformat(self.data), '    ')}"
            + "\n)"
        )

    def __getitem__(self, key):
        if self._string_output is not None:
            return self._string_output[key]
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
        if self._string_output is not None:
            return len(self._string_output)
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

        Parameters
        ----------
        substring : str
            Substring to search for.

        start : int, optional
            Index where to start the search. Default is `0`.

        end : int|None, optional
            Index where to end the search.
            Default is `None` for the end of the output.

        Returns
        -------
        int
            Output index where substring was found. `-1` if substring was not found.
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

        if self._string_output is not None:
            if end is None:
                return self._string_output.find(substring, start)
            return self._string_output.find(substring, start, end)
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

        Parameters
        ----------
        substring : str
            Substring to search for.

        start : int, optional
            Index where to end the reverse search. Default is `0`.

        end : int|None, optional
            Index where to start the reverse search.
            Default is `None` for the end of the output.

        Returns
        -------
        int
            Output index where substring was found. `-1` if substring was not found.
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

        if self._string_output is not None:
            if end is None:
                return self._string_output.rfind(substring, start)
            return self._string_output.rfind(substring, start, end)
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

        Parameters
        ----------
        label : str
            The label of the field.

        end_string : str
            End string that indicates the end of the value.

        separator : str, optional
            The separator between the label and the value.
        
        start : int, optional
            Index where to start the search. Default is `0`.
        
        end : int|None, optional
            Index where to end the search.
            Default is `None` for the end of the output.
        
        to_hex : bool, optional
            Return value as pyipcs.Hex if `to_hex` is `True`.
            Default is `False` for returning a string.
        
        Returns
        -------
        list
            A list `[value (str|pyipcs.Hex), start (int), end (int)]`
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

        Parameters
        ----------
        label : str
            The label of the field.

        length : int
            Length of the value to get.
        
        separator : str, optional
            The separator between the label and the value.
        
        start : int, optional
            Index where to start the search. Default is `0`.
        
        end : int|None, optional
            Index where to end the search.
            Default is `None` for the end of the output.
        
        to_hex : bool, optional
            Return value as pyipcs.Hex if `to_hex` is `True`.
            Default is `False` for returning a string.
        
        Returns
        -------
        list 
            A list `[value (str|pyipcs.Hex), start (int), end (int)]`
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

        Parameters
        ----------
        label : str
            The label of the field.

        end_string : str
            End string that indicates the end of the value.

        separator : str, optional
            The separator between the label and the value.

        start : int, optional
            Index where to end the reverse search. Default is `0`.

        end : int|None, optional
            Index where to start the reverse search.
            Default is `None` for the end of the output.
        
        to_hex : bool, optional
            Return value as pyipcs.Hex if `to_hex` is `True`.
            Default is `False` for returning a string.
        
        Returns
        -------
        list 
            A list `[value (str|pyipcs.Hex), start (int), end (int)]`
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

        Parameters
        ----------
        label : str
            The label of the field.

        length : int
            Length of the value to get.

        separator : str, optional
            The separator between the label and the value.

        start : int, optional
            Index where to end the reverse search. Default is `0`.

        end : int|None, optional
            Index where to start the reverse search.
            Default is `None` for the end of the output.

        to_hex : bool, optional
            Return value as pyipcs.Hex if `to_hex` is `True`.
            Default is `False` for returning a string.

        Returns
        -------
        list 
            A list `[value (str|pyipcs.Hex), start (int), end (int)]`
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

        Returns
        -------
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

        session_directory_path = Path(self._session_directory)
        outfile_path = Path(self.outfile)

        if outfile_path.exists() and outfile_path.is_file():

            outfile_path = outfile_path.resolve()
            session_directory_path = session_directory_path.resolve()

            outfile_path.unlink()

            # ===============================================
            # Check if directories exist and delete if empty
            # ===============================================

            for parent in outfile_path.parents:
                if (
                    parent == session_directory_path
                    or not str(parent).startswith(str(session_directory_path))
                ):
                    break
                try:
                    # Try to remove if empty
                    # OSError if not empty or no permission
                    parent.rmdir()
                except OSError:
                    # Directory not empty or cannot be removed
                    # Stop cleanup
                    break

        # ======================
        # Set outfile to None
        # ======================

        self._outfile = None

    @property
    def subcmd(self) -> str:
        """
        Attribute subcmd
        """
        return self._subcmd

    @property
    def outfile(self) -> str | None:
        """
        Attribute outfile
        """
        return self._outfile

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
        return self._keep_file

    @keep_file.setter
    def keep_file(self, value):
        if not isinstance(value, bool):
            raise TypeError(
                f"Attribute 'keep_file' must be of type bool, but got {type(value)}"
            )
        self._keep_file = value

    @property
    def rc(self) -> int:
        """
        Attribute rc
        """
        return self._rc

    def _create_outfile_path(self, session_directory_full: str) -> str:
        """
        Create the path for outfile

        Parameters
        ----------
        session_directory_full : str

        Returns
        -------
        str
            String filepath for outfile
        """
        # Open Session Directory

        outfile_path = Path(session_directory_full)

        # Subcommand Output Directory

        outfile_path = outfile_path / "subcmd_output"

        # Original Filepath (May change if this is a copy to filepath + (1)/(2)/etc.)

        outfile_path = outfile_path / re.sub(r"[\/\0\?\*\:\ \']", "", self.subcmd.lower())
        outfile_path = outfile_path.with_suffix(".txt")

        # Add copy designation to filepath (1)/(2)/etc.

        dup_num = 1
        while outfile_path.exists():
            outfile_path = outfile_path.with_stem(f"{outfile_path.stem}({dup_num})")
            dup_num += 1

        return str(outfile_path)

    def __del__(self):
        if hasattr(self, "outfile") and self.outfile is not None and not self.keep_file:
            self.delete_file()
