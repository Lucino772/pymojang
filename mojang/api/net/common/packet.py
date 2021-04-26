import io
from typing import IO


class BasePacket:
    
    def __new__(cls, **kwargs):
        obj = object.__new__(cls)

        for key, value in obj._types().items():
            setattr(obj, key, kwargs.get(key, value.default))

        return obj

    @classmethod
    def from_bytes(cls, data: bytes):
        with io.BytesIO(data) as buffer:
            packet = cls.read(buffer)

        return packet

    @classmethod
    def _types(cls):
        return dict([(key, getattr(cls, key)) for key, value in getattr(cls, '__annotations__', {}).items()])

    @classmethod
    def read(cls, buffer: IO):
        _dict = {}
        for key, value in cls._types().items():
            _dict[key] = value.read(buffer)
        return cls(**_dict)

    def write(self, buffer: IO):
        for key, value in self._types().items():
            value.write(getattr(self, key), buffer)

    @property
    def data(self):
        with io.BytesIO() as buffer:
            self.write(buffer)
            data = buffer.getvalue()
        
        return data
