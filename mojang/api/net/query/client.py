import socket
import time

from .packets.handshake import HandhakeRequestPacket, HandhakeResponsePacket
from .packets.stats import BasicStatsRequestPacket, BasicStatsResponsePacket, FullStatsRequestPacket, FullStatsResponsePacket

class QueryClient:

    def __init__(self, host: str, port: int):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.settimeout(2)
        self.__host = (host, port)
        self.__token = None
        self.__session_id = int(time.time()) & 0x0F0F0F0F

        self._connect()

    def _connect(self):
        self.__sock.connect(self.__host)
        
        # Send request
        packet = HandhakeRequestPacket(id=self.__session_id)
        with self.__sock.makefile('wb') as buffer:
            packet.write(buffer)

        # Receive response
        with self.__sock.makefile('rb') as buffer:
            r_packet = HandhakeResponsePacket.read(buffer)
        
        # Check type and session id
        if r_packet.type != 9 or r_packet.id != packet.id:
            raise Exception("Error while getting the handshake")

        # Parse token to bytes
        self.__token = int(r_packet.token)

    def _basic_stats(self):
        # Send packet
        packet = BasicStatsRequestPacket(token=self.__token, id=self.__session_id)
        with self.__sock.makefile('wb') as buffer:
            packet.write(buffer)

        # Receive packet
        with self.__sock.makefile('rb') as buffer:
            r_packet = BasicStatsResponsePacket.read(buffer)

        # Check type and session id
        if r_packet.type != 0 or r_packet.id != packet.id:
            raise Exception("Error while getting basic stats")

        return r_packet

    def _full_stats(self):
        # Send packet
        packet = FullStatsRequestPacket(token=self.__token, id=self.__session_id)
        with self.__sock.makefile('wb') as buffer:
            packet.write(buffer)

        # Receive packet
        with self.__sock.makefile('rb') as buffer:
            r_packet = FullStatsResponsePacket.read(buffer)

        # Check type and session id
        if r_packet.type != 0 or r_packet.id != packet.id:
            raise Exception("Error while getting full stats")

        return r_packet

    def stats(self, full=False):
        if full:
            return self._full_stats()
        else:
            return self._basic_stats()
