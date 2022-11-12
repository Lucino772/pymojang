import json
import re
from typing import BinaryIO, Callable, TypeVar, Union
from uuid import UUID

from .basic import _GenericDataType
from .varnum import varint_t

T = TypeVar("T")


class _AdvancedByteArray(_GenericDataType[T]):
    def __init__(
        self,
        encode: Callable[[T], bytes],
        decode: Callable[[bytes], T],
        max_len: int = -1,
        length: int = -1,
        len_prefix_t: _GenericDataType[int] = None,
    ) -> None:
        self.__max_len = max_len
        self.__length = length
        self.__len_prefix_t = len_prefix_t
        self.__encode = encode
        self.__decode = decode

    def write(self, buffer: BinaryIO, value: T):
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

    def read(self, buffer: BinaryIO) -> T:
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


def bytearray_t(length: int):
    return _AdvancedByteArray[bytes](
        max_len=-1,
        length=length,
        len_prefix_t=None,
        encode=lambda val: val,
        decode=lambda val: val,
    )


def string_t(max_len: int = 32767):
    return _AdvancedByteArray[str](
        max_len=max_len,
        length=-1,
        len_prefix_t=varint_t,
        encode=lambda val: val.encode("utf-8"),
        decode=lambda val: val.decode("utf-8"),
    )


def _identifier_check(value: str):
    results = re.fullmatch("(([a-z0-9.-_]*):)?([a-z0-9.-_/]*)", value)
    if results is None:
        raise RuntimeError("Identifier is not valid: {}".format(value))

    return value


identifier_t = _AdvancedByteArray[str](
    max_len=32767,
    length=-1,
    len_prefix_t=varint_t,
    encode=lambda val: _identifier_check(val).encode("utf-8"),
    decode=lambda val: _identifier_check(val.decode("utf-8")),
)


chat_t = _AdvancedByteArray[Union[dict, list]](
    max_len=262144,
    length=-1,
    len_prefix_t=varint_t,
    encode=lambda val: json.dumps(val).encode("utf-8"),
    decode=json.loads,
)


uuid_t = _AdvancedByteArray[UUID](
    max_len=-1,
    length=16,
    len_prefix_t=None,
    encode=lambda val: val.bytes,
    decode=lambda val: UUID(bytes=val),
)
