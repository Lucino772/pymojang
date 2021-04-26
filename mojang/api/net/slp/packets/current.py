from ...common.packet import BasePacket
from ...common.types import *
from .types import *

class SLPCurrentHandshakePacket(BasePacket):
    packet_id: int = VarInt(default=0x00)
    proto_version: int = VarInt()
    server_address: str = String()
    server_port: int = BigEndianShort(signed=False)
    next_state: int = VarInt()

class SLPCurrentRequestPacket(BasePacket):
    packet_id: int = VarInt(default=0x00)

class SLPCurrentResponsePacket(BasePacket):
    packet_id: int = VarInt()
    response: dict = JSONString()
