from typing import IO

from ...common.types import Type, NullTerminatedString

class NullTerminatedStringList(Type):
    
    def __new__(cls, **kwargs):
        return super().__new__(cls, default=[], **kwargs)

    def check_value(self, value: str):
        if not isinstance(value, list):
            raise TypeError('Wrong type, got `{}` expect `list`'.format(type(value).__name__))

    def read(self, buffer: IO):
        values = []
        string = NullTerminatedString()
        current = string.read(buffer)
        
        while len(current) > 0:
            values.append(current)
            current = string.read(buffer)
        
        return values

    def write(self, values: list, buffer: IO):
        string = NullTerminatedString()
        for value in values:
            string.write(value, buffer)
        buffer.write(b'\0')
