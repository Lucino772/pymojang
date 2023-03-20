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


@dataclass
class MerchantOffers(Packet):
    packet_id = 38

    @dataclass
    class Trade:
        input_item1: Slot = field(metadata={"type": _Slot})
        output_item: Slot = field(metadata={"type": _Slot})
        input_item2: Slot = field(metadata={"type": _Slot})
        trade_disabled: bool = field(metadata={"type": Bool()})
        trade_uses: int = field(metadata={"type": Int()})
        max_trade_uses: int = field(metadata={"type": Int()})
        xp: int = field(metadata={"type": Int()})
        special_price: int = field(metadata={"type": Int()})
        price_multiplier: float = field(metadata={"type": Float()})
        demand: int = field(metadata={"type": Int()})

    window_id: int = field(metadata={"type": VarInt()})
    size: int = field(metadata={"type": VarInt()})
    trades: t.List[Trade] = field(
        metadata={
            "type": Array(Nested(Trade)),
            "length": lambda ctx: ctx["size"]["value"],
        }
    )
    villager_level: int = field(metadata={"type": VarInt()})
    experience: int = field(metadata={"type": VarInt()})
    is_regular_villager: bool = field(metadata={"type": Bool()})
    can_restock: bool = field(metadata={"type": Bool()})


@dataclass
class UpdateEntityPosition(Packet):
    packet_id = 39

    entity_id: int = field(metadata={"type": VarInt()})
    delta_x: int = field(metadata={"type": Short()})
    delta_y: int = field(metadata={"type": Short()})
    delta_z: int = field(metadata={"type": Short()})
    on_ground: bool = field(metadata={"type": Bool()})


@dataclass
class UpdateEntityPositionAndRotation(Packet):
    packet_id = 0x28

    entity_id: int = field(metadata={"type": VarInt()})
    delta_x: int = field(metadata={"type": Short()})
    delta_y: int = field(metadata={"type": Short()})
    delta_z: int = field(metadata={"type": Short()})
    yaw: int = field(metadata={"type": UByte()})
    pitch: int = field(metadata={"type": UByte()})
    on_ground: bool = field(metadata={"type": Bool()})


@dataclass
class UpdateEntityRotation(Packet):
    packet_id = 0x29

    entity_id: int = field(metadata={"type": VarInt()})
    yaw: int = field(metadata={"type": UByte()})
    pitch: int = field(metadata={"type": UByte()})
    on_ground: bool = field(metadata={"type": Bool()})


@dataclass
class MoveVehicle(Packet):
    packet_id = 0x2A

    x: float = field(metadata={"type": Double()})
    y: float = field(metadata={"type": Double()})
    z: float = field(metadata={"type": Double()})
    yaw: int = field(metadata={"type": UByte()})
    pitch: int = field(metadata={"type": UByte()})


@dataclass
class OpenBook(Packet):
    packet_id = 0x2B

    hand: int = field(metadata={"type": Enum(VarInt(), [0, 1])})


@dataclass
class OpenScreen(Packet):
    packet_id = 0x2C

    window_id: int = field(metadata={"type": VarInt()})
    window_type: int = field(metadata={"type": VarInt()})
    window_title: t.Union[list, dict] = field(metadata={"type": _Chat})


@dataclass
class OpenSignEditor(Packet):
    packet_id = 0x2D

    location: t.Tuple[int, int, int] = field(metadata={"type": Position()})


@dataclass
class Ping(Packet):
    packet_id = 0x2E

    id: int = field(metadata={"type": Int()})


@dataclass
class PlaceChostRecipe(Packet):
    packet_id = 0x2F

    window_id: int = field(metadata={"type": Byte()})
    recipe: str = field(metadata={"type": _Identifier})


@dataclass
class PlayerAbilities(Packet):
    packet_id = 0x30

    flags: int = field(metadata={"type": Byte()})
    flying_speed: float = field(metadata={"type": Float()})
    fov_modifier: float = field(metadata={"type": Float()})


