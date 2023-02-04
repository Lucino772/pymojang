import ctypes
import json
import re
import typing as t
from struct import Struct
from uuid import UUID

T = t.TypeVar("T")


class _GenericDataType(t.Generic[T]):
    def write(self, buffer: t.BinaryIO, value: T) -> int:
        raise NotImplementedError

    def read(self, buffer: t.BinaryIO) -> T:
        raise NotImplementedError

    def array(
        self,
        max_len: int = -1,
        length: int = -1,
        len_prefix_t: "_GenericDataType[int]" = None,
    ):
        return _AdvancedArray[T](self, max_len, length, len_prefix_t)

    def enum(self, values: t.Sequence[T]):
        return _EnumDatatype[T](self, values)

    def optional(self, present: bool, default: t.Optional[T] = None):
        return _OptionalDataType[T](self, present, default)


class _StructDataType(_GenericDataType[T]):
    def __init__(self, fmt: str) -> None:
        self.__fmt = Struct(fmt)

    def write(self, buffer: t.BinaryIO, value: T):
        data = self.__fmt.pack(value)
        return buffer.write(data)

    def read(self, buffer: t.BinaryIO) -> T:
        data = buffer.read(self.__fmt.size)
        return self.__fmt.unpack(data)[0]


class _OptionalDataType(_GenericDataType[t.Optional[T]]):
    def __init__(
        self,
        data_t: _GenericDataType[T],
        present: bool,
        default: t.Optional[T] = None,
    ) -> None:
        self.__data_t = data_t
        self.__present = present
        self.__default = default

    def write(self, buffer: t.BinaryIO, value: t.Optional[T]):
        if self.__present and value is not None:
            return self.__data_t.write(buffer, value)

        return 0

    def read(self, buffer: t.BinaryIO) -> t.Optional[T]:
        if self.__present:
            return self.__data_t.read(buffer)

        return self.__default


class _EnumDatatype(_GenericDataType[T]):
    def __init__(
        self,
        data_t: _GenericDataType[T],
        values: t.Sequence[T],
    ) -> None:
        self.__data_t = data_t
        self.__values = values

    def _check(self, value: T):
        if value not in self.__values:
            raise RuntimeError(
                "Value '{}' not in expected values {}".format(
                    value, self.__values
                )
            )

        return value

    def write(self, buffer: t.BinaryIO, value: T):
        return self.__data_t.write(buffer, self._check(value))

    def read(self, buffer: t.BinaryIO):
        return self._check(self.__data_t.read(buffer))


class _AdvancedArray(_GenericDataType[t.Sequence[T]]):
    def __init__(
        self,
        item_t: _GenericDataType[T],
        max_len: int = -1,
        length: int = -1,
        len_prefix_t: _GenericDataType[int] = None,
    ) -> None:
        self.__item_t = item_t
        self.__max_len = max_len
        self.__length = length
        self.__len_prefix_t = len_prefix_t

    def write(self, buffer: t.BinaryIO, values: t.Sequence[T]):
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

    def read(self, buffer: t.BinaryIO) -> t.Sequence[T]:
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


class _AdvancedByteArray(_GenericDataType[T]):
    def __init__(
        self,
        encode: t.Callable[[T], bytes],
        decode: t.Callable[[bytes], T],
        max_len: int = -1,
        length: int = -1,
        len_prefix_t: _GenericDataType[int] = None,
    ) -> None:
        self.__max_len = max_len
        self.__length = length
        self.__len_prefix_t = len_prefix_t
        self.__encode = encode
        self.__decode = decode

    def write(self, buffer: t.BinaryIO, value: T):
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

    def read(self, buffer: t.BinaryIO) -> T:
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

    def write(self, buffer: t.BinaryIO, value: int):
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

    def read(self, buffer: t.BinaryIO):
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

_bytearray_t = (
    lambda max_len=-1, length=-1, len_prefix_t=None: _AdvancedByteArray[bytes](
        encode=lambda val: val,
        decode=lambda val: val,
        max_len=max_len,
        length=length,
        len_prefix_t=len_prefix_t,
    )
)

bytearray_t = lambda length: _bytearray_t(-1, length, None)

_string_t = (
    lambda max_len=-1, length=-1, len_prefix_t=None: _AdvancedByteArray[str](
        encode=lambda val: val.encode("utf-8"),
        decode=lambda val: val.decode("utf-8"),
        max_len=max_len,
        length=length,
        len_prefix_t=len_prefix_t,
    )
)

string_t = lambda max_len=32767: _string_t(max_len, -1, varint_t())


def _identifier_check(value: str):
    results = re.fullmatch("(([a-z0-9.-_]*):)?([a-z0-9.-_/]*)", value)
    if results is None:
        raise RuntimeError("Identifier is not valid: {}".format(value))

    return value


identifier_t = lambda: _AdvancedByteArray[str](
    encode=lambda val: _identifier_check(val).encode("utf-8"),
    decode=lambda val: _identifier_check(val.decode("utf-8")),
    max_len=32767,
    length=-1,
    len_prefix_t=varint_t(),
)

chat_t = lambda: _AdvancedByteArray[t.Union[list, dict]](
    encode=lambda val: json.dumps(val).encode("utf-8"),
    decode=json.loads,
    max_len=262144,
    length=-1,
    len_prefix_t=varint_t(),
)

uuid_t = lambda: _AdvancedByteArray[UUID](
    encode=lambda val: val.bytes,
    decode=lambda val: UUID(bytes=val),
    max_len=-1,
    length=16,
    len_prefix_t=None,
)
