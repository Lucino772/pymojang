import struct

from .base import Packet

class BasicStatsRequest(Packet):
    magic: int = 0xFEFD
    type: int = 0
    id: int
    token: int

    def _bytes(self):
        return struct.pack('>Hbii', self.magic, self.type, self.id, self.token)

class BasicStatsResponse(Packet):
    type: int
    id: int
    motd: str
    game_type: str
    map: str
    players: tuple
    host: tuple

    @classmethod
    def _parse(cls, buffer: bytes):
        _type, _id, payload = struct.unpack('>bi{}s'.format(len(buffer) - 5), buffer)

        # Parse payload
        motd, game_type, _map, n_players, max_players, host = payload.strip(b'\0').split(b'\0')
        host_port, host_ip = struct.unpack('<h{}s'.format(len(host) - 2), host)

        return {
            'type': _type,
            'id': _id,
            'motd': motd.decode('ascii'),
            'game_type': game_type.decode('ascii'),
            'map': _map.decode('ascii'),
            'players': (int(n_players), int(max_players)),
            'host': (host_port, host_ip.decode('ascii'))
        }


class FullStatsRequest(Packet):
    magic: int = 0xFEFD
    type: int = 0
    padding: int = 0xFFFFFF01
    id: int
    token: int

    def _bytes(self):
        return struct.pack('>HbiiI', self.magic, self.type, self.id, self.token, self.padding)

class FullStatsResponse(Packet):
    type: int
    id: int
    is_last_packet: bool
    hostname: str
    game_type: str
    game_id: str
    version: str
    plugins: list
    map: str
    players: tuple
    host: tuple
    player_list: list

    @classmethod
    def _parse(cls, buffer: bytes):
        payload = b''
        if isinstance(buffer, list):
            for _bytes in buffer:
                _type, _id, _, last_packet, _, _payload = struct.unpack('>bi9sBb{}s'.format(len(_bytes) - 16), _bytes)
                is_last_packet = last_packet == 0x80

                payload += _payload
        elif isinstance(buffer, bytes):
            _type, _id, _, last_packet, _, payload = struct.unpack('>bi9sBb{}s'.format(len(buffer) - 16), buffer)
            is_last_packet = last_packet == 0x80

            if not is_last_packet:
                return dict(type=_type, id=_id, is_last_packet=is_last_packet)
        
        server_info, player_info = payload.split(b'\x01\x70\x6C\x61\x79\x65\x72\x5F\x00\x00')
        key_values = server_info.strip(b'\0').split(b'\0')
        players = player_info.strip(b'\0').split(b'\0')

        info = dict([(key_values[i].decode('ascii'), key_values[i+1].decode('ascii')) for i in range(0, len(key_values), 2)])
        player_list = [player.decode('ascii') for player in players if len(player) > 0]
        return {
            'type': _type,
            'id': _id,
            'is_last_packet': is_last_packet,
            'hostname': info['hostname'],
            'game_type': info['gametype'],
            'game_id': info['game_id'],
            'version': info['version'],
            'plugins': info['plugins'].split(':'),
            'map': info['map'],
            'players': (int(info['numplayers']), int(info['maxplayers'])),
            'host': (info['hostip'], int(info['hostport'])),
            'player_list': player_list
        }
