from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.types import Long


@dataclass
class PingResponse(Packet):
    packet_id = 0x01
    payload: int = field(metadata={"type": Long()})
