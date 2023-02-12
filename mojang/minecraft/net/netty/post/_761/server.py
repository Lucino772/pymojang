import uuid
from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.types import (
    UUID,
    Bool,
    Bytes,
    Enum,
    Optional,
    Prefixed,
    String,
    UShort,
    VarInt,
)


# Handshaking
@dataclass
class Handshake(Packet):
    packet_id = 0

    protocol_version: int = field(metadata={"type": VarInt()})
    server_addr: str = field(metadata={"type": Prefixed(String(), VarInt())})
    server_port: int = field(metadata={"type": UShort()})
    next_state: int = field(metadata={"type": Enum(VarInt(), [1, 2])})


# Status
@dataclass
class StatusRequest(Packet):
    packet_id = 0


@dataclass
class PingRequest(Packet):
    packet_id = 1


# Login
@dataclass
class LoginStart(Packet):
    packet_id = 0

    name: str = field(metadata={"type": Prefixed(String(), VarInt())})
    has_uuid: bool = field(metadata={"type": Bool()})
    _uuid: uuid.UUID = field(metadata={"type": UUID()})


@dataclass
class EncryptionResponse(Packet):
    packet_id = 1

    shared_secret: bytes = field(
        metadata={"type": Prefixed(Bytes(), VarInt())}
    )
    verify_token: bytes = field(metadata={"type": Prefixed(Bytes(), VarInt())})


@dataclass
class LoginPluginResponse(Packet):
    packet_id = 2

    message_id: int = field(metadata={"type": VarInt()})
    successful: bool = field(metadata={"type": Bool()})
    data: bytes = field(
        metadata={
            "type": Optional(Bytes()),
            "present": lambda ctx: ctx["successful"]["value"],
            "len": lambda ctx: ctx["__len"],
        }
    )
