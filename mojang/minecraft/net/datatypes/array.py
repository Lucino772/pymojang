from typing import BinaryIO, Callable, Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


class _ByteArrayDataType(Generic[T]):
    def __init__(
        self,
        fixed_length: int,
        encode: Callable[[T], bytes],
        decode: Callable[[bytes], T],
    ) -> None:
        self.__fixed_length = fixed_length
        self.__encode = encode
        self.__decode = decode

    def write(self, buffer: BinaryIO, value: T):
        _bytes = self.__encode(value)
        if len(_bytes) != self.__fixed_length:
            raise RuntimeError(
                "Length of {} is different then expected length {}".format(
                    len(_bytes), self.__fixed_length
                )
            )

        return buffer.write(_bytes)

    def read(self, buffer: BinaryIO) -> T:
        _bytes = buffer.read(self.__fixed_length)
        return self.__decode(_bytes)


uuid_t = _ByteArrayDataType[UUID](
    16,
    encode=lambda value: value.bytes,
    decode=lambda value: UUID(bytes=value),
)
