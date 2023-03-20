from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.types import Bool, Bytes, Optional, VarInt


@dataclass
class LoginPluginResponse(Packet):
    packet_id = 0x02

    message_id: int = field(metadata={"type": VarInt()})
    successful: bool = field(metadata={"type": Bool()})
    data: bytes = field(
        metadata={
            "type": Optional(Bytes()),
            "present": lambda ctx: ctx["successful"]["value"],
            "len": lambda ctx: ctx["__len"],
        }
    )
