from __future__ import annotations

import ctypes
import io
import json
import re
import struct
import typing as t
import uuid
from dataclasses import dataclass, field, fields

T = t.TypeVar("T")


class _Type(t.Generic[T]):
    def write(self, buffer: t.BinaryIO, value: T, **kwds) -> int:
        raise NotImplementedError

    def read(self, buffer: t.BinaryIO, **kwds) -> T:
        raise NotImplementedError


class _PyStructType(_Type[T]):
    def __init__(self, __fmt: str) -> None:
        super().__init__()
        self.__fmt = struct.Struct(__fmt)

    def write(self, buffer: t.BinaryIO, value: T, **kwds) -> int:
        _bytes = self.__fmt.pack(value)
        return buffer.write(_bytes)

    def read(self, buffer: t.BinaryIO, **kwds) -> T:
        _bytes = buffer.read(self.__fmt.size)
        return self.__fmt.unpack(_bytes)[0]


class _ByteArray(_Type[T]):
    def __init__(self, max_len: int = -1) -> None:
        super().__init__()
        self.__max_len = max_len

    def encode(self, value: T) -> bytes:
        raise NotImplementedError

    def decode(self, value: bytes) -> T:
        raise NotImplementedError

    def write(self, buffer: t.BinaryIO, value: T, **kwds) -> int:
        _bytes = self.encode(value)
        if self.__max_len > 0 and len(_bytes) >= self.__max_len:
            raise RuntimeError(
                "Got length {}, max len is {}".format(
                    len(_bytes), self.__max_len
                )
            )
        return buffer.write(_bytes)

    def read(self, buffer: t.BinaryIO, len: int = -1, **kwds) -> T:
        if self.__max_len > 0 and len >= self.__max_len:
            raise RuntimeError(
                "Got length {}, max len is {}".format(len, self.__max_len)
            )
        _bytes = buffer.read(len)
        return self.decode(_bytes)


class _VarNumType(_Type[int]):
    def __init__(self, length: int, intXX_t, uintXX_t) -> None:
        self.__length = length
        self.__ctype_u = intXX_t
        self.__ctype_i = uintXX_t

    def write(self, buffer: t.BinaryIO, value: int, **kwds) -> int:
        value = self.__ctype_u(value).value
        written = 0
        while True and written <= self.__length:
            byte = value & 0x7F
            value >>= 7

            if value > 0:
                byte |= 0x80

            written += UByte().write(buffer, byte)

            if value == 0:
                break

        return written

    def read(self, buffer: t.BinaryIO, **kwds) -> int:
        val = 0

        for i in range(self.__length):
            byte = UByte().read(buffer)

            val |= (byte & 0x7F) << (7 * i)

            if byte & 0x80 == 0:
                break

        return self.__ctype_i(val).value


# Utils
class Prefixed(_Type[T]):
    def __init__(self, _type: _Type[T], _prefix_t: _Type[int]) -> None:
        super().__init__()
        self.__type = _type
        self.__prefix_t = _prefix_t

    def write(self, buffer: t.BinaryIO, value: T, **kwds) -> int:
        with io.BytesIO() as temp:
            _len = self.__type.write(temp, value, **kwds)
            _bytes = temp.getvalue()

        nbytes = self.__prefix_t.write(buffer, _len)
        nbytes += buffer.write(_bytes)
        return nbytes

    def read(self, buffer: t.BinaryIO, **kwds) -> T:
        _len = self.__prefix_t.read(buffer)
        return self.__type.read(buffer, len=_len, **kwds)


class Optional(_Type[t.Optional[T]]):
    def __init__(self, _type: _Type[T]) -> None:
        super().__init__()
        self.__type = _type

    def write(
        self,
        buffer: t.BinaryIO,
        value: t.Optional[T],
        present: bool = True,
        **kwds,
    ) -> int:
        if present:
            return self.__type.write(buffer, t.cast(T, value), **kwds)

        return 0

    def read(
        self, buffer: t.BinaryIO, present: bool = True, **kwds
    ) -> t.Optional[T]:
        if present:
            return self.__type.read(buffer, **kwds)

        return None


class Enum(_Type[T]):
    def __init__(self, _type: _Type[T], values: t.Sequence[T]) -> None:
        super().__init__()
        self.__type = _type
        self.__values = values

    def _check(self, value: T):
        if value not in self.__values:
            raise RuntimeError(
                "Value '{}' not in expected values {}".format(
                    value, self.__values
                )
            )

        return value

    def write(self, buffer: t.BinaryIO, value: T, **kwds) -> int:
        return self.__type.write(buffer, self._check(value), **kwds)

    def read(self, buffer: t.BinaryIO, **kwds) -> T:
        return self._check(self.__type.read(buffer, **kwds))


