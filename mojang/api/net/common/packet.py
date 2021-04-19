
class Packet:

    def __new__(cls, **kwargs):
        obj = object.__new__(cls)
        
        for key, _type in getattr(cls, '__annotations__', {}).items():
            value = kwargs.get(key, getattr(cls, key, None))
            if callable(value):
                value = value()
            if isinstance(value, _type) or value is None:
                setattr(obj, key, value)
            else:
                raise TypeError('Wrong type for parameter `{}`, got `{}` expecting `{}`'.format(key, type(value).__name__, _type.__name__))
        
        return obj

    @classmethod
    def create_from(cls, buffer: bytes):
        kwargs = cls._parse(buffer)
        return cls(**kwargs)

    @classmethod
    def _parse(cls, buffer: bytes):
        raise NotImplementedError()

    def _bytes(self):
        return NotImplemented

    def __bytes__(self):
        return self._bytes()
