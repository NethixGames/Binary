import struct
from typing import Optional


class ByteOrder:
    LITTLE_ENDIAN = '<'
    BIG_ENDIAN = '>'


class ByteType:
    SIGNED_CHAR = 'b'
    UNSIGNED_CHAR = 'B'

    SIGNED_SHORT = 'h'
    UNSIGNED_SHORT = 'H'

    SIGNED_INT = 'i'
    UNSIGNED_INT = 'I'

    SIGNED_LONG = 'q'
    UNSIGNED_LONG = 'Q'

    FLOAT = 'f'
    DOUBLE = 'd'
    BOOLEAN = '?'


class ByteSize:
    SHORT = 2
    INT = 4
    LONG = 8

    FLOAT = 4
    DOUBLE = 8


class Buffer:
    def __init__(self, buffer: bytes = bytes(), offset: int = 0):
        self.buffer = buffer
        self.offset = offset

    def feos(self) -> bool:
        return len(self.buffer[self.offset:]) == 0

    def rewind(self) -> None:
        self.offset = 0

    def read(self, size: Optional[int] = 0) -> bytes:
        if size is None:
            size = bytes()

        if size < 0:
            raise ValueError("Size cannot be negative")

        remaining = len(self.buffer) - self.offset
        if remaining < size:
            raise OverflowError("Not enough bytes to read")

        buffer = self.buffer[self.offset:self.offset + size]
        self.offset += size

        return buffer

    def write(self, __bytes: bytes) -> None:
        self.buffer += __bytes


class BinaryStream(Buffer):
    def read_bool(self) -> bool:
        return struct.unpack(ByteType.BOOLEAN, self.read(1))[0]

    def write_bool(self, value: bool) -> None:
        self.write(struct.pack(ByteType.BOOLEAN, value))

    def read_byte(self, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> int:
        __format = order + (ByteType.UNSIGNED_CHAR if unsigned else ByteType.SIGNED_CHAR)
        return struct.unpack(__format, self.read(1))[0]

    def write_byte(self, value: int, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> None:
        __format = order + (ByteType.UNSIGNED_CHAR if unsigned else ByteType.SIGNED_CHAR)
        self.write(struct.pack(__format, value))

    def read_short(self, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> int:
        __format = order + (ByteType.UNSIGNED_SHORT if unsigned else ByteType.SIGNED_SHORT)
        return struct.unpack(__format, self.read(ByteSize.SHORT))[0]

    def write_short(self, value: int, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> None:
        __format = order + (ByteType.UNSIGNED_SHORT if unsigned else ByteType.SIGNED_SHORT)
        self.write(struct.pack(__format, value))

    def read_triad(self, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> int:
        __bytes = self.read(3)
        __format = order + (ByteType.UNSIGNED_INT if unsigned else ByteType.UNSIGNED_INT)
        __buffer = b"\x00" if unsigned else (b"\x00" if __bytes[2] < 0x80 else b"\xff")
        return struct.unpack(__format, __buffer + __bytes)[0]

    def write_triad(self, value: int, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> None:
        __format = order + (ByteType.UNSIGNED_INT if unsigned else ByteType.UNSIGNED_INT)
        self.write(struct.pack(__format, value)[1:])

    def read_int(self, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> int:
        __format = order + (ByteType.UNSIGNED_INT if unsigned else ByteType.SIGNED_INT)
        return struct.unpack(__format, self.read(ByteSize.INT))[0]

    def write_int(self, value: int, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> None:
        __format = order + (ByteType.UNSIGNED_INT if unsigned else ByteType.SIGNED_INT)
        self.write(struct.pack(__format, value))

    def read_long(self, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> int:
        __format = order + (ByteType.UNSIGNED_LONG if unsigned else ByteType.SIGNED_LONG)
        return struct.unpack(__format, self.read(ByteSize.LONG))[0]

    def write_long(self, value: int, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> None:
        __format = order + (ByteType.UNSIGNED_LONG if unsigned else ByteType.SIGNED_LONG)
        self.write(struct.pack(__format, value))

    def read_float(self, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> int:
        __format = order + (ByteType.FLOAT if unsigned else ByteType.FLOAT)
        return struct.unpack(__format, self.read(ByteSize.FLOAT))[0]

    def write_float(self, value: int, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> None:
        __format = order + (ByteType.FLOAT if unsigned else ByteType.FLOAT)
        self.write(struct.pack(__format, value))

    def read_double(self, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> int:
        __format = order + (ByteType.DOUBLE if unsigned else ByteType.DOUBLE)
        return struct.unpack(__format, self.read(ByteSize.DOUBLE))[0]

    def write_double(self, value: int, *, unsigned: bool = True, order: str = ByteOrder.BIG_ENDIAN) -> None:
        __format = order + (ByteType.DOUBLE if unsigned else ByteType.DOUBLE)
        self.write(struct.pack(__format, value))

    def read_var_int(self):
        value: int = 0
        for i in range(0, 35, 7):
            number = self.read_byte()
            value |= ((number & 0x7f) << i)
            if (number & 0x80) == 0:
                return value
        raise ValueError("VarInt is too big")

    def write_var_int(self, value: int) -> None:
        value &= 0xffffffff
        for i in range(0, 5):
            to_write: int = value & 0x7f
            value >>= 7
            if value != 0:
                self.write_byte(to_write | 0x80)
            else:
                self.write_byte(to_write)
                break
