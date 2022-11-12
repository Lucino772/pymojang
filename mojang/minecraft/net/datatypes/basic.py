from struct import Struct
from typing import BinaryIO, Generic, TypeVar

DataType_T = TypeVar("DataType_T")


class _GenericDataType(Generic[DataType_T]):
    def write(self, buffer: BinaryIO, value: DataType_T):
        raise NotImplementedError

    def read(self, buffer: BinaryIO) -> DataType_T:
        raise NotADirectoryError


class _BasicDataType(_GenericDataType[DataType_T]):
    def __init__(self, fmt: str):
        self.__fmt = Struct(fmt)

    def write(self, buffer: BinaryIO, value: DataType_T):
        data = self.__fmt.pack(value)
        return buffer.write(data)

    def read(self, buffer: BinaryIO) -> DataType_T:
        data = buffer.read(self.__fmt.size)
        return self.__fmt.unpack(data)[0]


int8_t = _BasicDataType[int](">b")
uint8_t = _BasicDataType[int](">B")
int16_t = _BasicDataType[int](">h")
uint16_t = _BasicDataType[int](">H")
int32_t = _BasicDataType[int](">i")
uint32_t = _BasicDataType[int](">I")
int64_t = _BasicDataType[int](">q")
uint64_t = _BasicDataType[int](">Q")

float32_t = _BasicDataType[float](">f")
float64_t = _BasicDataType[float](">d")

bool_t = _BasicDataType[bool](">?")
