import struct

from ...common.packet import Packet

class LoginRequest(Packet):
    type: int = 3
    id: int
    payload: str

    def _bytes(self):
        encoded_payload = self.payload.encode('ascii')
        return struct.pack('<ii{}s2s'.format(len(encoded_payload)), self.id, self.type, encoded_payload, b'\0\0')

class LoginResponse(Packet):
    type: int
    id: int

    @classmethod
    def _parse(cls, buffer: bytes):
        request_id, _type, _ = struct.unpack_from('<ii{}s'.format(len(buffer) - 10), buffer)
        return dict(type=_type,id=request_id)
