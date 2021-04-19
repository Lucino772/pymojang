import socket
import select
import time

from .packets.handshake import HandhakeRequest, HandhakeResponse
from .packets.stats import BasicStatsRequest, BasicStatsResponse, FullStatsRequest, FullStatsResponse

class QueryClient:

    def __init__(self, host: str, port: int):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.settimeout(2)
        self.__host = (host, port)
        self.__token = None
        self.__session_id = int(time.time()) & 0x0F0F0F0F

        self._connect()

    def _connect(self):
        packet = HandhakeRequest(id=self.__session_id)
        self.__sock.sendto(bytes(packet), self.__host)

        # Receive response
        data, _ = self.__sock.recvfrom(18)
        r_packet = HandhakeResponse.create_from(data)
        
        # Check type and session id
        if r_packet.type != 9 or r_packet.id != packet.id:
            raise Exception("Error while getting the handshake")

        # Parse token to bytes
        self.__token = r_packet.token

    def _basic_stats(self):
        packet = BasicStatsRequest(token=self.__token,id=self.__session_id)
        self.__sock.sendto(bytes(packet), self.__host)

        data, _ = self.__sock.recvfrom(4096)
        r_packet = BasicStatsResponse.create_from(data)

        # Check type and session id
        if r_packet.type != 0 or r_packet.id != packet.id:
            raise Exception("Error while getting basic stats")

        return r_packet

    def _full_stats(self):
        packet = FullStatsRequest(token=self.__token,id=self.__session_id)
        self.__sock.sendto(bytes(packet), self.__host)

        buffer_list = []

        while 1:
            data, _ = self.__sock.recvfrom(4096)
            buffer_list.append(data)
            r_packet = FullStatsResponse.create_from(data)

            # Check type and session id
            if r_packet.type != 0 or r_packet.id != packet.id:
                raise Exception("Error while getting full stats")

            if r_packet.is_last_packet:
                break
        return FullStatsResponse.create_from(buffer_list)

    def stats(self, full=False):
        if full:
            return self._full_stats()
        else:
            return self._basic_stats()
