import gzip
import io
import os
import random
import unittest
import uuid

from mojang.minecraft.net.types import (
    NBT,
    UUID,
    Array,
    Bool,
    Byte,
    Bytes,
    Chat,
    Double,
    Float,
    GlobalPosition,
    Identifier,
    Int,
    Long,
    Nested,
    Optional,
    Position,
    Prefixed,
    Rotation,
    Short,
    String,
    UByte,
    UInt,
    ULong,
    UShort,
    VarInt,
    VarLong,
    VillagerData,
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
            VarLong(), True, -9223372036854775808, 9223372036854775807
        )

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
        pass  # TODO

    def test_array(self):
        pass  # TODO

    def test_nested(self):
        pass  # TODO

    def test_position(self):
        self._simple_test(Position(), (100, 100, 50))

    def test_rotation(self):
        self._simple_test(Nested(Rotation), Rotation(10, 100, 200))

    def test_slot(self):
        pass  # TODO

    def test_particle(self):
        pass  # TODO

    def test_villager_data(self):
        self._simple_test(Nested(VillagerData), VillagerData(1, 1, 20))

    def test_global_position(self):
        self._simple_test(
            Nested(GlobalPosition),
            GlobalPosition("minecraft:nether", (100, 100, 50)),
        )

    def test_entity_metadata(self):
        pass  # TODO
