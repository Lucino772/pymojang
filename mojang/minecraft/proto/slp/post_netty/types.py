import struct
from typing import IO, Optional


class VarInt:

    @classmethod
    def write(cls, buffer: IO, value: int):
        while True:
            byte = value & 0x7f
            value >>= 7

            if value > 0:
                byte |= 0x80

            buffer.write(struct.pack('B', byte))
            
            if value == 0:
                break


    @classmethod
    def read(cls, buffer: IO) -> int:
        val = 0

        for i in range(5):
            byte = buffer.read(1)
            if len(byte) == 0:
                break

            val |= (ord(byte) & 0x7f) << (7*i)
            
            if ord(byte) & 0x80 == 0:
                break

        return val


class String:

    @classmethod
    def write(cls, buffer: IO, value: str, encoding: Optional[str] = 'utf-8'):
        value = value.encode(encoding)
        VarInt.write(buffer, len(value))
        buffer.write(value)


    @classmethod
    def read(cls, buffer: IO, encoding: Optional[str] = 'utf-8') -> str:
        length = VarInt.read(buffer)
        return buffer.read(length).decode(encoding)
