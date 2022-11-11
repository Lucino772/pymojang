import json
import re
from typing import BinaryIO, Callable, Generic, TypeVar, Union

from .varnum import varint_t

T = TypeVar("T")


class _StringDataType(Generic[T]):
    def __init__(
        self,
        length: int,
        encode: Callable[[T], str],
        decode: Callable[[str], T],
    ) -> None:
        self.__length = length
        self.__encode = encode
        self.__decode = decode

    def write(self, buffer: BinaryIO, value: T):
        str_val = self.__encode(value)

        if len(str_val) > self.__length:
            raise RuntimeError(
                "Max len for String is {}".format(self.__length)
            )

        written = varint_t.write(buffer, len(str_val))
        written += buffer.write(str_val.encode("utf-8"))
        return written

    def read(self, buffer: BinaryIO) -> T:
        _len = varint_t.read(buffer)
        str_val = buffer.read(_len).decode("utf-8")
        return self.__decode(str_val)


string_t = _StringDataType[str](32767, encode=str, decode=str)


def _identifier_check(value: str):
    results = re.fullmatch("(([a-z0-9.-_]*):)?([a-z0-9.-_/]*)", value)
    if results is None:
        raise RuntimeError("Identifier is not valid: {}".format(value))

    return value


identifier_t = _StringDataType[str](
    32767, encode=_identifier_check, decode=_identifier_check
)

chat_t = _StringDataType[Union[dict, list]](
    262144, encode=json.dumps, decode=json.loads
)
