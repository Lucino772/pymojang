import typing as t
from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.packets.types import _Chat


@dataclass
class Disconnect(Packet):
    packet_id = 0
    reason: t.Union[dict, list] = field(metadata={"type": _Chat})
