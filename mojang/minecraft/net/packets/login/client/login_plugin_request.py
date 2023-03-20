from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.packets.types import _Identifier
from mojang.minecraft.net.types import Bytes, VarInt


@dataclass
class LoginPluginRequest(Packet):
    packet_id = 0x04

    message_id: int = field(metadata={"type": VarInt()})
    channel: str = field(metadata={"type": _Identifier})
    data: bytes = field(
        metadata={"type": Bytes(), "len": lambda ctx: ctx["__len"]}
    )
