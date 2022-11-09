import io
import struct


class _Number:
    def __init__(self, length: int) -> None:
        self.length = length

    def write(self, buffer: io.BytesIO, value: int, signed: bool = True):
        _bytes = value.to_bytes(self.length, "big", signed=signed)
        return buffer.write(_bytes)

    def read(self, buffer: io.BytesIO, signed: bool = True):
        _bytes = buffer.read(self.length)
        return int.from_bytes(_bytes, "big", signed=signed)


class _FloatingNumber:
    _formats = {4: ">f", 8: ">d"}

    def __init__(self, length: int):
        self.length = length

    def write(self, buffer: io.BytesIO, value: float):
        _bytes = struct.pack(self._formats[self.length], value)
        return buffer.write(_bytes)

    def read(self, buffer: io.BytesIO) -> float:
        _bytes = buffer.read(self.length)
        return struct.unpack(self._formats[self.length], _bytes)[0]


class _VarNumber:
    # FIXME: This class does not support negative numbers

    def __init__(self, length: int) -> None:
        self.length = length

    def write(self, buffer: io.BytesIO, value: int):
        written = 0
        while True:
            byte = value & 0x7F
            value >>= 7

            if value > 0:
                byte |= 0x80

            written += Byte.write(buffer, byte, False)

            if value == 0:
                break

        return written

    def read(self, buffer: io.BytesIO):
        val = 0

        for i in range(self.length):
            byte = Byte.read(buffer, False)

            val |= (byte & 0x7F) << (7 * i)

            if byte & 0x80 == 0:
                break

        return val


class Bool:
    @staticmethod
    def write(buffer: io.BytesIO, value: bool):
        _bytes = value.to_bytes(1, "big")
        return buffer.write(_bytes)

    @staticmethod
    def read(buffer: io.BytesIO):
        _bytes = buffer.read(1)
        return bool.from_bytes(_bytes, "big")


class _String:
    def __init__(self, length: int) -> None:
        self.length = length

    def write(self, buffer: io.BytesIO, value: str):
        if len(value) > self.length:
            raise RuntimeError("Max len for String is {}".format(self.length))

        written = VarInt.write(buffer, len(value))
        written += buffer.write(value.encode("utf-8"))
        return written

    def read(self, buffer: io.BytesIO):
        _len = VarInt.read(buffer)
        return buffer.read(_len).decode("utf-8")


Byte = _Number(1)
Short = _Number(2)
Int = _Number(4)
Long = _Number(8)

Float = _FloatingNumber(4)
Double = _FloatingNumber(8)

VarInt = _VarNumber(5)
VarLong = _VarNumber(10)

String = _String(32767)
