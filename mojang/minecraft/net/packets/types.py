from mojang.minecraft.net.types import (
    Array,
    Chat,
    Identifier,
    Long,
    Nested,
    Prefixed,
    Slot,
    String,
    VarInt,
)

_String = Prefixed(String(), VarInt())
_Chat = Prefixed(Chat(), VarInt())
_Identifier = Prefixed(Identifier(), VarInt())
_Slot = Nested(Slot)
_BitSets = Prefixed(Array(Long()), VarInt())
