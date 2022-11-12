from typing import BinaryIO, Protocol, Sequence, TypeVar

T = TypeVar("T")


class _DataTypeProtocol(Protocol[T]):
    def write(self, buffer: BinaryIO, value: T) -> int:
        ...

    def read(self, buffer: BinaryIO) -> T:
        ...


class _ArrayDataTypeProtocol(Protocol[T]):
    def write(self, buffer: BinaryIO, value: Sequence[T]) -> int:
        ...

    def read(self, buffer: BinaryIO) -> Sequence[T]:
        ...


class _TagDataTypeProtocol(_DataTypeProtocol[T]):
    tag_id: int


class _TagArrayDataTypeProtocol(_ArrayDataTypeProtocol[T]):
    tag_id: int
