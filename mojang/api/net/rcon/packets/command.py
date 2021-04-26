from ...common.packet import BasePacket
from ...common.types import *

class CommandRequestPacket(BasePacket):
    id: int = LittleEndianInt32()
    type: int = LittleEndianInt32(default=2)
    payload: str = NullTerminatedString()
    pad: int = Byte(default=0x00)

class CommandResponsePacket(BasePacket):
    id: int = LittleEndianInt32()
    type: int = LittleEndianInt32()
    payload: str = NullTerminatedString()
    pad: int = Byte()