@dataclass
class PlayerChatMessage(Packet):
    packet_id = 0x31

    # header
    sender: uuid.UUID = field(metadata={"type": UUID()})
    index: int = field(metadata={"type": VarInt()})
    signature_present: bool = field(metadata={"type": Bool()})
    signature_bytes: bytes = field(
        metadata={
            "type": Optional(Bytes()),
            "present": lambda ctx: ctx["signature_present"]["value"],
        }
    )

    # body
    message: str = field(metadata={"type": _String})
    timestamp: int = field(metadata={"type": Long()})
    salt: int = field(metadata={"type": Long()})

    # prev. message
    total_prev_msgs: int = field(metadata={"type": VarInt()})
    prev_msgs_sigs: t.List[bytes] = field(
        metadata={
            "type": Array(Prefixed(Bytes(), VarInt())),
            "length": lambda ctx: ctx["total_prev_msgs"]["value"],
        }
    )

    # other
    unsigned_content_present: bool = field(metadata={"type": Bool()})
    unsigned_content: t.Union[list, dict] = field(
        metadata={
            "type": Optional(_Chat),
            "present": lambda ctx: ctx["unsigned_content_present"]["value"],
        }
    )
    filter_type: int = field(metadata={"type": VarInt()})
    filter_type_bits: t.List[int] = field(metadata={"type": _BitSets})

    # net. target
    chat_type: int = field(metadata={"type": VarInt()})
    net_name: t.Union[list, dict] = field(metadata={"type": _Chat})
    net_target_name_present: bool = field(metadata={"type": Bool()})
    net_target_name: t.Union[list, dict] = field(
        metadata={
            "type": Optional(_Chat),
            "present": lambda ctx: ctx["net_target_name_present"]["value"],
        }
    )


@dataclass
class EndCombat(Packet):
    packet_id = 0x32

    duration: int = field(metadata={"type": VarInt()})
    entity_id: int = field(metadata={"type": Int()})


@dataclass
class EnterCombat(Packet):
    packet_id = 0x33


@dataclass
class CombatDeath(Packet):
    packet_id = 0x34

    player_id: int = field(metadata={"type": VarInt()})
    entity_id: int = field(metadata={"type": Int()})
    message: t.Union[list, dict] = field(metadata={"type": _Chat})


@dataclass
class PlayerInfoRemove(Packet):
    packet_id = 0x35

    nb_players: int = field(metadata={"type": VarInt()})
    players: t.List[uuid.UUID] = field(
        metadata={
            "type": Array(UUID()),
            "length": lambda ctx: ctx["nb_players"]["value"],
        }
    )


@dataclass
class PlayerInfoUpdate(Packet):
    packet_id = 0x36

    @dataclass
    class _Action:
        _uuid: uuid.UUID = field(metadata={"type": UUID()})

    @dataclass
    class Action_AddPlayer(_Action):
        @dataclass
        class Property:
            name: str = field(metadata={"type": _String})
            value: str = field(metadata={"type": _String})
            signed: bool = field(metadata={"type": Bool()})
            signature: str = field(
                metadata={
                    "type": Optional(_String),
                    "present": lambda ctx: ctx["signed"]["value"],
                }
            )

        name: str = field(metadata={"type": _String})
        properties: t.List[Property] = field(
            metadata={"type": Prefixed(Array(Nested(Property)), VarInt())}
        )

    @dataclass
    class Action_InitChat(_Action):
        has_sig_data: bool = field(metadata={"type": Bool()})
        chat_sess_id: uuid.UUID = field(
            metadata={
                "type": Optional(UUID()),
                "present": lambda ctx: ctx["has_sig_data"]["value"],
            }
        )
        public_key_exp_time: int = field(
            metadata={
                "type": Optional(Long()),
                "present": lambda ctx: ctx["has_sig_data"]["value"],
            }
        )
        encoded_public_key: bytes = field(
            metadata={
                "type": Optional(Prefixed(Bytes(), VarInt())),
                "present": lambda ctx: ctx["has_sig_data"]["value"],
            }
        )
        public_key_sig: bytes = field(
            metadata={
                "type": Optional(Prefixed(Bytes(), VarInt())),
                "present": lambda ctx: ctx["has_sig_data"]["value"],
            }
        )

    @dataclass
    class Action_UpdateGamemode(_Action):
        gamemode: int = field(metadata={"type": VarInt()})

    @dataclass
    class Action_UpdateListed(_Action):
        listed: bool = field(metadata={"type": Bool()})

    @dataclass
    class Action_UpdateLatency(_Action):
        ping: int = field(metadata={"type": VarInt()})

    @dataclass
    class Action_UpdateDisplayName:
        has_display_name: bool = field(metadata={"type": Bool()})
        display_name: t.Union[list, dict] = field(
            metadata={
                "type": Optional(_Chat),
                "present": lambda ctx: ctx["has_display_name"]["value"],
            }
        )

    actions: int = field(metadata={"type": Byte()})
    # TODO: Actions List


