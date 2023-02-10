import io
import typing as t
from dataclasses import dataclass, fields


@dataclass
class Packet:
    @classmethod
    def _iter_fields(cls):
        for field in fields(cls):
            if "type" in field.metadata:
                yield field

    def serialize(self, buffer: t.BinaryIO) -> int:
        _ctx: t.Dict[str, t.Dict[str, t.Any]] = {}

        # TODO: Explain why reversed
        for field in reversed(list(self._iter_fields())):
            _type = field.metadata["type"]
            _value = field.metadata.get("value", None)

            if callable(_value):
                value = _value(_ctx)
            else:
                value = getattr(self, field.name)

            with io.BytesIO() as buf:
                _len = _type.write(buf, value)
                _bytes = buf.getvalue()

            _ctx[field.name] = {"value": value, "bytes": _bytes, "len": _len}

        return sum(
            [
                buffer.write(_ctx[field.name]["bytes"])
                for field in self._iter_fields()
            ]
        )

    @classmethod
    def deserialize(cls, buffer: t.BinaryIO) -> "Packet":
        _ctx: t.Dict[str, t.Dict[str, t.Any]] = {}
        init_args = {}
        other_args = {}

        for field in cls._iter_fields():
            _type = field.metadata["type"]
            _len = field.metadata.get("len", None)

            props = {}
            if callable(_len):
                props["len"] = _len(_ctx)

            value = _type.read(buffer, **props)

            _ctx[field.name] = {"value": value, "bytes": None, "len": None}

            if field.init:
                init_args[field.name] = value
            else:
                other_args[field.name] = value

        instance = cls(**init_args)
        for key, val in other_args.items():
            setattr(instance, key, val)
        return instance
