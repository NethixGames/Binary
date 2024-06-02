import struct
from typing import Optional

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

    def write(self, buffer: bytes) -> None:
        self.buffer += buffer


class BinaryStream(Buffer):
    def read_bool(self) -> bool:
        return struct.unpack("?", self.read(1))[0]

    def write_bool(self, value: bool) -> None:
        self.write(struct.pack("?", value))
