import io

from .common import Byte, Long


class Position:
    @classmethod
    def write(cls, buffer: io.BytesIO, x: int, z: int, y: int):
        value = ((x & 0x3FFFFFF) << 38) | ((z & 0x3FFFFFF) << 12) | (y & 0xFFF)
        return Long.write(buffer, value, False)

    @classmethod
    def read(cls, buffer: io.BytesIO):
        value = Long.read(buffer, False)

        x, z, y = value >> 38, (value >> 12) & 0x3FFFFFF, value & 0xFFF

        if x >= 1 << 25:
            x -= 1 << 26
        if y >= 1 << 11:
            y -= 1 << 12
        if z >= 1 << 25:
            z -= 1 << 26

        return x, z, y


class Angle:
    @classmethod
    def check_value(cls, value: int):
        if not (0 <= value <= 255):
            raise RuntimeError(
                "Angle value must be between 1 and 256: {}".format(value)
            )

        return value

    @classmethod
    def write(cls, buffer: io.BytesIO, value: int):
        cls.check_value(value)
        return Byte.write(buffer, value, False)

    @classmethod
    def read(cls, buffer: io.BytesIO):
        value = Byte.read(buffer, False)
        return cls.check_value(value)
