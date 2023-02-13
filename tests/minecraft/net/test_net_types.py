import gzip
import io
import os
import random
import unittest
import uuid
from dataclasses import dataclass, field

from mojang.minecraft.net.types import (
    NBT,
    UUID,
    Array,
    Bool,
    Byte,
    Bytes,
    Chat,
    Double,
    EntityMetadata,
    EntityMetadataEntry,
    Enum,
    Float,
    GlobalPosition,
    Identifier,
    Int,
    Long,
    Nested,
    Optional,
    Particle,
    Position,
    Prefixed,
    Rotation,
    Short,
    Slot,
    String,
    Tag_End,
    UByte,
    UInt,
    ULong,
    UShort,
    VarInt,
    VarLong,
    VillagerData,
)


@dataclass
class CustomType:
    name_len: int = field(
        metadata={
            "type": Int(),
            "value": lambda ctx: len(ctx["name"]["bytes"]),
        },
        init=False,
        compare=False,
        default=-1,
    )
    name: str = field(
        metadata={
            "type": String(),
            "len": lambda ctx: ctx["name_len"]["value"],
        }
    )

    has_age: bool = field(metadata={"type": Bool()})
    age: int = field(
        metadata={
            "type": Optional(Int()),
            "present": lambda ctx: ctx["has_age"]["value"],
        }
    )


