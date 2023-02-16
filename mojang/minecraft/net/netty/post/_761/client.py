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
    Int,
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
    VarLong,
)

_String = Prefixed(String(), VarInt())
_Chat = Prefixed(Chat(), VarInt())
_Identifier = Prefixed(Identifier(), VarInt())
_Slot = Nested(Slot)
_BitSets = Prefixed(Array(Long()), VarInt())


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


@dataclass
class DisguisedChatMessage(Packet):
    packet_id = 24

    message: t.Union[dict, list] = field(metadata={"type": _Chat})
    chat_type: int = field(metadata={"type": VarInt()})
    chat_type_name: t.Union[dict, list] = field(metadata={"type": _Chat})
    has_target_name: bool = field(metadata={"type": Bool()})
    target_name: str = field(
        metadata={
            "type": Optional(_Chat),
            "present": lambda ctx: ctx["has_target_name"]["value"],
        }
    )


@dataclass
class EntityEvent(Packet):
    packet_id = 25

    entity_id: int = field(metadata={"type": Int()})
    entity_status: int = field(metadata={"type": Byte()})


@dataclass
class Explosion(Packet):
    packet_id = 26

    @dataclass
    class Record:
        x: int = field(metadata={"type": Byte()})
        y: int = field(metadata={"type": Byte()})
        z: int = field(metadata={"type": Byte()})

    x: float = field(metadata={"type": Double()})
    y: float = field(metadata={"type": Double()})
    z: float = field(metadata={"type": Double()})
    strength: float = field(metadata={"type": Float()})
    record_count: int = field(metadata={"type": VarInt()})
    records: t.List[Record] = field(
        metadata={
            "type": Array(Nested(Record)),
            "len": lambda ctx: ctx["record_count"]["value"],
        }
    )
    motion_x: float = field(metadata={"type": Float()})
    motion_y: float = field(metadata={"type": Float()})
    motion_z: float = field(metadata={"type": Float()})


@dataclass
class UnloadChunk(Packet):
    packet_id = 27

    chunk_x: int = field(metadata={"type": Int()})
    chunk_z: int = field(metadata={"type": Int()})


@dataclass
class GameEvent(Packet):
    packet_id = 28

    event: int = field(metadata={"type": UByte()})
    value: float = field(metadata={"type": Float()})


@dataclass
class OpenHorseScreen(Packet):
    packet_id = 29

    window_id: int = field(metadata={"type": UByte()})
    slot_cnt: int = field(metadata={"type": VarInt()})
    entity_id: int = field(metadata={"type": Int()})


@dataclass
class InitializeWorldBorder(Packet):
    packet_id = 30

    x: float = field(metadata={"type": Double()})
    z: float = field(metadata={"type": Double()})
    old_diameter: float = field(metadata={"type": Double()})
    new_diameter: float = field(metadata={"type": Double()})
    speed: int = field(metadata={"type": VarLong()})
    portal_teleport: int = field(metadata={"type": VarInt()})
    warn_blocks: int = field(metadata={"type": VarInt()})
    warn_time: int = field(metadata={"type": VarInt()})


@dataclass
class KeepAlive(Packet):
    packet_id = 31

    id: int = field(metadata={"type": Long()})


@dataclass
class ChunkDataUpdateLight(Packet):
    packet_id = 32

    @dataclass
    class BlockEntity:
        packed_xz: int = field(metadata={"type": Byte()})
        y: int = field(metadata={"type": Short()})
        type: int = field(metadata={"type": VarInt()})
        data: Tag = field(metadata={"type": NBT()})

    @dataclass
    class LightItem:
        length: int = field(metadata={"type": VarInt()})
        array: bytes = field(
            metadata={
                "type": Bytes(),
                "len": lambda ctx: ctx["length"]["value"],
            }
        )

    chunk_x: int = field(metadata={"type": Int()})
    chunk_z: int = field(metadata={"type": Int()})
    heightmaps: Tag = field(metadata={"type": NBT()})
    size: int = field(metadata={"type": VarInt()})
    data: bytes = field(
        metadata={"type": Bytes(), "len": lambda ctx: ctx["size"]["value"]}
    )
    block_entity_cnt: int = field(metadata={"type": VarInt()})
    block_entities: t.List[BlockEntity] = field(
        metadata={
            "type": Array(Nested(BlockEntity)),
            "len": lambda ctx: ctx["block_entity_cnt"]["value"],
        }
    )
    trust_edges: bool = field(metadata={"type": Bool()})
    sky_light_mask: t.List[int] = field(metadata={"type": _BitSets})
    block_light_mask: t.List[int] = field(metadata={"type": _BitSets})
    empty_sky_light_mask: t.List[int] = field(metadata={"type": _BitSets})
    empty_block_light_mask: t.List[int] = field(metadata={"type": _BitSets})
    sky_light_array_cnt: int = field(metadata={"type": VarInt()})
    sky_light_arrays: t.List[LightItem] = field(
        metadata={
            "type": Array(Nested(LightItem)),
            "len": lambda ctx: ctx["sky_light_array_cnt"]["value"],
        }
    )
    block_light_array_cnt: int = field(metadata={"type": VarInt()})
    block_light_arrays: t.List[LightItem] = field(
        metadata={
            "type": Array(Nested(LightItem)),
            "len": lambda ctx: ctx["block_light_array_cnt"]["value"],
        }
    )


@dataclass
class WorldEvent(Packet):
    packet_id = 33

    event: int = field(metadata={"type": Int()})
    location: t.Tuple[int, int, int] = field(metadata={"type": Position()})
    data: int = field(metadata={"type": Int()})
    disable_rel_volume: bool = field(metadata={"type": Bool()})


