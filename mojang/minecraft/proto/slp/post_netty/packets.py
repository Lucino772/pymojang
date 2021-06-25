import io
import socket
from contextlib import contextmanager

from .types import VarInt


class Packets:

    def __init__(self, sock: socket.socket):
        self.__sock = sock


    @contextmanager
    def send(self):
        packet = io.BytesIO()
        try:
            yield packet
        finally:
            data = packet.getvalue()
            with self.__sock.makefile('wb') as buffer:
                VarInt.write(buffer, len(data))
                buffer.write(data)


    def recv(self):
        with self.__sock.makefile('rb') as buffer:
            length = VarInt.read(buffer)
            packet = buffer.read(length)

        return io.BytesIO(packet)