class TestMinecraftNetTypes(unittest.TestCase):
    def _pack(self, _type, init_val, assert_len_equals=True, **kwds):
        with io.BytesIO() as buffer:
            nbytes = _type.write(buffer, init_val, **kwds)
            _bytes = buffer.getvalue()

        if assert_len_equals:
            self.assertEqual(nbytes, len(_bytes))

        return nbytes, _bytes

    def _unpack(
        self, _type, _bytes, init_val, assert_init_equals=True, **kwds
    ):
        with io.BytesIO(_bytes) as buffer:
            value = _type.read(buffer, **kwds)

        if assert_init_equals:
            if isinstance(init_val, float):
                self.assertAlmostEqual(value, init_val)
            else:
                self.assertEqual(value, init_val)

        return value

    def _simple_test(self, _type, init_val, **kwds):
        nbytes, _bytes = self._pack(_type, init_val)
        value = self._unpack(_type, _bytes, init_val, **kwds)
        return nbytes, _bytes, value

    def _test_optional(self, _type, init_val):
        opt_type = Optional(_type)

        # Test with present=True
        self._simple_test(opt_type, init_val, present=True)

        # Test with present=False
        _bytes = self._pack(opt_type, init_val, present=False)[1]
        self.assertEqual(_bytes, b"")
        value = self._unpack(
            opt_type, _bytes, init_val, assert_init_equals=False, present=False
        )
        self.assertIsNone(value)

    def _test_numeric_value(
        self, _type, signed, min_num, max_num, value=None, test_max_min=True
    ):
        if value is None:
            value = abs(random.choice(range(min_num + 1, max_num)))

        # Pick a random value in range and test it
        # If type is signed also test a negative value
        self._simple_test(_type, value)
        if signed:
            self._simple_test(_type, -value)

        # Test the max and min number
        if test_max_min is True:
            self._simple_test(_type, min_num)
            self._simple_test(_type, max_num)

            # Test a number bigger than the max, this should raise an error
            with self.assertRaises(Exception):
                self._simple_test(_type, max_num + 1)

            # Test a number smaller than the min, this should raise an error
            with self.assertRaises(Exception):
                self._simple_test(_type, min_num - 1)

    def test_bytes(self):
        self._simple_test(Bytes(), b"Hello World !", len=13)

    def test_string(self):
        self._simple_test(String(), "Hello World !", len=13)

    def test_identifier(self):
        self._simple_test(Identifier(), "minecraft:world", len=15)

        with self.assertRaises(RuntimeError):
            self._pack(Identifier(), "Hello World !")

    def test_chat(self):
        self._simple_test(Chat(), ["Hello", "World !", 10, 12, 255])
        self._simple_test(Chat(), {"name": "John", "age": 40, "height": 1.70})

    def test_uuid(self):
        self._simple_test(UUID(), uuid.uuid4())

    def test_varnums(self):
        self._test_numeric_value(VarInt(), True, -2147483648, 2147483647)
        self._test_numeric_value(
            VarLong(),
            True,
            -9223372036854775808,
            9223372036854775807,
            value=100,
        )

        # Check that any negative numbers uses the maximum number of bytes
        self.assertEqual(self._simple_test(VarInt(), -100)[0], 5)
        self.assertEqual(self._simple_test(VarLong(), -100)[0], 10)

    def test_numbers(self):
        self._test_numeric_value(Byte(), True, -128, 127)
        self._test_numeric_value(UByte(), False, 0, 255)
        self._test_numeric_value(Short(), True, -32768, 32767)
        self._test_numeric_value(UShort(), False, 0, 65535)
        self._test_numeric_value(Int(), True, -2147483648, 2147483647)
        self._test_numeric_value(UInt(), False, 0, 4294967295)
        self._test_numeric_value(
            Long(), True, -9223372036854775808, 9223372036854775807, value=100
        )
        self._test_numeric_value(
            ULong(), False, 0, 18446744073709551615, value=100
        )
        self._test_numeric_value(
            Float(),
            True,
            1.175494351e-38,
            3.402823466e38,
            value=100,
            test_max_min=False,
        )
        self._test_numeric_value(
            Double(),
            True,
            2.2250738585072014e-308,
            1.7976931348623158e308,
            value=100,
            test_max_min=False,
        )

    def test_bool(self):
        self._simple_test(Bool(), True)
        self._simple_test(Bool(), False)

    def test_nbt(self):
        filename = os.path.join(
            os.path.dirname(__file__), "example_nbt_big.nbt.gz"
        )
        with gzip.open(filename, "rb") as fp:
            nbt_bytes = fp.read()

        with io.BytesIO(nbt_bytes) as buffer:
            tag = NBT().read(buffer)

        with io.BytesIO() as buffer:
            nbytes = NBT().write(buffer, tag)
            _bytes = buffer.getvalue()

        self.assertEqual(nbytes, len(_bytes))
        self.assertEqual(nbt_bytes, _bytes)

    def test_prefixed(self):
        self._simple_test(Prefixed(String(), UShort()), "Hello World !")
        self._simple_test(Prefixed(Bytes(), UInt()), b"Hello World !")
        self._simple_test(
            Prefixed(Array(UInt()), UByte()), [10, 50, 10, 40, 22, 192]
        )

    def test_optional(self):
        self._test_optional(Int(), 10)
        self._test_optional(Prefixed(String(), UInt()), "Hello World !")
        self._test_optional(Prefixed(Bytes(), UShort()), b"Hello World !")

    def test_enum(self):
        self._simple_test(Enum(Int(), [0, 1, 2, 3]), 3)

        with self.assertRaises(RuntimeError):
            self._simple_test(Enum(Int(), [0, 1, 2, 3]), 6)

    def test_array(self):
        init_val = [0, 1, 2, 3, 4]

        # The array type returns how many items where
        # written in the buffer instead of how many bytes
        # were written in the buffer. This makes it easier
        # when used with Prefixed type
        array_len, _bytes = self._pack(
            Array(Int()), init_val, assert_len_equals=False
        )

        # If we want to check that all the items were writtent
        # we can multiply the array_len by the item size in bytes
        self.assertEqual(array_len * 4, len(_bytes))

        self._unpack(Array(Int()), _bytes, init_val, len=len(init_val))

    def test_nested(self):
        self._simple_test(Nested(CustomType), CustomType("John", False, None))
        self._simple_test(Nested(CustomType), CustomType("John", True, 40))

    def test_position(self):
        self._simple_test(Position(), (100, 100, 50))

    def test_rotation(self):
        self._simple_test(Nested(Rotation), Rotation(10, 100, 200))

    def test_slot(self):
        self._simple_test(Nested(Slot), Slot(True, 4, 2, Tag_End))

    def test_particle(self):
        self._simple_test(Particle(), (1, None))
        self._simple_test(Particle(), (2, 5))
        self._simple_test(Particle(), (3, 5))
        self._simple_test(Particle(), (14, Particle.DustParticle(1, 1, 1, 0)))
        self._simple_test(
            Particle(),
            (15, Particle.DustTransitionParticle(0, 0, 0, 0, 1, 1, 1)),
        )
        self._simple_test(Particle(), (24, 5))
        self._simple_test(Particle(), (35, Slot(True, 4, 2, Tag_End)))
        self._simple_test(
            Particle(),
            (
                36,
                Particle.VibrationParticle("minecraft:entity", None, 1, 3, 4),
            ),
        )

    def test_villager_data(self):
        self._simple_test(Nested(VillagerData), VillagerData(1, 1, 20))

    def test_global_position(self):
        self._simple_test(
            Nested(GlobalPosition),
            GlobalPosition("minecraft:nether", (100, 100, 50)),
        )

    def test_entity_metadata(self):
        meta = [
            EntityMetadataEntry(0, 0, 100),  # Byte
            EntityMetadataEntry(0, 1, 100),  # VarInt
            EntityMetadataEntry(0, 2, 100),  # VarLong
            EntityMetadataEntry(0, 3, 100),  # Float
            EntityMetadataEntry(0, 4, "Hello World !"),  # String
            EntityMetadataEntry(0, 5, {"name": "John"}),  # Chat
            EntityMetadataEntry(0, 6, {"name": "John"}),  # Optchat
            EntityMetadataEntry(0, 6, None),  # OptChat
            EntityMetadataEntry(0, 7, Slot(True, 4, 2, Tag_End)),  # Slot
            EntityMetadataEntry(0, 8, True),  # Bool
            EntityMetadataEntry(0, 9, Rotation(10, 10, 10)),  # Rotation
            EntityMetadataEntry(0, 10, (10, 10, 10)),  # Position
            EntityMetadataEntry(0, 11, (10, 10, 10)),  # OptPosition
            EntityMetadataEntry(0, 11, None),  # OptPosition
            EntityMetadataEntry(0, 12, 1),  # Direction (VarInt)
            EntityMetadataEntry(0, 13, uuid.uuid4()),  # OptUUID
            EntityMetadataEntry(0, 13, None),  # OptUUID
            EntityMetadataEntry(0, 14, 1),  # OptBlockID (VarInt)
            EntityMetadataEntry(0, 15, Tag_End),  # NBT
            EntityMetadataEntry(0, 16, (1, None)),  # Particle
            EntityMetadataEntry(0, 17, VillagerData(1, 1, 20)),  # VillagerData
            EntityMetadataEntry(0, 18, 10),  # OptVarInt (entity ID)
            EntityMetadataEntry(0, 18, None),  # OptVarInt (entity ID)
            EntityMetadataEntry(0, 19, 5),  # Pose (VarInt Enum)
            EntityMetadataEntry(0, 20, 1),  # Cat Variant
            EntityMetadataEntry(0, 21, 1),  # Frog Variant
            EntityMetadataEntry(
                0, 22, GlobalPosition("minecraft:world", (10, 10, 10))
            ),  # GlobalPos
            EntityMetadataEntry(0, 23, 1),  # Painting Variant
        ]
        self._simple_test(EntityMetadata(), meta)

        with self.assertRaises(RuntimeError):
            self._simple_test(
                EntityMetadata(), meta + [EntityMetadataEntry(0xFF, 0, None)]
            )