@dataclass
class Particle(Packet):
    packet_id = 34

    particle_id: int = field(metadata={"type": VarInt()})
    long_distance: int = field(metadata={"type": Bool()})
    x: float = field(metadata={"type": Double()})
    y: float = field(metadata={"type": Double()})
    z: float = field(metadata={"type": Double()})
    offset_x: float = field(metadata={"type": Float()})
    offset_y: float = field(metadata={"type": Float()})
    offset_z: float = field(metadata={"type": Float()})
    max_speed: float = field(metadata={"type": Float()})
    particle_cnt: int = field(metadata={"type": Int()})
    # TODO: Add data property


@dataclass
class UpdateLight(Packet):
    packet_id = 35

    @dataclass
    class LightItem:
        length: int = field(metadata={"type": VarInt()})
        array: bytes = field(
            metadata={
                "type": Bytes(),
                "len": lambda ctx: ctx["length"]["value"],
            }
        )

    chunk_x: int = field(metadata={"type": VarInt()})
    chunk_z: int = field(metadata={"type": VarInt()})
    trust_edges: bool = field(metadata={"type": Bool()})
    sky_light_mask: t.List[int] = field(metadata={"type": _BitSets})
    block_light_mask: t.List[int] = field(metadata={"type": _BitSets})
    empty_sky_light_mask: t.List[int] = field(metadata={"type": _BitSets})
    empty_block_light_mask: t.List[int] = field(metadata={"type": _BitSets})
    sky_light_array_cnt: int = field(metadata={"type": VarInt()})
    sky_light_arrays: t.List[LightItem] = field(
        metadata={
            "type": Array(Nested(LightItem)),
            "len": lambda ctx: ctx["sky_light_array_cnt"]["value"],
        }
    )
    block_light_array_cnt: int = field(metadata={"type": VarInt()})
    block_light_arrays: t.List[LightItem] = field(
        metadata={
            "type": Array(Nested(LightItem)),
            "len": lambda ctx: ctx["block_light_array_cnt"]["value"],
        }
    )


@dataclass
class Login(Packet):
    packet_id = 36

    entity_id: int = field(metadata={"type": Int()})
    is_hardcore: bool = field(metadata={"type": Bool()})
    gamemode: int = field(metadata={"type": UByte()})
    prev_gamemode: int = field(metadata={"type": Byte()})
    dim_count: int = field(metadata={"type": VarInt()})
    dim_names: t.List[str] = field(
        metadata={
            "type": Array(_Identifier),
            "len": lambda ctx: ctx["dim_count"]["value"],
        }
    )
    reg_codec: Tag = field(metadata={"type": NBT()})
    dim_type: str = field(metadata={"type": _Identifier})
    dim_name: str = field(metadata={"type": _Identifier})
    hashed_seed: int = field(metadata={"type": Long()})
    max_players: int = field(metadata={"type": VarInt()})
    view_distance: int = field(metadata={"type": VarInt()})
    sim_distance: int = field(metadata={"type": VarInt()})
    reduced_debug_info: bool = field(metadata={"type": Bool()})
    enable_respawn_screen: bool = field(metadata={"type": Bool()})
    is_debug: bool = field(metadata={"type": Bool()})
    is_flat: bool = field(metadata={"type": Bool()})
    has_death_location: bool = field(metadata={"type": Bool()})
    death_dim_name: str = field(
        metadata={
            "type": Optional(_Identifier),
            "present": lambda ctx: ctx["has_death_location"]["value"],
        }
    )
    death_location: str = field(
        metadata={
            "type": Optional(Position()),
            "present": lambda ctx: ctx["has_death_location"]["value"],
        }
    )


@dataclass
class MapData(Packet):
    packet_id = 37

    @dataclass
    class Icon:
        type: int = field(metadata={"type": VarInt()})
        x: int = field(metadata={"type": Byte()})
        z: int = field(metadata={"type": Byte()})
        direction: int = field(metadata={"type": Byte()})
        has_display_name: bool = field(metadata={"type": Bool()})
        display_name: str = field(
            metadata={
                "type": Optional(_Chat),
                "present": lambda ctx: ctx["has_display_name"]["value"],
            }
        )

    map_id: int = field(metadata={"type": VarInt()})
    scale: int = field(metadata={"type": Byte()})
    locked: bool = field(metadata={"type": Bool()})
    icon_cnt: int = field(metadata={"type": VarInt()})
    icons: t.List[Icon] = field(
        metadata={
            "type": Array(Nested(Icon)),
            "len": lambda ctx: ctx["icon_cnt"]["value"],
        }
    )
    columns: int = field(metadata={"type": UByte()})
    rows: int = field(
        metadata={
            "type": Optional(UByte()),
            "present": lambda ctx: ctx["columns"]["value"] > 0,
        }
    )
    x: int = field(
        metadata={
            "type": Optional(Byte()),
            "present": lambda ctx: ctx["columns"]["value"] > 0,
        }
    )
    z: int = field(
        metadata={
            "type": Optional(Byte()),
            "present": lambda ctx: ctx["columns"]["value"] > 0,
        }
    )
    length: int = field(
        metadata={
            "type": Optional(VarInt()),
            "present": lambda ctx: ctx["columns"]["value"] > 0,
        }
    )
    data: t.List[int] = field(
        metadata={
            "type": Array(UByte()),
            "len": lambda ctx: ctx["length"]["value"],
        }
    )
