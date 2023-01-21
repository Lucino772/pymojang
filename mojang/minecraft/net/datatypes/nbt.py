from __future__ import annotations

from typing import (
    BinaryIO,
    Generic,
    List,
    Mapping,
    MutableMapping,
    NamedTuple,
    Sequence,
    TypeVar,
    Union,
    cast,
)

from .basic import (
    _bytearray_t,
    _GenericDataType,
    _string_t,
    float32_t,
    float64_t,
    int8_t,
    int16_t,
    int32_t,
    int64_t,
    uint8_t,
    uint16_t,
)

DataType_T = TypeVar("DataType_T")


class _TagProtocol(_GenericDataType[DataType_T]):
    tag_id: int


def with_tag_id(
    data_t: _GenericDataType[DataType_T], tag_id: int
) -> _TagProtocol[DataType_T]:
    setattr(data_t, "tag_id", tag_id)
    return cast(_TagProtocol[DataType_T], data_t)


tag_byte_t = with_tag_id(int8_t(), 1)
tag_short_t = with_tag_id(int16_t(), 2)
tag_int_t = with_tag_id(int32_t(), 3)
tag_long_t = with_tag_id(int64_t(), 4)
tag_float_t = with_tag_id(float32_t(), 5)
tag_double_t = with_tag_id(float64_t(), 6)

tag_bytearray_t = with_tag_id(_bytearray_t(len_prefix_t=int32_t()), 7)
tag_string_t = with_tag_id(_string_t(len_prefix_t=uint16_t()), 8)
tag_int_array_t = with_tag_id(int32_t().array(len_prefix_t=int32_t()), 11)
tag_long_array_t = with_tag_id(int64_t().array(len_prefix_t=int32_t()), 12)

TagType = Union[
    _TagProtocol[int],
    _TagProtocol[float],
    _TagProtocol[bytes],
    _TagProtocol[str],
    _TagProtocol[Sequence[int]],
]

TagDataType_T = TypeVar("TagDataType_T")


class Tag(NamedTuple, Generic[TagDataType_T]):
    id: int
    name: Union[str, None]
    value: TagDataType_T
    item_id: Union[int, None] = None


Tag_End = Tag(0, None, None)


class nbt_tags_t:
    tags: List[TagType] = [
        tag_byte_t,
        tag_short_t,
        tag_int_t,
        tag_long_t,
        tag_float_t,
        tag_double_t,
        tag_bytearray_t,
        tag_string_t,
        tag_int_array_t,
        tag_long_array_t,
    ]

    @classmethod
    def write_tag_payload(cls, buffer: BinaryIO, tag: Tag):
        if tag.id == 10 and isinstance(tag.value, dict):
            return cls.write_compound_tag(buffer, tag)

        if tag.id == 9 and isinstance(tag.value, list):
            return cls.write_list_tag(buffer, tag)

        tag_t = [tag_ for tag_ in cls.tags if tag_.tag_id == tag.id]
        if len(tag_t) == 0:
            raise RuntimeError("Invalid tag_id {}".format(tag.id))

        return tag_t[0].write(buffer, tag.value)

    @classmethod
    def write_compound_tag(cls, buffer: BinaryIO, tag: Tag[Mapping[str, Tag]]):
        if tag.id != 10:
            raise RuntimeError("Invalid compound tag")

        written = sum(
            [cls.write(buffer, tag_item) for tag_item in tag.value.values()]
        )
        return written + cls.write(buffer, Tag_End)

    @classmethod
    def write_list_tag(cls, buffer: BinaryIO, tag: Tag[Sequence[Tag]]):
        if tag.id != 9 or tag.item_id is None:
            raise RuntimeError("Invalid list tag")

        written = int8_t().write(buffer, tag.item_id)
        written += int32_t().write(buffer, len(tag.value))
        return written + sum(
            [cls.write_tag_payload(buffer, tag_item) for tag_item in tag.value]
        )

    @classmethod
    def write(cls, buffer: BinaryIO, tag: Tag) -> int:
        written = int8_t().write(buffer, tag.id)
        if tag.id == Tag_End.id:
            return written

        if tag.name is None:
            raise RuntimeError("Unexpected None tag name")

        written += uint16_t().write(buffer, len(tag.name))
        written += buffer.write(tag.name.encode("utf-8"))

        if tag.id == 10 and isinstance(tag.value, dict):
            return written + cls.write_compound_tag(buffer, tag)

        if tag.id == 9 and isinstance(tag.value, list):
            return written + cls.write_list_tag(buffer, tag)

        return written + cls.write_tag_payload(buffer, tag)

    @classmethod
    def read_tag_payload(cls, buffer: BinaryIO, tag_id: int):
        if tag_id == 10:
            return cls.read_compound_tag(buffer)

        if tag_id == 9:
            return cls.read_list_tag(buffer)

        tag_t = [tag_ for tag_ in cls.tags if tag_.tag_id == tag_id]
        if len(tag_t) == 0:
            raise RuntimeError("Invalid tag_id {}".format(tag_id))

        return tag_t[0].read(buffer)

    @classmethod
    def read_compound_tag(cls, buffer: BinaryIO):
        _last_tag: Tag = Tag(-1, None, None)

        result: MutableMapping[str, Tag] = dict()
        while _last_tag.id != Tag_End.id:
            _last_tag = cls.read(buffer)
            if _last_tag.id != Tag_End.id and _last_tag.name is not None:
                result[_last_tag.name] = _last_tag

        return result

    @classmethod
    def read_list_tag(cls, buffer: BinaryIO):
        item_tag_id = int8_t().read(buffer)
        list_length = int32_t().read(buffer)

        return [
            Tag(
                item_tag_id,
                None,
                cls.read_tag_payload(buffer, item_tag_id),
                item_id=item_tag_id,
            )
            for _ in range(list_length)
        ], item_tag_id

    @classmethod
    def read(cls, buffer: BinaryIO):
        tag_id = uint8_t().read(buffer)
        if tag_id == Tag_End.id:
            return Tag_End

        name_len = uint16_t().read(buffer)
        name = buffer.read(name_len).decode("utf-8")

        if tag_id == 10:
            return Tag(tag_id, name, cls.read_compound_tag(buffer))

        if tag_id == 9:
            list_items, item_tag_id = cls.read_list_tag(buffer)
            return Tag(tag_id, name, list_items, item_tag_id)

        return Tag(tag_id, name, cls.read_tag_payload(buffer, tag_id))
