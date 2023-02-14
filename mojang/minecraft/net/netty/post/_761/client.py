import typing as t
import uuid
from dataclasses import dataclass, field

from mojang.minecraft.net.packet import Packet
from mojang.minecraft.net.types import (
    NBT,
    UUID,
    Array,
    Bool,
    Byte,
    Bytes,
    Chat,
    Double,
    Enum,
    Float,
    Identifier,
    Long,
    Nested,
    Optional,
    Position,
    Prefixed,
    Short,
    Slot,
    String,
    Tag,
    UByte,
    VarInt,
)

_String = Prefixed(String(), VarInt())
_Chat = Prefixed(Chat(), VarInt())
_Identifier = Prefixed(Identifier(), VarInt())
_Slot = Nested(Slot)


# Status
@dataclass
class StatusResponse(Packet):
    packet_id = 0
    response: str = field(metadata={"type": _String})


@dataclass
class PingResponse(Packet):
    packet_id = 1
    payload: int = field(metadata={"type": Long()})


# Login
@dataclass
class Disconnect(Packet):
    packet_id = 0
    reason: t.Union[dict, list] = field(metadata={"type": _Chat})


@dataclass
class EncryptionRequest(Packet):
    packet_id = 1

    server_id: str = field(metadata={"type": _String})
    public_key: bytes = field(metadata={"type": Prefixed(Bytes(), VarInt())})
    verify_token: bytes = field(metadata={"type": Prefixed(Bytes(), VarInt())})


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

    packet_id = 2

    _uuid: uuid.UUID = field(metadata={"type": UUID()})
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


@dataclass
class SetCompression(Packet):
    packet_id = 3

    threshold: int = field(metadata={"type": VarInt()})


@dataclass
class LoginPluginRequest(Packet):
    packet_id = 4

    message_id: int = field(metadata={"type": VarInt()})
    channel: str = field(metadata={"type": _Identifier})
    data: bytes = field(
        metadata={"type": Bytes(), "len": lambda ctx: ctx["__len"]}
    )


# Play
@dataclass
class SpanEntity(Packet):
    packet_id = 0

    entity_id: int = field(metadata={"type": VarInt()})
    entity_uuid: uuid.UUID = field(metadata={"type": UUID()})
    type: int = field(metadata={"type": VarInt()})
    x: float = field(metadata={"type": Double()})
    y: float = field(metadata={"type": Double()})
    z: float = field(metadata={"type": Double()})
    pitch: int = field(metadata={"type": UByte()})
    yaw: int = field(metadata={"type": UByte()})
    head_yaw: int = field(metadata={"type": UByte()})
    data: int = field(metadata={"type": VarInt()})
    vel_x: int = field(metadata={"type": Short()})
    vel_y: int = field(metadata={"type": Short()})
    vel_z: int = field(metadata={"type": Short()})


@dataclass
class SpanExperiencOrb(Packet):
    packet_id = 1

    entity_id: int = field(metadata={"type": VarInt()})
    x: float = field(metadata={"type": Double()})
    y: float = field(metadata={"type": Double()})
    z: float = field(metadata={"type": Double()})
    count: int = field(metadata={"type": Short()})


@dataclass
class SpanwPlayer(Packet):
    packet_id = 2

    entity_id: int = field(metadata={"type": VarInt()})
    player_uuid: uuid.UUID = field(metadata={"type": UUID()})
    x: float = field(metadata={"type": Double()})
    y: float = field(metadata={"type": Double()})
    z: float = field(metadata={"type": Double()})
    yaw: int = field(metadata={"type": UByte()})
    pitch: int = field(metadata={"type": UByte()})


@dataclass
class EntityAnimation(Packet):
    packet_id = 3

    entity_id: int = field(metadata={"type": VarInt()})
    animation: int = field(metadata={"type": UByte()})


@dataclass
class AwardStatistics(Packet):
    packet_id = 4

    @dataclass
    class StatisticItem:
        cat_id: int = field(metadata={"type": VarInt()})
        stat_id: int = field(metadata={"type": VarInt()})
        value: int = field(metadata={"type": VarInt()})

    count: int = field(metadata={"type": VarInt()})
    statistics: t.List[StatisticItem] = field(
        metadata={
            "type": Array(Nested(StatisticItem)),
            "len": lambda ctx: ctx["count"]["value"],
        }
    )


@dataclass
class AcknowledgeBlockChange(Packet):
    packet_id = 5

    seq_id: int = field(metadata={"type": VarInt()})


@dataclass
class SetBlockDestroyStage(Packet):
    packet_id = 6

    entity_id: int = field(metadata={"type": VarInt()})
    location: t.Tuple[int, int, int] = field(metadata={"type": Position()})
    stage: int = field(metadata={"type": Byte()})


@dataclass
class BlockEntityData(Packet):
    packet_id = 7

    location: t.Tuple[int, int, int] = field(metadata={"type": Position()})
    type: int = field(metadata={"type": VarInt()})
    nbt_data: Tag = field(metadata={"type": NBT()})


@dataclass
class BlockAction(Packet):
    packet_id = 8

    location: t.Tuple[int, int, int] = field(metadata={"type": Position()})
    action_id: int = field(metadata={"type": UByte()})
    action_param: int = field(metadata={"type": UByte()})
    block_type: int = field(metadata={"type": VarInt()})


@dataclass
class BlockUpdate(Packet):
    packet_id = 9

    location: t.Tuple[int, int, int] = field(metadata={"type": Position()})
    block_id: int = field(metadata={"type": VarInt()})


