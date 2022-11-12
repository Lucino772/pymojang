from typing import TypeVar, cast

from ._protocols import (
    _DataTypeProtocol,
    _TagArrayDataTypeProtocol,
    _TagDataTypeProtocol,
)
from .array import _AdvancedArray
from .basic import (
    float32_t,
    float64_t,
    int8_t,
    int16_t,
    int32_t,
    int64_t,
    uint16_t,
)
from .bytearray import _AdvancedByteArray

T = TypeVar("T")


def with_tag_id(
    data_t: _DataTypeProtocol[T], tag_id: int
) -> _TagDataTypeProtocol[T]:
    setattr(data_t, "tag_id", tag_id)
    return cast(_TagDataTypeProtocol[T], data_t)


def array_with_tag_id(
    data_t: _AdvancedArray[T], tag_id: int
) -> _TagArrayDataTypeProtocol[T]:
    setattr(data_t, "tag_id", tag_id)
    return cast(_TagArrayDataTypeProtocol[T], data_t)


tag_byte_t = with_tag_id(int8_t, 1)
tag_short_t = with_tag_id(int16_t, 2)
tag_int_t = with_tag_id(int32_t, 3)
tag_long_t = with_tag_id(int64_t, 4)
tag_float_t = with_tag_id(float32_t, 5)
tag_double_t = with_tag_id(float64_t, 6)

tag_bytearray_t = with_tag_id(
    _AdvancedByteArray[bytes](
        max_len=-1,
        length=-1,
        len_prefix_t=int32_t,
        encode=lambda val: val,
        decode=lambda val: val,
    ),
    7,
)
tag_string_t = with_tag_id(
    _AdvancedByteArray[str](
        max_len=-1,
        length=-1,
        len_prefix_t=uint16_t,
        encode=lambda val: val.encode("utf-8"),
        decode=lambda val: val.decode("utf-8"),
    ),
    8,
)
tag_int_array_t = array_with_tag_id(
    _AdvancedArray[int](
        item_t=int32_t, max_len=-1, length=-1, len_prefix_t=int32_t
    ),
    11,
)
tag_long_array_t = array_with_tag_id(
    _AdvancedArray[int](
        item_t=int32_t, max_len=-1, length=-1, len_prefix_t=int64_t
    ),
    12,
)
