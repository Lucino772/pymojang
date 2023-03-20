from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.packets.types import _String
from mojang.minecraft.net.types import Bytes, Prefixed, VarInt


@dataclass
class EncryptionRequest(Packet):
    packet_id = 0x01

    server_id: str = field(metadata={"type": _String})
    public_key: bytes = field(metadata={"type": Prefixed(Bytes(), VarInt())})
    verify_token: bytes = field(metadata={"type": Prefixed(Bytes(), VarInt())})
