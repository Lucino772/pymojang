from struct import Struct
from typing import BinaryIO, Generic, TypeVar

T = TypeVar("T")


class _BasicDataType(Generic[T]):
    def __init__(self, fmt: str):
        self.__fmt = Struct(fmt)

    def write(self, buffer: BinaryIO, value: T):
        data = self.__fmt.pack(value)
        buffer.write(data)

    def read(self, buffer: BinaryIO) -> T:
        data = buffer.read(self.__fmt.size)
        return self.__fmt.unpack(data)[0]


int8_t = _BasicDataType[int](">b")
uint8_t = _BasicDataType[int](">B")
int16_t = _BasicDataType[int](">h")
uint16_t = _BasicDataType[int](">H")
int32_t = _BasicDataType[int](">i")
uint32_t = _BasicDataType[int](">I")
int64_t = _BasicDataType[int](">l")
uint64_t = _BasicDataType[int](">L")

float32_t = _BasicDataType[float](">f")
float64_t = _BasicDataType[float](">d")

bool_t = _BasicDataType[bool](">?")
