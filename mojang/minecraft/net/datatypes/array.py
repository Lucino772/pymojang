from typing import BinaryIO, Sequence, TypeVar

from .basic import _GenericDataType

T = TypeVar("T")


class _AdvancedArray(_GenericDataType[Sequence[T]]):
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

    def write(self, buffer: BinaryIO, values: Sequence[T]):
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

    def read(self, buffer: BinaryIO) -> Sequence[T]:
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


def array_t(data_t: _GenericDataType[T], length: int):
    return _AdvancedArray[T](
        item_t=data_t, max_len=-1, length=length, len_prefix_t=None
    )
