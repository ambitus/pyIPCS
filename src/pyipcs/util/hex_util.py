"""
pyIPCS Hex Related Util Functions
"""


def is_hex(hex_str: str):
    """
    Check if string is hex

    Parameters
    ----------
    hex_str : str

    Returns
    -------
    bool
        `True` if string is hex, `False` if not.
    """
    if hex_str.startswith("0x") or hex_str.startswith("0X"):
        hex_str = hex_str[2:]
    return all(c in "0123456789abcdefABCDEF" for c in hex_str)
