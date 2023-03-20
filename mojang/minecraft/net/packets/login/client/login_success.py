import typing as t
from dataclasses import dataclass, field
from uuid import UUID as _UUID

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.packets.types import _String
from mojang.minecraft.net.types import (
    UUID,
    Array,
    Bool,
    Nested,
    Optional,
    VarInt,
)


@dataclass
class LoginSuccess(Packet):
    @dataclass
    class Property:
        name: str = field(metadata={"type": _String})
        value: str = field(metadata={"type": _String})
        is_signed: bool = field(metadata={"type": Bool()})
        signature: str = field(
            metadata={
                "type": Optional(_String),
                "present": lambda ctx: ctx["is_signed"]["value"],
            }
        )

    packet_id = 0x02

    _uuid: _UUID = field(metadata={"type": UUID()})
    username: str = field(metadata={"type": _String})
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
