from __future__ import annotations

import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import socket


class Packets:
    def __init__(self, sock: socket.socket):
        self.__sock = sock

    def send(self, _type: int, sess_id: int, data: bytes = b"") -> int:
        packet = struct.pack(f">Hbi{len(data)}s", 0xFEFD, _type, sess_id, data)
        return self.__sock.send(packet)

    def recv(self) -> tuple[int, int, bytes]:
        with self.__sock.makefile("rb") as buffer:
            data = buffer.read()

        _type, sess_id = struct.unpack(">bi", data[:5])
        return _type, sess_id, data[5:]
