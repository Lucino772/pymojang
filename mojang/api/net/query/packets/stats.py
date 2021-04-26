from ...common.packet import BasePacket
from ...common.types import *
from .types import NullTerminatedStringList


class BasicStatsRequestPacket(BasePacket):
    magic: int = BigEndianShort(default=0xFEFD, signed=False)
    type: int = Byte(default=0)
    id: int = BigEndianInt32()
    token: int = BigEndianInt32()

class BasicStatsResponsePacket(BasePacket):
    type: int = Byte()
    id: int = BigEndianInt32()
    motd: str = NullTerminatedString()
    game_type: str = NullTerminatedString()
    map: str = NullTerminatedString()
    num_players: str = NullTerminatedString()
    max_players: str = NullTerminatedString()
    host_port: int = LittleEndianShort()
    host_ip: str = NullTerminatedString()


class FullStatsRequestPacket(BasePacket):
    magic: int = BigEndianShort(default=0xFEFD, signed=False)
    type: int = Byte(default=0)
    id: int = BigEndianInt32()
    token: int = BigEndianInt32()
    padding: int = BigEndianInt32(default=0xFFFFFF01, signed=False)

class FullStatsResponsePacket(BasePacket):
    type: int = Byte()
    id: int = BigEndianInt32()
    is_last_packet: int = Byte()
    # Padding
    _pad1: int = ArrayOf(Byte(), 10)
    # K.V Section
    _motd: str = NullTerminatedString()
    motd: str = NullTerminatedString()
    _game_type: str = NullTerminatedString()
    game_type: str = NullTerminatedString()
    _game_id: str = NullTerminatedString()
    game_id: str = NullTerminatedString()
    _version: str = NullTerminatedString()
    version: str = NullTerminatedString()
    _plugins: str = NullTerminatedString()
    plugins: str = NullTerminatedString()
    _map: str = NullTerminatedString()
    map: str = NullTerminatedString()
    _num_players: str = NullTerminatedString()
    num_players: str = NullTerminatedString()
    _max_players: str = NullTerminatedString()
    max_players: str = NullTerminatedString()
    _host_port: str = NullTerminatedString()
    host_port: str = NullTerminatedString()
    _host_ip: str = NullTerminatedString()
    host_ip: str = NullTerminatedString()
    # Padding
    _pad2: int = ArrayOf(Byte(), 11)
    # Players Section
    players: list = NullTerminatedStringList()