@dataclass
class BossBar(Packet):
    packet_id = 10

    _uuid: uuid.UUID = field(metadata={"type": UUID()})
    action: int = field(metadata={"type": VarInt()})

    title: t.Union[dict, list] = field(
        metadata={
            "type": Optional(_Chat),
            "present": lambda ctx: ctx["action"] in [0, 3],
        }
    )
    health: float = field(
        metadata={
            "type": Optional(Float()),
            "present": lambda ctx: ctx["action"] in [0, 2],
        }
    )
    color: int = field(
        metadata={
            "type": Optional(VarInt()),
            "present": lambda ctx: ctx["action"] in [0, 4],
        }
    )
    division: int = field(
        metadata={
            "type": Optional(VarInt()),
            "present": lambda ctx: ctx["action"] in [0, 4],
        }
    )
    flags: int = field(
        metadata={
            "type": Optional(UByte()),
            "present": lambda ctx: ctx["action"] in [0, 5],
        }
    )


@dataclass
class ChangeDifficulty(Packet):
    packet_id = 11

    difficulty: int = field(metadata={"type": UByte()})
    locked: bool = field(metadata={"type": Bool()})


@dataclass
class ClearTitles(Packet):
    packet_id = 12

    reset: bool = field(metadata={"type": Bool()})


@dataclass
class CommandSuggestionsResponse(Packet):
    packet_id = 13

    @dataclass
    class Match:
        match: str = field(metadata={"type": _String})
        has_tooltip: bool = field(metadata={"type": Bool()})
        tooltip: t.Union[dict, list] = field(
            metadata={
                "type": Optional(_Chat),
                "present": lambda ctx: ctx["has_tooltip"]["value"],
            }
        )

    id: int = field(metadata={"type": VarInt()})
    start: int = field(metadata={"type": VarInt()})
    length: int = field(metadata={"type": VarInt()})
    count: int = field(metadata={"type": VarInt()})
    matches: t.List[Match] = field(
        metadata={
            "type": Array(Nested(Match)),
            "len": lambda ctx: ctx["count"]["value"],
        }
    )


@dataclass
class Commands(Packet):
    packet_id = 14

    @dataclass
    class Node:
        flags: int = field(metadata={"type": Byte()})
        count: int = field(metadata={"type": VarInt()})
        children: t.List[int] = field(
            metadata={
                "type": Array(VarInt()),
                "len": lambda ctx: ctx["count"]["value"],
            }
        )

        redirect_node: int = field(
            metadata={
                "type": Optional(VarInt()),
                "present": lambda ctx: ctx["flags"]["value"] == 0x80,
            }
        )
        name: str = field(
            metadata={
                "type": Optional(_String),
                "present": lambda ctx: ctx["flags"]["value"] & 0b11 > 1,
            }
        )
        parser_id: int = field(
            metadata={
                "type": Optional(VarInt()),
                "present": lambda ctx: ctx["flags"]["value"] & 0b10 == 1,
            }
        )
        # TODO: properties: t.Any = field(...)
        suggest_type: str = field(metadata={"type": _Identifier})

    count: int = field(metadata={"type": VarInt()})
    nodes: t.List[Node] = field(
        metadata={
            "type": Array(Nested(Node)),
            "len": lambda ctx: ctx["count"]["value"],
        }
    )
    root_index: int = field(metadata={"type": VarInt()})


@dataclass
class CloseContainer(Packet):
    packet_id = 15

    window_id: int = field(metadata={"type": UByte()})


@dataclass
class SetContainerContent(Packet):
    packet_id = 16

    window_id: int = field(metadata={"type": UByte()})
    state_id: int = field(metadata={"type": VarInt()})
    count: int = field(metadata={"type": VarInt()})
    slots: t.List[Slot] = field(
        metadata={
            "type": Array(_Slot),
            "len": lambda ctx: ctx["count"]["value"],
        }
    )
    carried: Slot = field(metadata={"type": _Slot})


@dataclass
class SetContainerProperty(Packet):
    packet_id = 17

    window_id: int = field(metadata={"type": UByte()})
    property: int = field(metadata={"type": Short()})
    value: int = field(metadata={"type": Short()})


@dataclass
class SetContainerSlot(Packet):
    packet_id = 18

    window_id: int = field(metadata={"type": UByte()})
    state_id: int = field(metadata={"type": VarInt()})
    slot_id: int = field(metadata={"type": Short()})
    slot: Slot = field(metadata={"type": _Slot})


@dataclass
class SetCooldown(Packet):
    packet_id = 19

    item_id: int = field(metadata={"type": VarInt()})
    cooldown_ticks: int = field(metadata={"type": VarInt()})


@dataclass
class ChatSuggestions(Packet):
    packet_id = 20

    action: int = field(metadata={"type": Enum(VarInt(), [0, 1, 2])})
    count: int = field(metadata={"type": VarInt()})
    entries: t.List[str] = field(
        metadata={
            "type": Array(_String),
            "len": lambda ctx: ctx["count"]["value"],
        }
    )


@dataclass
class PluginMessage(Packet):
    packet_id = 21

    channel: str = field(metadata={"type": _Identifier})
    data: bytes = field(
        metadata={
            "type": Bytes(),
            "len": lambda ctx: ctx["__len"] - ctx["channel"]["len"],
        }
    )


@dataclass
class DeleteMessage(Packet):
    packet_id = 22

    sig_len: int = field(metadata={"type": VarInt()})
    signature: bytes = field(
        metadata={"type": Bytes(), "len": lambda ctx: ctx["sig_len"]["value"]}
    )


@dataclass
class DisconnectPlay(Packet):
    packet_id = 23

    reason: t.Union[dict, list] = field(metadata={"type": _Chat})
