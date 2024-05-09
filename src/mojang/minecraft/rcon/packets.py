from __future__ import annotations

import random
import socket
import struct


class Packets:
    def __init__(self, sock: socket.socket):
        self.__sock = sock

    def _new_id(self) -> int:
        return random.randint(0, 2**31)

    def send(self, _type: int, payload: str) -> tuple[int, int]:
        packet_id = self._new_id()
        packet = struct.pack(
            f"<iii{len(payload) + 2}s",
            10 + len(payload),
            packet_id,
            _type,
            payload.encode("ascii") + b"\00",
        )
        sent = self.__sock.send(packet)
        return packet_id, sent

    def recv(self) -> tuple[int, int, bytes, int]:
        with self.__sock.makefile("rb") as buffer:
            size = int.from_bytes(buffer.read(4), "little")

            # Read fully
            data = b""
            while len(data) < size:
                _data = buffer.read(size - len(data))
                if _data:
                    data += _data

        packet_id, _type = struct.unpack("<ii", data[:8])
        return packet_id, _type, data[8:], size - 8
