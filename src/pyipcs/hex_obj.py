"""
pyIPCS Hex Object
"""

from collections.abc import Iterable
import copy


class Hex:
    """
    Hex Object

    Contains various methods and functionality to manage hex variables in a IPCS environment

    Methods:
    ```
        __init__(value:str|int) -> None:
            Constructor for Hex Object

        sign() -> str:
            Get sign of hex value.

        unsigned() -> pyipcs.Hex:
            Get unsigned hex value.

        get_nibble(nibble:int, from_right:bool=False):
            Get 0 indexed nibble. Default 0 index is from left side of hex string.

        get_byte(byte:int, from_right:bool=False):
            Get 0 indexed byte. Default 0 index is from left side of hex string.

        get_half_word(half_word:int, from_right:bool=False):
            Get 0 indexed half word. Default 0 index is from left side of hex string.

        get_word(word:int, from_right:bool=False):
            Get 0 indexed word. Default 0 index is from left side of hex string.

        get_doubleword(doubleword:int, from_right:bool=False):
            Get 0 indexed doubleword. Default 0 index is from left side of hex string.

        to_int() -> int:
            Convert hex to an integer.

        to_str() -> str:
            Convert Hex object to a hex string.

        to_char_str(encoding:str="ibm1047") -> str:
            Convert hex to character string.

        concat(other) -> pyipcs.Hex:
            Concatenate with other Hex Object/Objects.

        resize(new_bit_length:int) -> pyipcs.Hex:
            Convert hex string to new bit length.

        bit_len_no_pad() -> int:
            Determine bit length of hex string, not including leading 0s.

        bit_len() -> int:
            Determine bit length of hex string, including leading 0s.

        turn_on_bit(bit_position:int, from_right:bool=False) -> pyipcs.Hex:
            Turn on bit at 0 indexed bit position. Default 0 index is from left side of hex string.

        turn_off_bit(bit_position:int, from_right:bool=False) -> pyipcs.Hex:
            Turn off bit at 0 indexed bit position. Default 0 index is from left side of hex string.

        check_bit(bit_position:int, from_right:bool=False) -> bool:
            Check bit at 0 indexed bit position. Default 0 index is from left side of hex string.

    ```
    """

    def __init__(self, value: str | int) -> None:
        """
        Constructor for Hex Object

        Either convert int to hex string or check that string is valid hex
        Then convert hex string to IPCS format and Store

        Args:
            value (str|int):
                hex string or integer for hex value
        Returns:
            None
        """
        # ==============================
        #  TYPE ERRORS CHECK
        # ==============================

        if not isinstance(value, int) and not isinstance(value, str):
            raise TypeError(
                f"Hex 'value' must be of type str or int, but got {type(value)}"
            )

        # =================================
        # Convert value to IPCS Hex string
        # =================================

        self.__value = value

        # Convert int to hex string
        if isinstance(self.__value, int):
            if self.__value < 0:
                self.__value = "-" + hex(self.__value * -1)
            else:
                self.__value = hex(self.__value)

        # Remove spaces from hex string if they exist (ex. 01234567 89ABCDEF -> 0123456789ABCDEF)
        self.__value = "".join(self.__value.split())

        # Convert to uppercase
        self.__value = self.__value.upper()

        # Remove sign and set sign attribute
        if self.__value.startswith("-"):
            self.__value = self.__value.removeprefix("-")
            sign = "-"
        else:
            sign = ""

        # Remove 0X from hex string
        self.__value = self.__value.removeprefix("0X")

        # Check if value is hex
        if not all(c in "0123456789abcdefABCDEF" for c in self.__value):
            raise ValueError(f"Hex 'value' {value} is not a valid hexadecimal string")

        # Insert sign back into value
        if not all(c == "0" for c in self.__value):
            self.__value = sign + self.__value

    def __pyipcs_json__(self) -> str:
        """
        Convert Hex object for JSON format

        Returns:
            str
        """
        return {
            "__ipcs_type__": "Hex",
            "value": copy.deepcopy(self.to_str()),
        }

    # ==============================
    # Get sign and unsigned values
    # ==============================

    def sign(self) -> str:
        """
        Get sign of hex value.

        Returns:
            str : '-' or '' depending on whether Hex is positive or negative
        """
        if self.__value.startswith("-"):
            return "-"
        return ""

    def unsigned(self):
        """
        Get unsigned hex value.

        Returns:
            pyipcs.Hex : unsigned Hex
        """
        return Hex(self.__value.removeprefix("-"))

    # ======================
    # Get Functions
    # ======================
    def __getitem__(self, key):
        return Hex(self.__value.removeprefix("-")[key])

    def get_nibble(self, nibble: int, from_right: bool = False):
        """
        Get 0 indexed nibble. Default 0 index is from left side of hex string.

        Args:
            nibble (int):
                0 indexed nibble position
            from_right (bool):
                Optional. If 'True' will make 0 index the right most nibble. 'False' by Default.
        Returns:
            pyipcs.Hex: 0 indexed nibble at position nibble
        """
        if not isinstance(nibble, int):
            raise TypeError(
                f"Argument 'nibble' must be of type int, but got {type(nibble)}"
            )
        if not isinstance(from_right, bool):
            raise TypeError(
                f"Argument 'from_right' must be of type bool, but got {type(from_right)}"
            )
        return self.__get_chunk(nibble, 1, from_right)

    def get_byte(self, byte: int, from_right: bool = False):
        """
        Get 0 indexed byte. Default 0 index is from left side of hex string.

        Args:
            byte (int):
                0 indexed byte position
            from_right (bool):
                Optional. If 'True' will make 0 index the right most byte. 'False' by Default.
        Returns:
            pyipcs.Hex: 0 indexed byte at position byte
        """
        if not isinstance(byte, int):
            raise TypeError(
                f"Argument 'byte' must be of type int, but got {type(byte)}"
            )
        if not isinstance(from_right, bool):
            raise TypeError(
                f"Argument 'from_right' must be of type bool, but got {type(from_right)}"
            )
        return self.__get_chunk(byte, 2, from_right)

    def get_half_word(self, half_word: int, from_right: bool = False):
        """
        Get 0 indexed half word. Default 0 index is from left side of hex string.

        Args:
            half_word (int):
                0 indexed half word position
            from_right (bool):
                Optional. If 'True' will make 0 index the right most half word. 'False' by Default.
        Returns:
            pyipcs.Hex: 0 indexed half word at position half_word
        """
        if not isinstance(half_word, int):
            raise TypeError(
                f"Argument 'half_word' must be of type int, but got {type(half_word)}"
            )
        if not isinstance(from_right, bool):
            raise TypeError(
                f"Argument 'from_right' must be of type bool, but got {type(from_right)}"
            )
        return self.__get_chunk(half_word, 4, from_right)

    def get_word(self, word: int, from_right: bool = False):
        """
        Get 0 indexed word. Default 0 index is from left side of hex string.

        Args:
            word (int):
                0 indexed word position
            from_right (bool):
                Optional. If 'True' will make 0 index the right most word. 'False' by Default.
        Returns:
            pyipcs.Hex: 0 indexed word at position word
        """
        if not isinstance(word, int):
            raise TypeError(
                f"Argument 'word' must be of type int, but got {type(word)}"
            )
        if not isinstance(from_right, bool):
            raise TypeError(
                f"Argument 'from_right' must be of type bool, but got {type(from_right)}"
            )
        return self.__get_chunk(word, 8, from_right)

    def get_doubleword(self, doubleword: int, from_right: bool = False):
        """
        Get 0 indexed doubleword. Default 0 index is from left side of hex string.

        Args:
            doubleword (int):
                0 indexed doubleword position
            from_right (bool):
                Optional. If 'True' will make 0 index the right most doubleword.
                'False' by Default.
        Returns:
            pyipcs.Hex: 0 indexed doubleword at position doubleword
        """
        if not isinstance(doubleword, int):
            raise TypeError(
                f"Argument 'doubleword' must be of type int, but got {type(doubleword)}"
            )
        if not isinstance(from_right, bool):
            raise TypeError(
                f"Argument 'from_right' must be of type bool, but got {type(from_right)}"
            )
        return self.__get_chunk(doubleword, 16, from_right)

    # ============================
    # Convert hex to other types
    # ============================

    def to_int(self) -> int:
        """
        Convert hex to an integer.

        Returns:
            int : hex integer
        """
        return int(self.__value, 16)

    def to_str(self) -> str:
        """
        Convert Hex object to a hex string.

        Returns:
            str : hex string
        """
        return self.__value

    def to_char_str(self, encoding: str = "ibm1047") -> str:
        """
        Convert hex to character string.

        If there is an error reading the hex string to characters, will return empty string('').

        Args:
            encoding (str):
                Optional. Encoding to use to decode hex string. Default is 'ibm1047'.
        Returns:
            str : character string
        """
        try:
            # Convert hex string to bytes
            data_bytes = bytes.fromhex(self.to_str())
            # Decode using IBM1047 encoding, replace any errors with spaces
            text_data = data_bytes.decode(encoding, errors="replace")
            return text_data
        except Exception:
            return ""

    # ==========================
    # Print and Hash Functions
    # ==========================

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f"Hex(\'{self.to_str()}\')"

    def __hash__(self) -> int:
        return hash(self.to_int())

    # ===============================
    # Concat Function
    # ===============================
    def concat(self, other):
        """
        Concatenate with other Hex Object/Objects

        Args:
            other (pyipcs.Hex|Iterable):
                Other Hex object or Iterable of Hex objects
                to concatenate to the end of the current Hex Object.
                Disregard sign of this variable in concatenation.
        Returns:
            pyipcs.Hex: Concatenated Hex Object
        """
        if isinstance(other, Hex):
            return Hex(self.to_str() + other.unsigned().to_str())
        if not isinstance(other, Iterable):
            raise TypeError(
                f"Argument 'other' must be of type pyipcs.Hex or Iterable, but got {type(other)}"
            )
        new_hex = Hex(self.to_str())
        for o in other:
            if isinstance(o, Hex):
                new_hex = Hex(new_hex.to_str() + o.unsigned().to_str())
            else:
                raise TypeError(
                    f"Items of iterable 'other' must be of type pyipcs.Hex, but got {type(o)}"
                )
        return new_hex

    # =================
    # Bit Functions
    # =================

    def resize(self, new_bit_length: int):
        """
        Convert hex string to new bit length.

        Will either pad hex string with 0s or truncate string at bit length.

        Args:
            new_bit_length (int):
                new length of string in bits
        Returns:
            pyipcs.Hex: hex with new bit length
        """
        if not isinstance(new_bit_length, int):
            raise TypeError(
                f"Argument 'new_bit_length' must be of type int, but got {type(new_bit_length)}"
            )
        if new_bit_length < 0:
            raise ValueError("new_bit_length cannot be less than 0")

        # Convert just hex part of string to int
        new_hex_int = self.unsigned().to_int()

        # If bit length is less than current bit length
        # Use logical AND up to that bit to truncate
        if new_bit_length < new_hex_int.bit_length():
            new_hex_int = new_hex_int & ((1 << new_bit_length) - 1)

        new_hex_str = hex(new_hex_int).removeprefix("0x")

        # If new_bit_length is greater than hex_str figure
        # Figure out what the new string length needs to be
        # Use negative so it rounds up
        new_str_length = -(-new_bit_length // 4)

        # pad to new length, add current sign for sign, and return as new Hex object
        return Hex(self.sign() + new_hex_str.zfill(new_str_length))

    def bit_len_no_pad(self) -> int:
        """
        Determine bit length of hex string, not including leading 0s.

        Returns:
            int: Length in bits of hex string, not including leading 0s
        """
        return self.to_int().bit_length()

    def bit_len(self) -> int:
        """
        Determine bit length of hex string, including leading 0s.

        Returns:
            int: Length in bits of hex string, including leading 0s
        """
        return len(self.unsigned().to_str()) * 4

    def turn_on_bit(self, bit_position: int, from_right: bool = False):
        """
        Turn on bit at 0 indexed bit position. Default 0 index is from left side of hex string.

        Args:
            bit_position (int):
                0 indexed bit position
            from_right (bool):
                Optional. If 'True' will make 0 index the right most bit. 'False' by Default.
        Returns:
            pyipcs.Hex: hex with bit at bit_position on
        """
        if not isinstance(bit_position, int):
            raise TypeError(
                f"Argument 'bit_position' must be of type int, but got {type(bit_position)}"
            )
        if not isinstance(from_right, bool):
            raise TypeError(
                f"Argument 'from_right' must be of type bool, but got {type(from_right)}"
            )

        hex_part = self.unsigned().to_str()

        # Determine bit length
        bit_length = len(hex_part) * 4

        # Calculate correct bit length if from_right is on
        if from_right:
            bit_position = bit_length - 1 - bit_position

        if bit_position >= bit_length or bit_position < 0:
            raise ValueError("Argument 'bit_position' is out of bounds")

        # Calculate index of hex digit to change
        index = bit_position // 4
        # Calculate new hex digit
        new_digit_value = int(hex_part[index], 16) | (1 << (3 - (bit_position % 4)))

        # Remove 0x and ensure you are only getting one digit
        new_digit_value = hex(new_digit_value)[2:]
        if len(new_digit_value) > 1:
            new_digit_value = new_digit_value[-1]

        # Create new Hex Object with bit turned on
        return Hex(
            self.sign() + hex_part[:index] + new_digit_value + hex_part[index + 1 :]
        )

    def turn_off_bit(self, bit_position: int, from_right: bool = False):
        """
        Turn off bit at 0 indexed bit position. Default 0 index is from left side of hex string.

        Args:
            bit_position (int):
                0 indexed bit position
            from_right (bool):
                Optional. If 'True' will make 0 index the right most bit. 'False' by Default.
        Returns:
            pyipcs.Hex: hex with bit at bit_position off.
        """
        if not isinstance(bit_position, int):
            raise TypeError(
                f"Argument 'bit_position' must be of type int, but got {type(bit_position)}"
            )
        if not isinstance(from_right, bool):
            raise TypeError(
                f"Argument 'from_right' must be of type bool, but got {type(from_right)}"
            )

        hex_part = self.unsigned().to_str()

        # Determine bit length
        bit_length = len(hex_part) * 4

        # Calculate correct bit length if from_right is on
        if from_right:
            bit_position = bit_length - 1 - bit_position

        if bit_position >= bit_length or bit_position < 0:
            raise ValueError("Argument 'bit_position' is out of bounds")

        # Calculate index of hex digit to change
        index = bit_position // 4
        # Calculate new hex digit
        new_digit_value = int(hex_part[index], 16) & ~(1 << (3 - (bit_position % 4)))

        # Remove 0x and ensure you are only getting one digit
        new_digit_value = hex(new_digit_value)[2:]
        if len(new_digit_value) > 1:
            new_digit_value = new_digit_value[-1]

        # Create new Hex Object with bit turned off
        return Hex(
            self.sign() + hex_part[:index] + new_digit_value + hex_part[index + 1 :]
        )

    def check_bit(self, bit_position: int, from_right: bool = False) -> bool:
        """
        Check bit at 0 indexed bit position. Default 0 index is from left side of hex string.

        Args:
            bit_position (int):
                0 indexed bit position
            from_right (bool):
                Optional. If 'True' will make 0 index the right most bit. 'False' by Default.
        Returns:
            bool: 'True' if bit is on, 'False' if it is off
        """
        if not isinstance(bit_position, int):
            raise TypeError(
                f"Argument 'bit_position' must be of type int, but got {type(bit_position)}"
            )
        if not isinstance(from_right, bool):
            raise TypeError(
                f"Argument 'from_right' must be of type bool, but got {type(from_right)}"
            )

        hex_part = self.unsigned().to_str()

        # Determine bit length
        bit_length = len(hex_part) * 4

        # Calculate correct bit length if from_right is on
        if from_right:
            bit_position = bit_length - 1 - bit_position

        if not 0 <= bit_position < bit_length:
            raise ValueError("Argument 'bit_position' is out of bounds")

        # Calculate index of hex digit to change
        index = bit_position // 4
        # Check if bit is on
        is_bit_on = int(hex_part[index], 16) & (1 << (3 - (bit_position % 4)))

        return bool(is_bit_on)

    # ======================
    # Logical Functions
    # ======================

    def __eq__(self, other) -> bool:
        """
        Equal special method for Hex Object

        Will determine whether hex int is equal to other hex int.
        Will not take into account leading zeros

        """
        if isinstance(other, Hex):
            return self.to_int() == other.to_int()
        return False

    def __ne__(self, other) -> bool:
        """Not equal special method for Hex Object"""
        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        """Less than special method for Hex Object"""
        if isinstance(other, Hex):
            return self.to_int() < other.to_int()
        raise TypeError("unsupported operand type(s) for <: 'Hex' and Non 'Hex' type")

    def __le__(self, other) -> bool:
        """Less than or equal to special method for Hex Object"""
        if isinstance(other, Hex):
            return self.to_int() <= other.to_int()
        raise TypeError("unsupported operand type(s) for <=: 'Hex' and Non 'Hex' type")

    def __gt__(self, other) -> bool:
        """Greater than special method for Hex Object"""
        if isinstance(other, Hex):
            return self.to_int() > other.to_int()
        raise TypeError("unsupported operand type(s) for >: 'Hex' and Non 'Hex' type")

    def __ge__(self, other) -> bool:
        """Greater than or equal to special method for Hex Object"""
        if isinstance(other, Hex):
            return self.to_int() >= other.to_int()
        raise TypeError("unsupported operand type(s) for >=: 'Hex' and Non 'Hex' type")

    def __or__(self, other):
        """Or special method for Hex Object"""
        if isinstance(other, Hex):
            new_hex_obj = Hex(self.to_int() | other.to_int())
            if new_hex_obj.bit_len() < self.bit_len():
                new_hex_obj = new_hex_obj.resize(self.bit_len())
            return new_hex_obj
        raise TypeError("unsupported operand type(s) for |: 'Hex' and Non 'Hex' type")

    def __and__(self, other):
        """And special method for Hex Object"""
        if isinstance(other, Hex):
            new_hex_obj = Hex(self.to_int() & other.to_int())
            if new_hex_obj.bit_len() < self.bit_len():
                new_hex_obj = new_hex_obj.resize(self.bit_len())
            return new_hex_obj
        raise TypeError("unsupported operand type(s) for &: 'Hex' and Non 'Hex' type")

    # ======================
    # Arithmetic Functions
    # ======================

    def __add__(self, other):
        """Add special method for Hex Object"""
        if isinstance(other, Hex):
            new_hex_obj = Hex(self.to_int() + other.to_int())
            if new_hex_obj.bit_len() < self.bit_len():
                new_hex_obj = new_hex_obj.resize(self.bit_len())
            return new_hex_obj
        raise TypeError("unsupported operand type(s) for +: 'Hex' and Non 'Hex' type")

    def __sub__(self, other):
        """Subtract special method for Hex Object"""
        if isinstance(other, Hex):
            new_hex_obj = Hex(self.to_int() - other.to_int())
            if new_hex_obj.bit_len() < self.bit_len():
                new_hex_obj = new_hex_obj.resize(self.bit_len())
            return new_hex_obj
        raise TypeError("unsupported operand type(s) for -: 'Hex' and Non 'Hex' type")

    def __mul__(self, other):
        """Multiply special method for Hex Object"""
        if isinstance(other, Hex):
            new_hex_obj = Hex(self.to_int() * other.to_int())
            if new_hex_obj.bit_len() < self.bit_len():
                new_hex_obj = new_hex_obj.resize(self.bit_len())
            return new_hex_obj
        raise TypeError("unsupported operand type(s) for *: 'Hex' and Non 'Hex' type")

    def __truediv__(self, other):
        """Division special method for Hex Object"""
        if isinstance(other, Hex):
            new_hex_obj = Hex(self.to_int() // other.to_int())
            if new_hex_obj.bit_len() < self.bit_len():
                new_hex_obj = new_hex_obj.resize(self.bit_len())
            return new_hex_obj
        raise TypeError("unsupported operand type(s) for /: 'Hex' and Non 'Hex' type")

    def __mod__(self, other):
        """Modulo special method for Hex Object"""
        if isinstance(other, Hex):
            new_hex_obj = Hex(self.to_int() % other.to_int())
            if new_hex_obj.bit_len() < self.bit_len():
                new_hex_obj = new_hex_obj.resize(self.bit_len())
            return new_hex_obj
        raise TypeError("unsupported operand type(s) for %: 'Hex' and Non 'Hex' type")

    def __get_chunk(
        self, chunk: int, chunk_nibble_length: int, from_right: bool = False
    ):
        """Used by all get hex functions to grab a hex chunk

        Args:
            chunk (int):
                0 indexed chunk position
            chunk_nibble_length (int):
                length of hex chunk to grab
            from_right (bool): Optional.
                If 'True' will make 0 index the right most chunk. 'False' by Default
        Returns:
            pyipcs.Hex: 0 indexed chunk of chunk_nibble_length at position chunk
        """

        if from_right:
            start_index = (
                len(self.unsigned().to_str())
                - chunk_nibble_length
                - (chunk * chunk_nibble_length)
            )
        else:
            start_index = chunk * chunk_nibble_length

        if (chunk * chunk_nibble_length) >= len(self.unsigned().to_str()) or chunk < 0:
            raise ValueError("Hex index out of bounds")

        return Hex(
            self.unsigned().to_str()[start_index : start_index + chunk_nibble_length]
        )
