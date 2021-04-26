from ...common.packet import BasePacket
from ...common.types import *

class LoginRequestPacket(BasePacket):
    id: int = LittleEndianInt32()
    type: int = LittleEndianInt32(default=3)
    payload: str = NullTerminatedString()
    pad: int = Byte(default=0x00)

class LoginResponsePacket(BasePacket):
    id: int = LittleEndianInt32()
    type: int = LittleEndianInt32()
