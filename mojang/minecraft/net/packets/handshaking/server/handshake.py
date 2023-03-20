from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.packets.types import _String
from mojang.minecraft.net.types import Enum, UShort, VarInt


@dataclass
class Handshake(Packet):
    packet_id = 0x00

    protocol_version: int = field(metadata={"type": VarInt()})
    server_addr: str = field(metadata={"type": _String})
    server_port: int = field(metadata={"type": UShort()})
    next_state: int = field(metadata={"type": Enum(VarInt(), [1, 2])})