@dataclass
class LookAt(Packet):
    packet_id = 0x37

    feet_eyes: int = field(metadata={"type": Enum(VarInt(), [0, 1])})
    target_x: int = field(metadata={"type": Double()})
    target_y: int = field(metadata={"type": Double()})
    target_z: int = field(metadata={"type": Double()})
    is_entity: bool = field(metadata={"type": Bool()})
    entity_id: int = field(
        metadata={
            "type": Optional(VarInt()),
            "present": lambda ctx: ctx["is_entity"]["value"],
        }
    )
    entity_feet_eyes: int = field(
        metadata={
            "type": Optional(Enum(VarInt(), [0, 1])),
            "present": lambda ctx: ctx["is_entity"]["value"],
        }
    )


@dataclass
class SynchronizePlayerPosition(Packet):
    packet_id = 0x38

    x: float = field(metadata={"type": Double()})
    y: float = field(metadata={"type": Double()})
    z: float = field(metadata={"type": Double()})
    yaw: float = field(metadata={"type": Float()})
    pitch: float = field(metadata={"type": Float()})
    flags: int = field(metadata={"type": Byte()})
    teleport_id: int = field(metadata={"type": VarInt()})
    dismount_vehicle: bool = field(metadata={"type": Bool()})


@dataclass
class UpdateRecipeBook(Packet):
    packet_id = 0x39

    action: int = field(metadata={"type": VarInt()})
    crafting_recipe_book_open: bool = field(metadata={"type": Bool()})
    crafting_recipe_book_filter_active: bool = field(metadata={"type": Bool()})
    smelting_recipe_book_open: bool = field(metadata={"type": Bool()})
    smelting_recipe_book_filter_active: bool = field(metadata={"type": Bool()})
    blast_furnace_recipe_book_open: bool = field(metadata={"type": Bool()})
    blast_furnace_recipe_book_filter_active: bool = field(
        metadata={"type": Bool()}
    )
    smoker_recipe_book_open: bool = field(metadata={"type": Bool()})
    smoker_recipe_book_filter_active: bool = field(metadata={"type": Bool()})
    recipe_ids1: t.List[str] = field(
        metadata={"type": Prefixed(Array(_Identifier), VarInt())}
    )
    recipe_ids2: t.List[str] = field(
        metadata={
            "type": Optional(Prefixed(Array(_Identifier), VarInt())),
            "present": lambda ctx: ctx["action"]["value"] == 0,
        }
    )


@dataclass
class RemoveEntities(Packet):
    packet_id = 0x3A

    entity_ids: t.List[int] = field(
        metadata={"type": Prefixed(Array(VarInt()), VarInt())}
    )


@dataclass
class RemoveEntityEffect(Packet):
    packet_id = 0x3B

    entity_id: int = field(metadata={"type": VarInt()})
    effect_id: int = field(metadata={"type": VarInt()})


@dataclass
class ResourcePack(Packet):
    packet_id = 0x3C

    url: str = field(metadata={"type": _String})
    hash: str = field(metadata={"type": _String})
    forced: bool = field(metadata={"type": Bool()})
    has_prompt_message: bool = field(metadata={"type": Bool()})
    prompt_message: t.Union[list, dict] = field(
        metadata={
            "type": Optional(_Chat),
            "present": lambda ctx: ctx["has_prompt_message"]["value"],
        }
    )


@dataclass
class Respawn(Packet):
    packet_id = 0x3D

    dim_type: str = field(metadata={"type": _Identifier})
    dim_name: str = field(metadata={"type": _Identifier})
    hashed_seed: int = field(metadata={"type": Long()})
    gamemode: int = field(metadata={"type": UByte()})
    prev_gamemode: int = field(metadata={"type": Byte()})
    is_debug: bool = field(metadata={"type": Bool()})
    is_flat: bool = field(metadata={"type": Bool()})
    copy_metadata: bool = field(metadata={"type": Bool()})
    has_death_location: bool = field(metadata={"type": Bool()})
    death_dim_name: str = field(
        metadata={
            "type": Optional(_Identifier),
            "present": lambda ctx: ctx["has_death_location"]["value"],
        }
    )
    death_location: t.Tuple[int, int, int] = field(
        metadata={
            "type": Optional(Position()),
            "present": lambda ctx: ctx["has_death_location"]["value"],
        }
    )


@dataclass
class SetHeadRotation(Packet):
    packet_id = 0x3E

    entity_id: int = field(metadata={"type": VarInt()})
    head_yaw: int = field(metadata={"type": UByte()})


@dataclass
class UpdateSectionBlocks(Packet):
    packet_id = 0x3F

    chunk_section_pos: int = field(metadata={"type": Long()})
    suppress_ligh_updates: bool = field(metadata={"type": Bool()})
    blocks: t.List[int] = field(
        metadata={"type": Prefixed(Array(Long()), VarInt())}
    )
