import socket
import struct
from typing import Optional, Tuple


class Packets:
    
    def __init__(self, sock: socket.socket):
        self.__sock = sock

    def send(self, _type: int, sess_id: int, data: Optional[bytes] = b'') -> int:
        packet = struct.pack(f'>Hbi{len(data)}s', 0xFEFd, _type, sess_id, data)
        return self.__sock.send(packet)

    def recv(self) -> Tuple[int, int, bytes]:
        with self.__sock.makefile('rb') as buffer:
            data = buffer.read1()

        _type, sess_id = struct.unpack('>bi', data[:5])
        return _type, sess_id, data[5:]
