import struct
import time

from ...common.packet import Packet

class HandhakeRequest(Packet):
    magic: int = 0xFEFD
    type: int = 9
    id: int

    def _bytes(self):
        return struct.pack('>Hbi', self.magic, self.type, self.id)
    
class HandhakeResponse(Packet):
    type: int
    id: int
    token: int

    @classmethod
    def _parse(cls, buffer: bytes):
        _type, _id, payload = struct.unpack_from('>bi{}s'.format(len(buffer) - 6), buffer)
        return dict(type=_type, id=_id, token=int(payload))
