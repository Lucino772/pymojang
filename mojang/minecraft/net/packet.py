import io
import typing as t
import zlib
from dataclasses import dataclass, field

from mojang.minecraft.net.types import Bytes, Nested, VarInt

T = t.TypeVar("T", bound="Packet")


@dataclass
class Packet:
    packet_id: t.ClassVar[int] = -1


@dataclass
class _PacketStruct:
    packet_id: int = field(metadata={"type": VarInt()})
    # FIXME: Length is inferred by packet length
    data: bytes = field(metadata={"type": Bytes()})


def _write_packet_struct(buffer: t.BinaryIO, value: Packet) -> int:
    with io.BytesIO() as temp:
        Nested(value.__class__).write(temp, value)
        _bytes = temp.getvalue()

    return Nested(_PacketStruct).write(
        buffer, _PacketStruct(value.packet_id, _bytes)
    )


def write_packet(
    buffer: t.BinaryIO, packet: T, compress: bool = False, threshold: int = -1
):
    with io.BytesIO() as temp:
        _write_packet_struct(temp, packet)
        packet_bytes = temp.getvalue()

    nbytes = 0
    if not compress:
        nbytes += VarInt().write(buffer, len(packet_bytes))
        nbytes += buffer.write(packet_bytes)
    else:
        if len(packet_bytes) < threshold:
            compressed_bytes = packet_bytes
            datalen = 0
        else:
            compressed_bytes = zlib.compress(packet_bytes)
            datalen = len(packet_bytes)

        nbytes += VarInt().write(buffer, len(compressed_bytes))
        nbytes += VarInt().write(buffer, datalen)
        nbytes += buffer.write(compressed_bytes)

    return nbytes


def read_packet(buffer: t.BinaryIO, compress: bool = False) -> _PacketStruct:
    packet_len = VarInt().read(buffer)

    if not compress:
        packet_bytes = buffer.read(packet_len)
    else:
        datalen = VarInt().read(buffer)
        if datalen == 0:
            packet_bytes = buffer.read(packet_len)
        else:
            compressed_bytes = buffer.read(packet_len)
            packet_bytes = zlib.decompress(compressed_bytes)

    with io.BytesIO(packet_bytes) as temp:
        return Nested(_PacketStruct).read(temp, len=len(packet_bytes))
