from __future__ import annotations

import typing as t

_T = t.TypeVar("_T")


class Serializer(t.Generic[_T]):
    @classmethod
    def serialize(cls, buffer: t.BinaryIO, packet: _T) -> int:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, buffer: t.BinaryIO) -> _T:
        raise NotImplementedError


class _PacketSerializerSpec(t.NamedTuple, t.Generic[_T]):
    serializer: t.Type[Serializer[_T]]
    version: t.Optional[int]
    min_version: t.Optional[int]
    max_version: t.Optional[int]
    netty: bool


def packet(packet_cls: t.Type[_T]):
    def _get_serializer(cls, version: int, netty: bool):
        for spec in filter(lambda s: s.netty == netty, cls._serializers):
            if (spec.version is not None and spec.version == version) or (
                spec.min_version is not None
                and spec.max_version is not None
                and spec.min_version <= version <= spec.max_version
            ):
                return spec.serializer

        return None

    def add_serializer(
        cls,
        serializer_cls: t.Type[Serializer[_T]],
        version: t.Optional[int] = None,
        max_version: t.Optional[int] = None,
        min_version: t.Optional[int] = None,
        netty: bool = False,
    ):
        cls._serializers.append(
            _PacketSerializerSpec(
                serializer_cls, version, min_version, max_version, netty
            )
        )

    def register(
        cls,
        version: t.Optional[int] = None,
        max_version: t.Optional[int] = None,
        min_version: t.Optional[int] = None,
        netty: bool = True,
    ):
        def _wrapper(serializer_cls: t.Type[Serializer[_T]]):
            cls.add_serializer(
                serializer_cls, version, min_version, max_version, netty
            )
            return serializer_cls

        return _wrapper

    def serialize(
        cls, buffer: t.BinaryIO, packet: _T, version: int, netty: bool = True
    ) -> int:
        serializer = cls._get_serializer(version, netty)
        if serializer is None:
            raise RuntimeError(
                f"No serializer for version: {version} - netty: {netty}"
            )

        return serializer.serialize(buffer, packet)

    def deserialize(
        cls, buffer: t.BinaryIO, version: int, netty: bool = True
    ) -> _T:
        serializer = cls._get_serializer(version, netty)
        if serializer is None:
            raise RuntimeError(
                f"No serializer for version: {version} - netty: {netty}"
            )

        return serializer.deserialize(buffer)

    setattr(packet_cls, "_serializers", [])
    setattr(packet_cls, "_get_serializer", classmethod(_get_serializer))
    setattr(packet_cls, "add_serializer", classmethod(add_serializer))
    setattr(packet_cls, "register", classmethod(register))
    setattr(packet_cls, "serialize", classmethod(serialize))
    setattr(packet_cls, "deserialize", classmethod(deserialize))
    return packet_cls
