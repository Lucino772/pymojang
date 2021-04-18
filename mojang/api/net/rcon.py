import struct
import enum
import socket
import select

class RconPacketTypes(enum.IntEnum):
    SERVERDATA_AUTH = 3
    SERVERDATA_EXECOMMAND = 2
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_RESPONSE_VALUE = 0


class RconPacket:
    __id__ = 0
    id: int
    type: int
    payload: str

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        if len(args) == 1:
            req_id, _type, payload = struct.unpack_from('<ii{}s'.format(len(args[0]) - 10), args[0])
            setattr(obj, 'id', req_id)
            setattr(obj, 'type', _type)
            setattr(obj, 'payload', payload.decode('ascii'))
        elif len(kwargs) >= 2:
            setattr(obj, 'id', kwargs.get('id', cls.get_id()))
            setattr(obj, 'type', kwargs['type'])
            setattr(obj, 'payload', kwargs['payload'])
        else:
            raise Exception('Wrong arguments')

        return obj

    @classmethod
    def get_id(cls):
        cls.__id__ += 1
        return cls.__id__

    @property
    def data(self):
        data = struct.pack('<ii{}s2s'.format(len(self.payload)), self.id, self.type, self.payload.encode('ascii'), b'\0\0')
        return data


class RconClient:

    def __init__(self, host: str, port: int, password: str):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = (host, port)
        self.__password = password

    def _recv(self):
        if select.select([self.__sock], [], [], 2)[0]:
            with self.__sock.makefile('rb') as stream:
                packet_length = struct.unpack('<i', stream.read(4))[0]
                
                data = b''
                while len(data) < packet_length:
                    _data = stream.read(packet_length - len(data))
                    if _data:
                        data += _data

            return RconPacket(data)

    def _send(self, packet: RconPacket):
        if select.select([], [self.__sock], [], 2)[1]:
            with self.__sock.makefile('wb') as stream:
                stream.write(struct.pack('<i', len(packet.data)))
                stream.write(packet.data)
                    
    def connect(self):
        self.__sock.connect(self.__host)
        self.__sock.setblocking(False)
        self._authenticate()
    
    def _authenticate(self):
        packet = RconPacket(type=RconPacketTypes.SERVERDATA_AUTH, payload=self.__password)
        self._send(packet)

        r_packet = self._recv()

        if r_packet.type != RconPacketTypes.SERVERDATA_AUTH_RESPONSE or r_packet.id == -1:
            raise Exception('Authentication Failed !')

    def run_cmd(self, cmd: str):
        packet = RconPacket(type=RconPacketTypes.SERVERDATA_EXECOMMAND, payload=cmd)
        self._send(packet)

        response = ''
        try:
            while 1:
                r_packet = self._recv()
                if r_packet is None:
                    break

                if r_packet.type != RconPacketTypes.SERVERDATA_RESPONSE_VALUE or r_packet.id != packet.id:
                    raise Exception('Error while getting the response')

                response += r_packet.payload
        finally:
            return response

    def close(self):
        self.__sock.close()
