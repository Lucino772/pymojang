import dataclasses
import typing as t


@dataclasses.dataclass
class Packet:
    packet_id: t.ClassVar[int] = -1

    @classmethod
    def _iter_fields(cls):
        for field in dataclasses.fields(cls):
            _type = field.metadata.get("_type")
            if _type is not None:
                yield field, _type

    def serialize(self, buffer: t.BinaryIO) -> int:
        nbytes = 0

        for field, _type in self._iter_fields():
            nbytes += _type.write(buffer, getattr(self, field.name))

        return nbytes

    @classmethod
    def deserialize(cls, buffer: t.BinaryIO):
        values = {}

        for field, _type in cls._iter_fields():
            values[field.name] = _type.read(buffer)

        return cls(**values)
