class _Packet:
    @property
    def packet_id(self) -> int:
        raise NotImplementedError

    def serialize(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, data: bytes):
        raise NotImplementedError
