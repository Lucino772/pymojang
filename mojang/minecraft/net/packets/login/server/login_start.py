from dataclasses import dataclass, field
from uuid import UUID as _UUID

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.packets.types import _String
from mojang.minecraft.net.types import UUID, Bool


@dataclass
class LoginStart(Packet):
    packet_id = 0x00

    name: str = field(metadata={"type": _String})
    has_uuid: bool = field(metadata={"type": Bool()})
    uuid: _UUID = field(metadata={"type": UUID()})
