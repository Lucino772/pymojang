import io
import zlib
from typing import BinaryIO

from ..datatypes.common import VarInt


class _Packet:
    @property
    def packet_id(self) -> int:
        raise NotImplementedError

    def serialize(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, data: bytes):
        raise NotImplementedError


class Packets:
    @staticmethod
    def write(
        buffer: BinaryIO,
        packet: _Packet,
        compressed: bool = False,
        compression_threshold: int = -1,
    ):
        _bytes = packet.serialize()
        with io.BytesIO() as buff:
            VarInt.write(buff, packet.packet_id)
            buff.write(_bytes)

            data = buff.getvalue()

        data_length = len(data)
        if not compressed:
            with io.BytesIO() as buff:
                VarInt.write(buff, data_length)
                buff.write(data)

                return buffer.write(buff.getvalue())
        else:
            if -1 < compression_threshold < len(data):
                compressed_data = zlib.compress(data)
            else:
                compressed_data = data
                data_length = 0

            with io.BytesIO() as buff:
                VarInt.write(buff, data_length)
                buff.write(compressed_data)

                packet_data = buff.getvalue()

            with io.BytesIO() as buff:
                VarInt.write(buff, len(packet_data))
                buff.write(packet_data)

                return buffer.write(buff.getvalue())

    @staticmethod
    def read(buffer: BinaryIO, compressed: bool = False):
        if not compressed:
            data_length = VarInt.read(buffer)
            with io.BytesIO(buffer.read(data_length)) as buff:
                packet_id = VarInt.read(buff)
                packet_data = buff.read()

            return packet_id, packet_data
        else:
            packet_length = VarInt.read(buffer)
            with io.BytesIO(buffer.read(packet_length)) as buff:
                data_length = VarInt.read(buff)
                compressed_data = buff.read()

            if data_length == 0:
                uncompressed_data = compressed_data
            else:
                uncompressed_data = zlib.decompress(compressed_data)

            with io.BytesIO(uncompressed_data) as buff:
                packet_id = VarInt.read(buff)
                packet_data = buff.read()

            return packet_id, packet_data
