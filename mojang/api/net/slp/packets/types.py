from typing import IO
import struct
import json
from ...common.types import Type, BigEndianShort

## VarTypes ##
class VarType(Type):
    _python_type = int

    def __new__(cls, default=0, **kwargs):
        return super().__new__(cls, default=default, **kwargs)

    def __init_subclass__(cls, nbytes: int):
        cls.__nbytes = nbytes

    def check_value(self, value: int):
        if not isinstance(value, int):
            raise TypeError('Wrong type, got `{}` expect `int`'.format(type(value).__name__))

    @property
    def size(self):
        return self.__nbytes

    def read(self, buffer: IO):
        val = 0

        for i in range(self.__nbytes):
            byte = buffer.read(1)
            if len(byte) == 0:
                break

            val |= (ord(byte) & 0x7f) << (7*i)
            
            if ord(byte) & 0x80 == 0:
                break

        return val

    def write(self, value: int, buffer: IO):
        while True:
            byte = value & 0x7f
            value >>= 7

            if value > 0:
                byte |= 0x80
            
            buffer.write(struct.pack('B', byte))
            
            if value == 0:
                break


class VarInt(VarType, nbytes=5):
    pass

class VarLong(VarType, nbytes=10):
    pass

## Other ##
class String(Type):
    _python_type = str

    def __new__(cls, default='', encoding='utf-8', **kwargs):
        obj = super().__new__(cls, default=default, **kwargs)
        obj.__encoding = encoding
        return obj

    @property
    def encoding(self):
        return self.__encoding

    def check_value(self, value: str):
        if not isinstance(value, str):
            raise TypeError('Wrong type, got `{}` expect `str`'.format(type(value).__name__))
    
    def read(self, buffer: IO):
        length = VarInt().read(buffer)
        return buffer.read(length).decode(self.__encoding)

    def write(self, value: str, buffer: IO):
        self.check_value(value)
        VarInt().write(len(value), buffer)
        buffer.write(value.encode(self.__encoding))

class JSONString(String):
    _python_type = dict

    def read(self, buffer: IO):
        return json.loads(super().read(buffer))

    def write(self, value: dict, buffer: IO):
        text = json.dumps(value)
        super().write(text, buffer)
