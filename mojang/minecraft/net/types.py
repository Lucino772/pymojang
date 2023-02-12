from __future__ import annotations

import ctypes
import io
import json
import re
import struct
import typing as t
import uuid
from dataclasses import fields

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
        while True:
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
        for field in fields(self.__cls):
            if "type" in field.metadata:
                yield field

    def write(self, buffer: t.BinaryIO, value: T, **kwds) -> int:
        _ctx: t.Dict[str, t.Dict[str, t.Any]] = {}

        # TODO: Explain why reversed
        for field in reversed(list(self._iter_fields())):
            _type = field.metadata["type"]
            _value = field.metadata.get("value", None)

            if callable(_value):
                field_value = _value(_ctx)
            else:
                field_value = getattr(value, field.name)

            if field_value is not None:
                with io.BytesIO() as buf:
                    _len = _type.write(buf, field_value)
                    _bytes = buf.getvalue()

                _ctx[field.name] = {
                    "value": field_value,
                    "bytes": _bytes,
                    "len": _len,
                }
            else:
                _ctx[field.name] = {
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

        for field in self._iter_fields():
            _type = field.metadata["type"]
            _len = field.metadata.get("len", None)
            _present = field.metadata.get("present", None)

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

                _ctx[field.name] = {
                    "value": value,
                    "bytes": None,
                    "len": bytes_read,
                }
            else:
                _ctx[field.name] = {
                    "value": None,
                    "bytes": None,
                    "len": 0,
                }

            if field.init:
                init_args[field.name] = value
            else:
                other_args[field.name] = value

        instance = self.__cls(**init_args)
        for key, val in other_args.items():
            setattr(instance, key, val)
        return instance