class Array(_Type[t.Sequence[T]]):
    def __init__(self, _item_t: _Type[T]) -> None:
        super().__init__()
        self.__item_t = _item_t

    def write(self, buffer: t.BinaryIO, value: t.Sequence[T], **kwds) -> int:
        for val in value:
            self.__item_t.write(buffer, val, **kwds)

        return len(value)

    def read(self, buffer: t.BinaryIO, len: int = -1, **kwds) -> t.Sequence[T]:
        return [self.__item_t.read(buffer, **kwds) for _ in range(len)]


# Types
class Bytes(_ByteArray[bytes]):
    def encode(self, value: bytes) -> bytes:
        return value

    def decode(self, value: bytes) -> bytes:
        return value


class String(_ByteArray[str]):
    def __init__(self, encoding: str = "utf-8") -> None:
        super().__init__(max_len=32767)
        self.__encoding = encoding

    def encode(self, value: str) -> bytes:
        return value.encode(self.__encoding)

    def decode(self, value: bytes) -> str:
        return value.decode(self.__encoding)


class Identifier(String):
    def _check(self, value: str):
        results = re.fullmatch("(([a-z0-9.-_]*):)?([a-z0-9.-_/]*)", value)
        if results is None:
            raise RuntimeError("Identifier is not valid: {}".format(value))

        namespace = results.group(2)
        if namespace is None or namespace == "":
            return f"minecraft:{value}"

        return value

    def encode(self, value: str) -> bytes:
        return super().encode(self._check(value))

    def decode(self, value: bytes) -> str:
        return self._check(super().decode(value))


class Chat(_ByteArray[t.Union[list, dict]]):
    def __init__(self, encoding: str = "utf-8") -> None:
        super().__init__(max_len=262144)
        self.__encoding = encoding

    def encode(self, value: t.Union[list, dict]) -> bytes:
        return json.dumps(value).encode(self.__encoding)

    def decode(self, value: bytes) -> t.Union[list, dict]:
        return json.loads(value.decode("utf-8"))


class UUID(_ByteArray[uuid.UUID]):
    def encode(self, value: uuid.UUID) -> bytes:
        return value.bytes

    def decode(self, value: bytes) -> uuid.UUID:
        return uuid.UUID(bytes=value)

    def read(self, buffer: t.BinaryIO, len: int = 16, **kwds) -> uuid.UUID:
        return super().read(buffer, 16, **kwds)


VarInt = lambda: _VarNumType(5, ctypes.c_int32, ctypes.c_uint32)
VarLong = lambda: _VarNumType(10, ctypes.c_int64, ctypes.c_uint64)

Byte = lambda: _PyStructType[int](">b")
UByte = lambda: _PyStructType[int](">B")
Short = lambda: _PyStructType[int](">h")
UShort = lambda: _PyStructType[int](">H")
Int = lambda: _PyStructType[int](">i")
UInt = lambda: _PyStructType[int](">I")
Long = lambda: _PyStructType[int](">q")
ULong = lambda: _PyStructType[int](">Q")

Float = lambda: _PyStructType[float](">f")
Double = lambda: _PyStructType[float](">d")

Bool = lambda: _PyStructType[bool](">?")


# NBT
class _TagType(_Type[T]):
    tag_id: int


def _with_tag_id(data_t: _Type[T], tag_id: int) -> _TagType[T]:
    setattr(data_t, "tag_id", tag_id)
    return t.cast(_TagType[T], data_t)


TagByte = _with_tag_id(Byte(), 1)
TagShort = _with_tag_id(Short(), 2)
TagInt = _with_tag_id(Int(), 3)
TagLong = _with_tag_id(Long(), 4)
TagFloat = _with_tag_id(Float(), 5)
TagDouble = _with_tag_id(Double(), 6)

TagBytes = _with_tag_id(Prefixed(Bytes(), Int()), 7)
TagString = _with_tag_id(Prefixed(String(), Short()), 8)
TagIntArray = _with_tag_id(Prefixed(Array(Int()), Int()), 11)
TagLongArray = _with_tag_id(Prefixed(Array(Long()), Int()), 11)


class Tag(t.NamedTuple, t.Generic[T]):
    id: int
    name: t.Union[str, None]
    value: T
    item_id: t.Union[int, None] = None


Tag_End = Tag(0, None, None)

_TAG_TYPE = t.Union[
    _TagType[int],
    _TagType[float],
    _TagType[bytes],
    _TagType[str],
    _TagType[t.Sequence[int]],
]


