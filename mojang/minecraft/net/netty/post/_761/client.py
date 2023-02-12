import typing as t
import uuid
from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.types import (
    UUID,
    Array,
    Bool,
    Bytes,
    Chat,
    Identifier,
    Long,
    Nested,
    Prefixed,
    String,
    VarInt,
)


# Status
@dataclass
class StatusResponse(Packet):
    packet_id = 0
    response: str = field(metadata={"type": Prefixed(String(), VarInt())})


@dataclass
class PingResponse(Packet):
    packet_id = 1
    payload: int = field(metadata={"type": Long()})


# Login
@dataclass
class Disconnect(Packet):
    packet_id = 0
    reason: t.Union[dict, list] = field(
        metadata={"type": Prefixed(Chat(), VarInt())}
    )


@dataclass
class EncryptionRequest(Packet):
    packet_id = 1

    server_id: str = field(metadata={"type": Prefixed(String(), VarInt())})
    public_key: bytes = field(metadata={"type": Prefixed(Bytes(), VarInt())})
    verify_token: bytes = field(metadata={"type": Prefixed(Bytes(), VarInt())})


@dataclass
class LoginSuccess(Packet):
    @dataclass
    class Property:
        name: str = field(metadata={"type": Prefixed(String(), VarInt())})
        value: str = field(metadata={"type": Prefixed(String(), VarInt())})
        is_signed: bool = field(metadata={"type": Bool()})
        # FIXME: Field signature must be optional
        signature: str = field(metadata={"type": Prefixed(String(), VarInt())})

    packet_id = 2

    _uuid: uuid.UUID = field(metadata={"type": UUID()})
    username: str = field(metadata={"type": Prefixed(String(), VarInt())})
    len_props: int = field(
        metadata={
            "type": VarInt(),
            "value": lambda ctx: len(ctx["properties"]["value"]),
        },
        init=False,
        default=-1,
    )
    properties: t.List[Property] = field(
        metadata={
            "type": Array(Nested(Property)),
            "len": lambda ctx: ctx["len_props"]["value"],
        }
    )


@dataclass
class SetCompression(Packet):
    packet_id = 3

    threshold: int = field(metadata={"type": VarInt()})


@dataclass
class LoginPluginRequest(Packet):
    packet_id = 4

    message_id: int = field(metadata={"type": VarInt()})
    channel: str = field(metadata={"type": Identifier()})
    # FIXME: The length of this array must be inferred from the packet length.
    data: bytes = field(metadata={"type": Bytes()})
