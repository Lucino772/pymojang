from typing import Any, BinaryIO, Generic, Iterable, TypeVar

from .basic import _GenericDataType

T = TypeVar("T")


class optional_t(Generic[T]):
    def __init__(self, data_t: _GenericDataType[T]) -> None:
        self.__data_t = data_t

    def write(self, buffer: BinaryIO, value: T, present: bool):
        if present:
            return self.__data_t.write(buffer, value)

        return 0

    def read(self, buffer: BinaryIO, present: bool, default: Any = None):
        if present:
            return self.__data_t.read(buffer)

        return default


class enum_t(Generic[T]):
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
