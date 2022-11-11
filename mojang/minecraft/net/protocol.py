import io
import zlib
from typing import BinaryIO

from .datatypes import varint_t
from .packets import _Packet


# write
def _make_packet_data(packet: _Packet):
    _bytes = packet.serialize()
    with io.BytesIO() as buffer:
        varint_t.write(buffer, packet.packet_id)
        buffer.write(_bytes)

        packet_data = buffer.getvalue()

    return packet_data


def _compressed_packet_data(data: bytes, threshold: int = 0):
    if len(data) > threshold:
        data_length = len(data)
        compressed_data = zlib.compress(data)
    else:
        data_length = 0
        compressed_data = data

    with io.BytesIO() as buffer:
        varint_t.write(buffer, data_length)
        buffer.write(compressed_data)

        return buffer.getvalue()


def _write_len_prefixed(buffer: BinaryIO, data: bytes):
    written = varint_t.write(buffer, len(data))
    written += buffer.write(data)
    return written


def write(
    buffer: BinaryIO,
    packet: _Packet,
    compressed: bool = False,
    threshold: int = 0,
):
    packet_data = _make_packet_data(packet)
    if compressed:
        packet_data = _compressed_packet_data(packet_data, threshold)

    return _write_len_prefixed(buffer, packet_data)


# read
def _make_packet(data: bytes):
    with io.BytesIO(data) as buffer:
        packet_id = varint_t.read(buffer)
        packet_data = buffer.read()

    return packet_id, packet_data


def _uncompressed_packet_data(data: bytes):
    with io.BytesIO(data) as buffer:
        data_length = varint_t.read(buffer)
        compressed_data = buffer.read()

    if data_length == 0:
        return compressed_data  # Data was not compressed
    else:
        return zlib.decompress(compressed_data)


def _read_len_prefixed(buffer: BinaryIO):
    length = varint_t.read(buffer)
    return buffer.read(length)


def read(buffer: BinaryIO, compressed: bool = False):
    packet_data = _read_len_prefixed(buffer)
    if compressed:
        packet_data = _uncompressed_packet_data(packet_data)

    return _make_packet(packet_data)
