"""
pyIPCS IPCS Related Util Functions
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from ..hex_obj import Hex
from ..subcmd import Subcmd
from .hex_util import is_hex

if TYPE_CHECKING:
    from ..session import IpcsSession


# PSW Functions
def psw_scrunch(psw: Hex) -> Hex:
    """
    Scrunch 128 bit PSW to 64 bits.

    If 64 bit PSW is inputted as argument return PSW as is.

    Parameters
    ----------
    psw : pyipcs.Hex
        128 bit PSW or 64 bit PSW.

    Returns
    -------
    pyipcs.Hex
        64 bit PSW
    """
    if not isinstance(psw, Hex):
        raise TypeError(f"psw must be of type pyipcs.Hex, but got {type(psw)}\n")
    if psw.sign() == "-":
        raise ValueError("psw cannot be negative")
    # Return PSW as is or scrunch it
    if psw.bit_len() == 64:
        return psw
    if psw.bit_len() != 128:
        raise ValueError("psw to be scrunched is incorrect length")
    # Turn on Bit 12
    psw = psw.turn_on_bit(12)
    # Get 0 indexed 1st word and 3rd word
    second_half = psw.get_word(1) | psw.get_word(3)

    # Combine 0 indexed 0 word and second half that resulted from the OR
    return psw.get_word(0).concat(second_half)


def psw_parse(psw: Hex) -> Hex:
    """
    Obtain data from PSW.

    Parameters
    ----------
    psw : pyipcs.Hex
        128 bit PSW or 64 bit PSW.

    Returns
    -------
    dict
        data from PSW
        - **"enabled"** (bool|None)
            `True` for Enabled for I/O and External Interrupts if bit 6 and 7 are on.
            `False` for Disabled for I/O and External Interrupts if they are both off.
            `None` if one of either bit 6 or 7 is on and one is off.
        - **"key"** (int)
            PSW key.
        - **"privileged"** (bool):
            `True` for supervisor state(privileged).
            `False` for problem program state(unprivileged).
        - **"asc_mode"** (str)
            One of either `"PRIMARY"`, `"AR"`, `"SECONDARY"`, or `"HOME"`.
        - **"cc"** (int)
            Condition code.
        - **"amode"** (int|None)
            Either `24`, `31`, `64`, or `None` if invalid.
        - **"instr_addr"** (pyipcs.Hex)
            Instruction address.
    """
    if not isinstance(psw, Hex):
        raise TypeError(f"psw must be of type pyipcs.Hex, but got {type(psw)}\n")
    if not psw.bit_len() in [64, 128]:
        raise ValueError("psw is invalid length")
    if psw.sign() == "-":
        raise ValueError("psw cannot be negative")
    if psw.bit_len() == 128:
        psw = psw_scrunch(psw)

    psw_data = {}
    # ENABLEMENT BITS
    if psw.check_bit(6) and psw.check_bit(7):
        psw_data["enabled"] = True
    elif psw.check_bit(6) or psw.check_bit(7):
        psw_data["enabled"] = None
    else:
        psw_data["enabled"] = False
    # Key
    psw_data["key"] = psw.get_nibble(2).to_int()
    # Problem Program Bit
    if psw.check_bit(15):
        psw_data["privileged"] = False
    else:
        psw_data["privileged"] = True
    # Address Space Mode
    bit16 = psw.check_bit(16)
    bit17 = psw.check_bit(17)
    if not bit16 and not bit17:
        psw_data["asc_mode"] = "PRIMARY"
    elif not bit16 and bit17:
        psw_data["asc_mode"] = "AR"
    elif bit16 and not bit17:
        psw_data["asc_mode"] = "SECONDARY"
    else:
        psw_data["asc_mode"] = "HOME"
    # Condition Code
    bit18 = 2 if psw.check_bit(18) else 0
    bit19 = 1 if psw.check_bit(19) else 0
    psw_data["cc"] = bit18 + bit19
    # AMODE
    bit31 = psw.check_bit(31)
    bit32 = psw.check_bit(32)
    if not bit31 and not bit32:
        psw_data["amode"] = 24
    elif not bit31 and bit32:
        psw_data["amode"] = 31
    elif bit31 and bit32:
        psw_data["amode"] = 64
    else:
        psw_data["amode"] = None
    # Instruction Address
    # Get the last word and use bitwise and to remove high order bit from word
    instr_addr = psw.get_word(1)
    instr_addr = instr_addr.turn_off_bit(0)
    psw_data["instr_addr"] = instr_addr
    return psw_data


def opcode(session: IpcsSession, instr: str | int | Hex) -> str | None:
    """
    Get mnemonic of instruction.

    Runs `OPCODE` subcommand.

    Parameters
    ----------
    session : pyipcs.IpcsSession

    instr : str|int|pyipcs.Hex
        Instruction to get mnemonic from.

    Returns
    -------
    str|None
        Instruction mnemonic.
        Returns `None` if `OPCODE` subcommand returns with non-zero
        return code or mnemonic can't be determined.
    """
    if isinstance(instr, (int, str)):
        instr = Hex(instr)

    opcode_subcmd = Subcmd(session, f"OPCODE {instr}")

    if opcode_subcmd.rc != 0:
        return None
    if "IKJ56702I INVALID VARIABLE MNEMONIC OPTION" in opcode_subcmd.output:
        return None

    mnemonic_index = opcode_subcmd.output.find(f"Mnemonic for X'{instr}' is ") + len(
        f"Mnemonic for X'{instr}' is "
    )

    return opcode_subcmd.output[mnemonic_index:].rstrip()


def addr_key(session: IpcsSession, storage_addr: str | int | Hex) -> int | None:
    """
    Get storage key of storage address.

    Runs `LIST` subcommand with the `DISPLAY` parameter.

    Make sure to set correct defaults `DSNAME`, `ASID`, and `DSPNAME`
    prior to calling this function.

    Parameters
    ----------
    session : pyipcs.IpcsSession

    storage_addr : str|int|pyipcs.Hex
        Storage Address.

    Returns
    -------
    int|None
        Storage key.
        Returns `None` if `LIST` subcommand with the `DISPLAY` parameter subcommand
        returns with non-zero return code or key can't be determined.
    """
    if isinstance(storage_addr, (int, str)):
        storage_addr = Hex(storage_addr)

    list_display = Subcmd(session, f"LIST {storage_addr}. DISPLAY")

    if list_display.rc != 0:
        return None
    if not "KEY(" in list_display.output:
        return None

    key = list_display.output[list_display.output.find("KEY(") + len("KEY(")]

    # Check if KEY(..) contains valid hex
    # If not return None
    if not is_hex(key):
        return None

    return int(key, 16)


def addr_fetch_protected(
    session: IpcsSession, storage_addr: str | int | Hex
) -> bool | None:
    """
    Return if storage address is fetch protected.

    Runs `LIST` subcommand with the `DISPLAY` parameter.

    Make sure to set correct defaults `DSNAME`, `ASID`, and `DSPNAME`
    prior to calling this function.

    Parameters
    ----------
    session : pyipcs.IpcsSession

    storage_addr : str|int|pyipcs.Hex
        Storage Address.

    Returns
    -------
    bool 
        `True` if storage_addr is fetch protected, `False` if not.
        Returns `None` if `LIST` subcommand with the `DISPLAY` parameter subcommand
        returns with non-zero return code or fetch protected can't be determined.
    """
    if isinstance(storage_addr, (int, str)):
        storage_addr = Hex(storage_addr)

    list_display = Subcmd(session, f"LIST {storage_addr}. DISPLAY")

    if list_display.rc != 0:
        return None
    if not "KEY(" in list_display.output:
        return None

    fetch = list_display.output[list_display.output.find("KEY(") + len("KEY(") + 1]

    # Check if KEY(..) contains valid hex
    # If not return None
    if not is_hex(fetch):
        return None

    return Hex(fetch).check_bit(0)