class NBT(_Type[Tag]):
    tags: t.List[_TAG_TYPE] = [
        TagByte,
        TagShort,
        TagInt,
        TagLong,
        TagFloat,
        TagDouble,
        TagBytes,
        TagString,
        TagIntArray,
        TagLongArray,
    ]

    def write_tag_payload(self, buffer: t.BinaryIO, tag: Tag):
        if tag.id == 10 and isinstance(tag.value, dict):
            return self.write_compound_tag(buffer, tag)

        if tag.id == 9 and isinstance(tag.value, list):
            return self.write_list_tag(buffer, tag)

        tag_t = [tag_ for tag_ in self.tags if tag_.tag_id == tag.id]
        if len(tag_t) == 0:
            raise RuntimeError("Invalid tag_id {}".format(tag.id))

        return tag_t[0].write(buffer, tag.value)

    def write_compound_tag(
        self, buffer: t.BinaryIO, tag: Tag[t.Mapping[str, Tag]]
    ):
        if tag.id != 10:
            raise RuntimeError("Invalid compound tag")

        written = sum(
            [self.write(buffer, tag_item) for tag_item in tag.value.values()]
        )
        return written + self.write(buffer, Tag_End)

    def write_list_tag(self, buffer: t.BinaryIO, tag: Tag[t.Sequence[Tag]]):
        if tag.id != 9 or tag.item_id is None:
            raise RuntimeError("Invalid list tag")

        written = Byte().write(buffer, tag.item_id)
        written += Int().write(buffer, len(tag.value))
        return written + sum(
            [
                self.write_tag_payload(buffer, tag_item)
                for tag_item in tag.value
            ]
        )

    def write(self, buffer: t.BinaryIO, value: Tag, **kwds) -> int:
        written = Byte().write(buffer, value.id)
        if value.id == Tag_End.id:
            return written

        if value.name is None:
            raise RuntimeError("Unexpected None tag name")

        written += UShort().write(buffer, len(value.name))
        written += buffer.write(value.name.encode("utf-8"))

        if value.id == 10 and isinstance(value.value, dict):
            return written + self.write_compound_tag(buffer, value)

        if value.id == 9 and isinstance(value.value, list):
            return written + self.write_list_tag(buffer, value)

        return written + self.write_tag_payload(buffer, value)

    def read_tag_payload(self, buffer: t.BinaryIO, tag_id: int):
        if tag_id == 10:
            return self.read_compound_tag(buffer)

        if tag_id == 9:
            return self.read_list_tag(buffer)

        tag_t = [tag_ for tag_ in self.tags if tag_.tag_id == tag_id]
        if len(tag_t) == 0:
            raise RuntimeError("Invalid tag_id {}".format(tag_id))

        return tag_t[0].read(buffer)

    def read_compound_tag(self, buffer: t.BinaryIO):
        _last_tag: Tag = Tag(-1, None, None)

        result: t.MutableMapping[str, Tag] = dict()
        while _last_tag.id != Tag_End.id:
            _last_tag = self.read(buffer)
            if _last_tag.id != Tag_End.id and _last_tag.name is not None:
                result[_last_tag.name] = _last_tag

        return result

    def read_list_tag(self, buffer: t.BinaryIO):
        item_tag_id = Byte().read(buffer)
        list_length = Int().read(buffer)

        return [
            Tag(
                item_tag_id,
                None,
                self.read_tag_payload(buffer, item_tag_id),
                item_id=item_tag_id,
            )
            for _ in range(list_length)
        ], item_tag_id

    def read(self, buffer: t.BinaryIO, **kwds) -> Tag:
        tag_id = UByte().read(buffer)
        if tag_id == Tag_End.id:
            return Tag_End

        name_len = UShort().read(buffer)
        name = buffer.read(name_len).decode("utf-8")

        if tag_id == 10:
            return Tag(tag_id, name, self.read_compound_tag(buffer))

        if tag_id == 9:
            list_items, item_tag_id = self.read_list_tag(buffer)
            return Tag(tag_id, name, list_items, item_tag_id)

        return Tag(tag_id, name, self.read_tag_payload(buffer, tag_id))


