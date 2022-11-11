import ctypes
from typing import BinaryIO

from .basic import uint8_t


class _VarNumberDataType:
    def __init__(self, length: int, intXX_t, uintXX_t) -> None:
        self.__length = length
        self.__ctype_u = intXX_t
        self.__ctype_i = uintXX_t

    def write(self, buffer: BinaryIO, value: int):
        value = self.__ctype_u(value).value
        written = 0
        while True:
            byte = value & 0x7F
            value >>= 7

            if value > 0:
                byte |= 0x80

            written += uint8_t.write(buffer, byte)

            if value == 0:
                break

        return written

    def read(self, buffer: BinaryIO):
        val = 0

        for i in range(self.__length):
            byte = uint8_t.read(buffer)

            val |= (byte & 0x7F) << (7 * i)

            if byte & 0x80 == 0:
                break

        return self.__ctype_i(val).value


varint_t = _VarNumberDataType(5, ctypes.c_int32, ctypes.c_uint32)
varlong_t = _VarNumberDataType(10, ctypes.c_int64, ctypes.c_uint64)
