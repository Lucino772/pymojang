from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.types import VarInt


@dataclass
class SetCompression(Packet):
    packet_id = 0x03

    threshold: int = field(metadata={"type": VarInt()})