# Nested
class Nested(_Type[T]):
    def __init__(self, cls: t.Type[T]) -> None:
        super().__init__()
        self.__cls = cls

    def _iter_fields(self):
        for _field in fields(self.__cls):
            if "type" in _field.metadata:
                yield _field

    def write(self, buffer: t.BinaryIO, value: T, **kwds) -> int:
        _ctx: t.Dict[str, t.Dict[str, t.Any]] = {}

        # TODO: Explain why reversed
        for _field in reversed(list(self._iter_fields())):
            _type = _field.metadata["type"]
            _value = _field.metadata.get("value", None)

            if callable(_value):
                field_value = _value(_ctx)
            else:
                field_value = getattr(value, _field.name)

            if field_value is not None:
                with io.BytesIO() as buf:
                    _len = _type.write(buf, field_value)
                    _bytes = buf.getvalue()

                _ctx[_field.name] = {
                    "value": field_value,
                    "bytes": _bytes,
                    "len": _len,
                }
            else:
                _ctx[_field.name] = {
                    "value": None,
                    "bytes": b"",
                    "len": 0,
                }

        return sum(
            [
                buffer.write(_ctx[field.name]["bytes"])
                for field in self._iter_fields()
            ]
        )

    def read(self, buffer: t.BinaryIO, len: int = -1, **kwds) -> T:
        _ctx: t.Dict[str, t.Union[t.Any, t.Dict[str, t.Any]]] = {"__len": len}
        init_args = {}
        other_args = {}

        for _field in self._iter_fields():
            _type = _field.metadata["type"]
            _len = _field.metadata.get("len", None)
            _present = _field.metadata.get("present", None)

            is_present = True
            if callable(_present):
                is_present = _present(_ctx)

            value = None
            if is_present:
                props = {}
                if callable(_len):
                    props["len"] = _len(_ctx)

                start_pos = buffer.tell()
                value = _type.read(buffer, **props)
                bytes_read = buffer.tell() - start_pos

                _ctx[_field.name] = {
                    "value": value,
                    "bytes": None,
                    "len": bytes_read,
                }
            else:
                _ctx[_field.name] = {
                    "value": None,
                    "bytes": None,
                    "len": 0,
                }

            if _field.init:
                init_args[_field.name] = value
            else:
                other_args[_field.name] = value

        instance = self.__cls(**init_args)
        for key, val in other_args.items():
            setattr(instance, key, val)
        return instance


# Others
class Position(_Type[t.Tuple[int, int, int]]):
    def write(
        self, buffer: t.BinaryIO, value: t.Tuple[int, int, int], **kwds
    ) -> int:
        byte_val = (
            ((value[0] & 0x3FFFFFF) << 38)
            | ((value[1] & 0x3FFFFFF) << 12)
            | (value[2] & 0xFFF)
        )
        return ULong().write(buffer, byte_val)

    def read(self, buffer: t.BinaryIO, **kwds) -> t.Tuple[int, int, int]:
        byte_val = ULong().read(buffer)
        x, z, y = (
            byte_val >> 38,
            (byte_val >> 12) & 0x3FFFFFF,
            byte_val & 0xFFF,
        )

        if x >= 1 << 25:
            x -= 1 << 26
        if y >= 1 << 11:
            y -= 1 << 12
        if z >= 1 << 25:
            z -= 1 << 26

        return x, z, y


@dataclass
class Slot:
    present: bool = field(metadata={"type": Bool()})
    item_id: int = field(
        metadata={
            "type": Optional(VarInt()),
            "present": lambda ctx: ctx["present"]["value"],
        }
    )
    item_cnt: int = field(
        metadata={
            "type": Optional(Byte()),
            "present": lambda ctx: ctx["present"]["value"],
        }
    )
    nbt: Tag = field(
        metadata={
            "type": Optional(NBT()),
            "present": lambda ctx: ctx["present"]["value"],
        }
    )


@dataclass
class Rotation:
    x: float = field(metadata={"type": Float()})
    y: float = field(metadata={"type": Float()})
    z: float = field(metadata={"type": Float()})


