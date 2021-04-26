import struct
import io
from typing import IO

## Base Type ##
class Type:
    _python_type = None

    def __new__(cls, default=None, **kwargs):
        obj = object.__new__(cls)

        obj.__default = default
        obj.__options = kwargs

        return obj

    @property
    def default(self):
        return self.__default

    def check_value(self, value):
        pass

    def read(self, buffer: IO):
        raise NotImplementedError()

    def write(self, value, buffer: IO):
        raise NotImplementedError()


## Numeric Types ##
class NumericType(Type):
    _python_type = int

    def __new__(cls, default=0, signed=True, **kwargs):
        obj = super().__new__(cls, default, **kwargs)
        obj.__signed = signed
        obj.__format = '{}{}'.format(cls.__order, cls.__ctype[signed])
        return obj

    def __init_subclass__(cls, nbytes: int, order='big'):
        cls.__nbytes = nbytes

        if nbytes == 1:
            cls.__ctype = ['B','b']
        elif nbytes == 2:
            cls.__ctype = ['H','h']
        elif nbytes == 4:
            cls.__ctype = ['I', 'i']
        elif nbytes == 8:
            cls.__ctype = ['Q', 'q']
        else:
            raise ValueError('Invalid number of bytes. Valid values are `1`, `2`, `4` or `8`')

        if order == 'big':
            cls.__order = '>'
        elif order == 'little':
            cls.__order = '<'
        else:
            cls.__order = '='

    def check_value(self, value: int):
        if not isinstance(value, int):
            raise TypeError('Wrong type, got `{}` expect `int`'.format(type(value).__name__))
        
        bits = struct.calcsize(self.__format) * 8
        min_val, max_val = 0, (2**bits) - 1
        if self.__signed:
            min_val = -(2**bits) // 2
            max_val = ((2**bits) // 2) - 1
        
        if not (min_val <= value <= max_val):
            raise ValueError('The value is too big or to small. Value must be between `{}` and `{}`'.format(min_val, max_val))

    @property
    def size(self):
        return self.__nbytes

    @property
    def signed(self):
        return self.__signed

    def read(self, buffer: IO):
        return struct.unpack(self.__format, buffer.read(self.__nbytes))[0]

    def write(self, value: int, buffer: IO):
        self.check_value(value)
        return buffer.write(struct.pack(self.__format, value))


class Byte(NumericType, nbytes=1):
    pass

class BigEndianShort(NumericType, nbytes=2):
    pass

class LittleEndianShort(NumericType, nbytes=2, order='little'):
    pass

class BigEndianInt32(NumericType, nbytes=4):
    pass

class LittleEndianInt32(NumericType, nbytes=4, order='little'):
    pass

class BigEndianInt64(NumericType, nbytes=8):
    pass

class LittleEndianInt64(NumericType, nbytes=8, order='little'):
    pass


## Floating Types ##
class FloatingType(Type):
    _python_type = float

    def __new__(cls, default=0, **kwargs):
        obj = super().__new__(cls, default, **kwargs)
        obj.__format = '{}{}'.format(cls.__order, cls.__ctype)
        return obj

    def __init_subclass__(cls, nbytes: int, order='big'):
        cls.__nbytes = nbytes
        if nbytes == 2:
            cls.__ctype = 'e'
        elif nbytes == 4:
            cls.__ctype = 'f'
        elif nbytes == 8:
            cls.__ctype = 'd'
        else:
            raise ValueError('Invalid size. Valid options are `2`,`4` or `8`')
        
        if order == 'big':
            cls.__order = '>'
        elif order == 'little':
            cls.__order = '<'
        else:
            cls.__order = '='

    def check_value(self, value: float):
        if not isinstance(value, float):
            raise TypeError('Wrong type, got `{}` expect `float`'.format(type(value).__name__))
        
        # Try to pack the value to see if it will fit
        struct.pack(self.__format, value)

    @property
    def size(self):
        return self.__nbytes

    def read(self, buffer: IO):
        return struct.unpack(self.__format, buffer.read(self.__nbytes))[0]

    def write(self, value: float, buffer: IO):
        self.check_value(value)
        return buffer.write(struct.pack(self.__format, value))


class BigEndianFloat16(FloatingType, nbytes=2):
    pass

class LittleEndianFloat16(FloatingType, nbytes=2, order='little'):
    pass

class BigEndianFloat32(FloatingType, nbytes=4):
    pass

class LittleEndianFloat32(FloatingType, nbytes=4, order='little'):
    pass

class BigEndianFloat64(FloatingType, nbytes=8):
    pass

class LittleEndianFloat64(FloatingType, nbytes=8, order='little'):
    pass


## Other Types ##
class Bool(Type):
    _python_type = bool

    def __new__(cls, default=False, **kwargs):
        return super().__new__(cls, default, **kwargs)

    def check_value(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError('Wrong type, got `{}` expect `bool`'.format(type(value).__name__))

    def read(self, buffer: IO):
        return struct.unpack('?', buffer.read(1))[0]
    
    def write(self, value: bool, buffer: IO):
        self.check_value(value)
        buffer.write(struct.pack('?', value))

class ArrayOf(Type):

    def __new__(cls, _type: Type, size: int, **kwargs):
        obj = super().__new__(cls,default=[_type.default for _ in range(size)], **kwargs)
        obj.__type = _type
        obj.__size = size
        return obj

    def check_value(self, value: list):
        if not isinstance(value, list):
            raise TypeError('Wrong type, got `{}` expect `list`'.format(type(value).__name__))
        
        if len(value) != self.__size:
            raise ValueError('List is too big, length is `{}` excpected `{}`'.format(len(value), self.__size))

    def read(self, buffer: IO):
        data = []
        for _ in range(self.__size):
            data.append(self.__type.read(buffer))
        return data

    def write(self, value: list, buffer: IO):
        self.check_value(value)
        for item in value:
            self.__type.write(item, buffer)

class NullTerminatedString(Type):
    _python_type = str

    def __new__(cls, encoding='ascii', **kwargs):
        obj = super().__new__(cls, default='')
        obj.__encoding = encoding
        return obj

    @property
    def encoding(self):
        return self.__encoding

    def check_value(self, value: str):
        if not isinstance(value, str):
            raise TypeError('Wrong type, got `{}` expect `str`'.format(type(value).__name__))
    
    def read(self, buffer: IO):
        text = b''
        
        byte = buffer.read(1)
        while byte != b'\0':
            text += byte
            byte = buffer.read(1)

        return text.decode(self.__encoding)

    def write(self, value: str, buffer: IO):
        self.check_value(value)
        buffer.write(value.encode(self.__encoding) + b'\0')

class Bytes(Type):
    _python_type = bytes

    def __new__(cls, nbytes: int, default=bytes(), **kwargs):
        obj = super().__new__(cls, default=default, **kwargs)
        obj.__nbytes = nbytes
        return obj

    def check_value(self, value: bytes):
        if not isinstance(value, bytes):
            raise TypeError('Wrong type, got `{}` expect `bytes`'.format(type(value).__name__))

        if len(value) > self.__nbytes:
            raise ValueError('Value is too big')

    def read(self, buffer: IO):
        return buffer.read(self.__nbytes)

    def write(self, value: bytes, buffer: IO):
        self.check_value(value)
        buffer.write(value)
