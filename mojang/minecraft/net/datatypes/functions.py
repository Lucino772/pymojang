from typing import BinaryIO, Iterable, Optional, TypeVar

from .basic import _GenericDataType

T = TypeVar("T")


class optional_t(_GenericDataType[Optional[T]]):
    def __init__(
        self,
        data_t: _GenericDataType[T],
        present: bool,
        default: Optional[T] = None,
    ) -> None:
        self.__data_t = data_t
        self.__present = present
        self.__default = default

    def write(self, buffer: BinaryIO, value: Optional[T]):
        if self.__present and value is not None:
            return self.__data_t.write(buffer, value)

        return 0

    def read(self, buffer: BinaryIO) -> Optional[T]:
        if self.__present:
            return self.__data_t.read(buffer)

        return self.__default


class enum_t(_GenericDataType[T]):
    def __init__(
        self, data_t: _GenericDataType[T], values: Iterable[T]
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

    def write(self, buffer: BinaryIO, value: T):
        return self.__data_t.write(buffer, self._check(value))

    def read(self, buffer: BinaryIO):
        return self._check(self.__data_t.read(buffer))
