from ...common.packet import BasePacket
from ...common.types import *

class HandhakeRequestPacket(BasePacket):
    magic: int = BigEndianShort(default=0xFEFD, signed=False)
    type: int = Byte(default=9)
    id: int = BigEndianInt32()

class HandhakeResponsePacket(BasePacket):
    type: int = Byte()
    id: int = BigEndianInt32()
    token: str = NullTerminatedString()
