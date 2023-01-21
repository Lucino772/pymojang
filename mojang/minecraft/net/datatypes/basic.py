import ctypes
import json
import re
from struct import Struct
from typing import BinaryIO, Callable, Generic, Optional, Sequence, TypeVar
from uuid import UUID

DataType_T = TypeVar("DataType_T")


class _GenericDataType(Generic[DataType_T]):
    def write(self, buffer: BinaryIO, value: DataType_T) -> int:
        raise NotImplementedError

    def read(self, buffer: BinaryIO) -> DataType_T:
        raise NotImplementedError

    def array(
        self,
        max_len: int = -1,
        length: int = -1,
        len_prefix_t: "_GenericDataType[int]" = None,
    ):
        return _AdvancedArray[DataType_T](self, max_len, length, len_prefix_t)

    def enum(self, values: Sequence[DataType_T]):
        return _EnumDatatype[DataType_T](self, values)

    def optional(self, present: bool, default: Optional[DataType_T] = None):
        return _OptionalDataType[DataType_T](self, present, default)


class _StructDataType(_GenericDataType[DataType_T]):
    def __init__(self, fmt: str) -> None:
        self.__fmt = Struct(fmt)

    def write(self, buffer: BinaryIO, value: DataType_T):
        data = self.__fmt.pack(value)
        return buffer.write(data)

    def read(self, buffer: BinaryIO) -> DataType_T:
        data = buffer.read(self.__fmt.size)
        return self.__fmt.unpack(data)[0]


class _OptionalDataType(_GenericDataType[Optional[DataType_T]]):
    def __init__(
        self,
        data_t: _GenericDataType[DataType_T],
        present: bool,
        default: Optional[DataType_T] = None,
    ) -> None:
        self.__data_t = data_t
        self.__present = present
        self.__default = default

    def write(self, buffer: BinaryIO, value: Optional[DataType_T]):
        if self.__present and value is not None:
            return self.__data_t.write(buffer, value)

        return 0

    def read(self, buffer: BinaryIO) -> Optional[DataType_T]:
        if self.__present:
            return self.__data_t.read(buffer)

        return self.__default


class _EnumDatatype(_GenericDataType[DataType_T]):
    def __init__(
        self,
        data_t: _GenericDataType[DataType_T],
        values: Sequence[DataType_T],
    ) -> None:
        self.__data_t = data_t
        self.__values = values

    def _check(self, value: DataType_T):
        if value not in self.__values:
            raise RuntimeError(
                "Value '{}' not in expected values {}".format(
                    value, self.__values
                )
            )

        return value

    def write(self, buffer: BinaryIO, value: DataType_T):
        return self.__data_t.write(buffer, self._check(value))

    def read(self, buffer: BinaryIO):
        return self._check(self.__data_t.read(buffer))


class _AdvancedArray(_GenericDataType[Sequence[DataType_T]]):
    def __init__(
        self,
        item_t: _GenericDataType[DataType_T],
        max_len: int = -1,
        length: int = -1,
        len_prefix_t: _GenericDataType[int] = None,
    ) -> None:
        self.__item_t = item_t
        self.__max_len = max_len
        self.__length = length
        self.__len_prefix_t = len_prefix_t

    def write(self, buffer: BinaryIO, values: Sequence[DataType_T]):
        if self.__max_len != -1 and len(values) > self.__max_len:
            raise RuntimeError(
                "Max len for Array is {}, got {}".format(
                    self.__max_len, len(values)
                )
            )

        written = 0
        if self.__len_prefix_t is not None:
            written += self.__len_prefix_t.write(buffer, len(values))
        elif self.__length != len(values):
            raise RuntimeError(
                "Expected fixed length {} for Array, got {}".format(
                    self.__length, len(values)
                )
            )

        written += sum(
            [self.__item_t.write(buffer, value) for value in values]
        )
        return written

    def read(self, buffer: BinaryIO) -> Sequence[DataType_T]:
        _len = self.__length
        if self.__len_prefix_t is not None:
            _len = self.__len_prefix_t.read(buffer)

        if _len == -1:
            raise RuntimeError("Failed to read Array length")

        if self.__max_len != -1 and _len > self.__max_len:
            raise RuntimeError(
                "Max len for Array is {}, got {}".format(self.__max_len, _len)
            )

        values = [self.__item_t.read(buffer) for _ in range(_len)]
        return values