class Particle(_Type[t.Tuple[int, t.Any]]):
    @dataclass
    class DustParticle:
        red: float = field(metadata={"type": Float()})
        blue: float = field(metadata={"type": Float()})
        green: float = field(metadata={"type": Float()})
        scale: float = field(metadata={"type": Float()})

    @dataclass
    class DustTransitionParticle:
        from_red: float = field(metadata={"type": Float()})
        from_blue: float = field(metadata={"type": Float()})
        from_green: float = field(metadata={"type": Float()})
        scale: float = field(metadata={"type": Float()})
        to_red: float = field(metadata={"type": Float()})
        to_blue: float = field(metadata={"type": Float()})
        to_green: float = field(metadata={"type": Float()})

    @dataclass
    class VibrationParticle:
        position_type: str = field(
            metadata={"type": Prefixed(String(), VarInt())}
        )
        block_position: t.Tuple[int, int, int] = field(
            metadata={
                "type": Position(),
                "present": lambda ctx: ctx["position_type"]["value"]
                == "minecraft:block",
            }
        )
        entity_id: int = field(
            metadata={
                "type": VarInt(),
                "present": lambda ctx: ctx["position_type"]["value"]
                == "minecraft:entity",
            }
        )
        entity_eye_height: float = field(
            metadata={
                "type": Float(),
                "present": lambda ctx: ctx["position_type"]["value"]
                == "minecraft:entity",
            }
        )
        ticks: int = field(metadata={"type": VarInt()})

    _types: t.Mapping[int, _Type] = {
        2: VarInt(),
        3: VarInt(),
        14: Nested(DustParticle),
        15: Nested(DustTransitionParticle),
        24: VarInt(),
        35: Nested(Slot),
        36: Nested(VibrationParticle),
    }

    def write(
        self, buffer: t.BinaryIO, value: t.Tuple[int, t.Any], **kwds
    ) -> int:
        nbytes = VarInt().write(buffer, value[0])
        if value[0] in self._types.keys():
            _type = self._types[value[0]]
            nbytes += _type.write(buffer, value[1])

        return nbytes

    def read(self, buffer: t.BinaryIO, **kwds) -> t.Tuple[int, t.Any]:
        part_id = VarInt().read(buffer)
        if part_id in self._types.keys():
            _type = self._types[part_id]
            value = _type.read(buffer)
        else:
            value = None

        return part_id, value


@dataclass
class VillagerData:
    type: int = field(metadata={"type": VarInt()})
    profession: int = field(metadata={"type": VarInt()})
    level: int = field(metadata={"type": VarInt()})


@dataclass
class GlobalPosition:
    dimension: str = field(metadata={"type": Prefixed(Identifier(), VarInt())})
    position: t.Tuple[int, int, int] = field(metadata={"type": Position()})


@dataclass
class EntityMetadataEntry:
    index: int
    type: int
    value: t.Any


class EntityMetadata(_Type[t.Sequence[EntityMetadataEntry]]):
    _types: t.Mapping[int, _Type] = {
        0: Byte(),
        1: VarInt(),
        2: VarLong(),
        3: Float(),
        4: Prefixed(String(), VarInt()),
        5: Prefixed(Chat(), VarInt()),
        6: Optional(Prefixed(Chat(), VarInt())),
        7: Nested(Slot),
        8: Bool(),
        9: Nested(Rotation),
        10: Position(),
        11: Optional(Position()),
        12: VarInt(),
        13: Optional(UUID()),
        14: VarInt(),
        15: NBT(),
        16: Particle(),
        17: Nested(VillagerData),
        18: Optional(VarInt()),
        19: Enum(VarInt(), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]),
        20: VarInt(),
        21: VarInt(),
        22: Nested(GlobalPosition),
        23: VarInt(),
    }

    def _write_entry(
        self, buffer: t.BinaryIO, entry: EntityMetadataEntry
    ) -> int:
        nbytes = UByte().write(buffer, entry.index)
        if entry.index != 0xFF:
            nbytes += VarInt().write(buffer, entry.type)
            _type = self._types[entry.type]
            if isinstance(_type, Optional):
                is_present = entry.value is not None
                nbytes += Bool().write(buffer, is_present)
                nbytes += _type.write(buffer, entry.value, present=is_present)
            else:
                nbytes += _type.write(buffer, entry.value)

        return nbytes

    def _read_entry(self, buffer: t.BinaryIO) -> EntityMetadataEntry:
        entry_index = UByte().read(buffer)
        if entry_index != 0xFF:
            entry_type = VarInt().read(buffer)
            _type = self._types[entry_type]
            if isinstance(_type, Optional):
                is_present = Bool().read(buffer)
                value = _type.read(buffer, present=is_present)
            else:
                value = _type.read(buffer)
        else:
            entry_type = -1
            value = None

        return EntityMetadataEntry(entry_index, entry_type, value)

    def write(
        self,
        buffer: t.BinaryIO,
        value: t.Sequence[EntityMetadataEntry],
        **kwds,
    ) -> int:
        nbytes = 0
        for entry in value:
            if entry.index == 0xFF:
                raise RuntimeError("Entry index cannot be 0xFF")

            nbytes += self._write_entry(buffer, entry)

        # Write entry for end of metadata
        nbytes += self._write_entry(buffer, EntityMetadataEntry(0xFF, 0, None))
        return nbytes

    def read(self, buffer: t.BinaryIO, **kwds) -> t.List[EntityMetadataEntry]:
        entries = []
        entry = self._read_entry(buffer)
        while entry.index != 0xFF:
            print(entry)
            entries.append(entry)
            entry = self._read_entry(buffer)

        return entries
