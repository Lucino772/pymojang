from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.packets.types import _String


@dataclass
class StatusResponse(Packet):
    packet_id = 0x00
    response: str = field(metadata={"type": _String})
