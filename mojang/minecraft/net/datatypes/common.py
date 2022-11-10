import ctypes
import json
import re
import struct
import uuid
from typing import BinaryIO, Union


class _Number:
    def __init__(self, length: int) -> None:
        self.length = length

    def write(self, buffer: BinaryIO, value: int, signed: bool = True):
        _bytes = value.to_bytes(self.length, "big", signed=signed)
        return buffer.write(_bytes)

    def read(self, buffer: BinaryIO, signed: bool = True):
        _bytes = buffer.read(self.length)
        return int.from_bytes(_bytes, "big", signed=signed)


class _FloatingNumber:
    _formats = {4: ">f", 8: ">d"}

    def __init__(self, length: int):
        self.length = length

    def write(self, buffer: BinaryIO, value: float):
        _bytes = struct.pack(self._formats[self.length], value)
        return buffer.write(_bytes)

    def read(self, buffer: BinaryIO) -> float:
        _bytes = buffer.read(self.length)
        return struct.unpack(self._formats[self.length], _bytes)[0]


class _VarNumber:
    def __init__(self, length: int, bits) -> None:
        self.length = length

        self.ctype_u = ctypes.c_uint32 if bits == 32 else ctypes.c_uint64
        self.ctype_i = ctypes.c_int32 if bits == 32 else ctypes.c_int64

    def write(self, buffer: BinaryIO, value: int):
        value = self.ctype_u(value).value
        written = 0
        while True:
            byte = value & 0x7F
            value >>= 7

            if value > 0:
                byte |= 0x80

            written += Byte.write(buffer, byte, False)

            if value == 0:
                break

        return written

    def read(self, buffer: BinaryIO):
        val = 0

        for i in range(self.length):
            byte = Byte.read(buffer, False)

            val |= (byte & 0x7F) << (7 * i)

            if byte & 0x80 == 0:
                break

        return self.ctype_i(val).value


class Bool:
    @staticmethod
    def write(buffer: BinaryIO, value: bool):
        _bytes = value.to_bytes(1, "big")
        return buffer.write(_bytes)

    @staticmethod
    def read(buffer: BinaryIO):
        _bytes = buffer.read(1)
        return bool.from_bytes(_bytes, "big")


class _String:
    def __init__(self, length: int) -> None:
        self.length = length

    def write(self, buffer: BinaryIO, value: str):
        if len(value) > self.length:
            raise RuntimeError("Max len for String is {}".format(self.length))

        written = VarInt.write(buffer, len(value))
        written += buffer.write(value.encode("utf-8"))
        return written

    def read(self, buffer: BinaryIO):
        _len = VarInt.read(buffer)
        return buffer.read(_len).decode("utf-8")


class Identifier:
    @classmethod
    def check_value(cls, value: str):
        results = re.fullmatch("(([a-z0-9.-_]*):)?([a-z0-9.-_/]*)", value)
        if results is None:
            raise RuntimeError("Identifier is not valid: {}".format(value))

        return results.groups()[1:]

    @classmethod
    def write(cls, buffer: BinaryIO, value: str):
        cls.check_value(value)
        return _String(32767).write(buffer, value)

    @classmethod
    def read(cls, buffer: BinaryIO):
        value = _String(32767).read(buffer)
        return cls.check_value(value)


class Chat:
    @classmethod
    def write(cls, buffer: BinaryIO, value: Union[dict, list]):
        value_str = json.dumps(value)
        return _String(262144).write(buffer, value_str)

    @classmethod
    def read(cls, buffer: BinaryIO) -> Union[dict, list]:
        value_str = _String(262144).read(buffer)
        return json.loads(value_str)


class UUID:
    @classmethod
    def write(cls, buffer: BinaryIO, value: uuid.UUID):
        return buffer.write(value.bytes)

    @classmethod
    def read(cls, buffer: BinaryIO):
        value = buffer.read(16)
        return uuid.UUID(bytes=value)


Byte = _Number(1)
Short = _Number(2)
Int = _Number(4)
Long = _Number(8)

Float = _FloatingNumber(4)
Double = _FloatingNumber(8)

VarInt = _VarNumber(5, 32)
VarLong = _VarNumber(10, 64)

String = _String(32767)
