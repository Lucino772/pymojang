from ...common.packet import BasePacket
from ...common.types import *
from .types import *

class SLPPingPacket(BasePacket):
    packet_id: int = VarInt(default=0x01)
    payload: int = BigEndianInt64()

class SLPPongPacket(BasePacket):
    packet_id: int = VarInt()
    payload: int = BigEndianInt64()