class _AdvancedByteArray(_GenericDataType[DataType_T]):
    def __init__(
        self,
        encode: Callable[[DataType_T], bytes],
        decode: Callable[[bytes], DataType_T],
        max_len: int = -1,
        length: int = -1,
        len_prefix_t: _GenericDataType[int] = None,
    ) -> None:
        self.__max_len = max_len
        self.__length = length
        self.__len_prefix_t = len_prefix_t
        self.__encode = encode
        self.__decode = decode

    def write(self, buffer: BinaryIO, value: DataType_T):
        _bytes = self.__encode(value)
        if self.__max_len != -1 and len(_bytes) > self.__max_len:
            raise RuntimeError(
                "Max len for ByteArray is {}, got {}".format(
                    self.__max_len, len(_bytes)
                )
            )

        written = 0
        if self.__len_prefix_t is not None:
            written += self.__len_prefix_t.write(buffer, len(_bytes))
        elif self.__length != len(_bytes):
            raise RuntimeError(
                "Expected fixed length {} for ByteArray, got {}".format(
                    self.__length, len(_bytes)
                )
            )

        written += buffer.write(_bytes)
        return written

    def read(self, buffer: BinaryIO) -> DataType_T:
        _len = self.__length
        if self.__len_prefix_t is not None:
            _len = self.__len_prefix_t.read(buffer)

        if _len == -1:
            raise RuntimeError("Failed to read ByteArray length")

        _bytes = buffer.read(_len)
        if self.__max_len != -1 and len(_bytes) > self.__max_len:
            raise RuntimeError(
                "Max len for ByteArray is {}, got {}".format(
                    self.__max_len, len(_bytes)
                )
            )

        return self.__decode(_bytes)


class _VarNumberDataType(_GenericDataType[int]):
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

            written += uint8_t().write(buffer, byte)

            if value == 0:
                break

        return written

    def read(self, buffer: BinaryIO):
        val = 0

        for i in range(self.__length):
            byte = uint8_t().read(buffer)

            val |= (byte & 0x7F) << (7 * i)

            if byte & 0x80 == 0:
                break

        return self.__ctype_i(val).value


varint_t = lambda: _VarNumberDataType(5, ctypes.c_int32, ctypes.c_uint32)
varlong_t = lambda: _VarNumberDataType(10, ctypes.c_int64, ctypes.c_uint64)

int8_t = lambda: _StructDataType[int](">b")
uint8_t = lambda: _StructDataType[int](">B")
int16_t = lambda: _StructDataType[int](">h")
uint16_t = lambda: _StructDataType[int](">H")
int32_t = lambda: _StructDataType[int](">i")
uint32_t = lambda: _StructDataType[int](">I")
int64_t = lambda: _StructDataType[int](">q")
uint64_t = lambda: _StructDataType[int](">Q")

float32_t = lambda: _StructDataType[float](">f")
float64_t = lambda: _StructDataType[float](">d")

bool_t = lambda: _StructDataType[bool](">?")


def _bytearray_t(
    max_len: int = -1,
    length: int = -1,
    len_prefix_t: _GenericDataType[int] = None,
):
    return _AdvancedByteArray(
        encode=lambda val: val,
        decode=lambda val: val,
        max_len=max_len,
        length=length,
        len_prefix_t=len_prefix_t,
    )


def _string_t(
    max_len: int = -1,
    length: int = -1,
    len_prefix_t: _GenericDataType[int] = None,
):
    return _AdvancedByteArray(
        encode=lambda val: val.encode("utf-8"),
        decode=lambda val: val.decode("utf-8"),
        max_len=max_len,
        length=length,
        len_prefix_t=len_prefix_t,
    )


def _identifier_check(value: str):
    results = re.fullmatch("(([a-z0-9.-_]*):)?([a-z0-9.-_/]*)", value)
    if results is None:
        raise RuntimeError("Identifier is not valid: {}".format(value))

    return value


def _identifier_t(
    max_len: int = -1,
    length: int = -1,
    len_prefix_t: _GenericDataType[int] = None,
):
    return _AdvancedByteArray(
        encode=lambda val: _identifier_check(val).encode("utf-8"),
        decode=lambda val: _identifier_check(val.decode("utf-8")),
        max_len=max_len,
        length=length,
        len_prefix_t=len_prefix_t,
    )


def _chat_t(
    max_len: int = -1,
    length: int = -1,
    len_prefix_t: _GenericDataType[int] = None,
):
    return _AdvancedByteArray(
        encode=lambda val: json.dumps(val).encode("utf-8"),
        decode=json.loads,
        max_len=max_len,
        length=length,
        len_prefix_t=len_prefix_t,
    )


def _uuid_t(
    max_len: int = -1,
    length: int = -1,
    len_prefix_t: _GenericDataType[int] = None,
):
    return _AdvancedByteArray(
        encode=lambda val: val.bytes,
        decode=lambda val: UUID(bytes=val),
        max_len=max_len,
        length=length,
        len_prefix_t=len_prefix_t,
    )


def bytearray_t(length: int):
    return _bytearray_t(max_len=-1, length=length, len_prefix_t=None)


def string_t(max_len: int = 32767):
    return _string_t(max_len=max_len, length=-1, len_prefix_t=varint_t())


def identifier_t():
    return _identifier_t(max_len=32767, length=-1, len_prefix_t=varint_t())


def chat_t():
    return _chat_t(max_len=262144, length=-1, len_prefix_t=varint_t())


def uuid_t():
    return _uuid_t(max_len=-1, length=16, len_prefix_t=None)
