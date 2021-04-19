import struct
import socket
import select

from ..common.packet import Packet
from .packets.login import LoginRequest, LoginResponse
from .packets.command import CommandRequest, CommandResponse

class RconClient:

    def __init__(self, host: str, port: int, password: str):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = (host, port)
        self.__password = password

        self.__id__ = 0

    @property
    def _new_id(self):
        self.__id__ += 1
        return self.__id__

    def _recv(self, cls: Packet = None):
        if select.select([self.__sock], [], [], 1)[0]:
            with self.__sock.makefile('rb') as stream:
                packet_length = struct.unpack('<i', stream.read(4))[0]
                
                data = b''
                while len(data) < packet_length:
                    _data = stream.read(packet_length - len(data))
                    if _data:
                        data += _data
            if cls:
                return cls.create_from(data)
            else:
                return data

    def _send(self, packet: Packet):
        if select.select([], [self.__sock], [], 1)[1]:
            with self.__sock.makefile('wb') as stream:
                data = bytes(packet)
                stream.write(struct.pack('<i', len(data)))
                stream.write(data)
                    
    def connect(self):
        self.__sock.connect(self.__host)
        self.__sock.setblocking(False)
        self._authenticate()
    
    def _authenticate(self):
        packet = LoginRequest(id=self._new_id, payload=self.__password)
        self._send(packet)

        r_packet = self._recv(LoginResponse)

        if r_packet.type != 2 or r_packet.id == -1:
            raise Exception('Authentication Failed !')

    def run_cmd(self, cmd: str):
        packet = CommandRequest(id=self._new_id, payload=cmd)
        self._send(packet)

        response = ''
        try:
            while 1:
                r_packet = self._recv(CommandResponse)
                if r_packet is None:
                    break

                if r_packet.type != 0 or r_packet.id != packet.id:
                    raise Exception('Error while getting the response')

                response += r_packet.payload
        finally:
            return response

    def close(self):
        self.__sock.close()
