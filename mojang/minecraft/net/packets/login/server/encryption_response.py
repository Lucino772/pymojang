from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.types import Bytes, Prefixed, VarInt


@dataclass
class EncryptionResponse(Packet):
    packet_id = 0x01

    shared_secret: bytes = field(
        metadata={"type": Prefixed(Bytes(), VarInt())}
    )
    verify_token: bytes = field(metadata={"type": Prefixed(Bytes(), VarInt())})
