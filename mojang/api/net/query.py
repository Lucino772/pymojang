import enum
import struct
import socket
import time

MAGIC = 0xFEFD
PADDING = 0xFFFFFF01
LAST_PACKET = 0x80
SPLIT_PADDING = b'\x01\x70\x6C\x61\x79\x65\x72\x5F\x00\x00'


class QueryPacketTypes(enum.IntEnum):
    HANDSHAKE = 9
    STAT = 0


def _session_id():
    return int(time.time()) & 0x0F0F0F0F

def handshake(sock: socket.socket, address: tuple):
    # Send request
    sess_id = _session_id()
    packet = struct.pack('>Hbi', MAGIC, QueryPacketTypes.HANDSHAKE, sess_id)
    sock.sendto(packet, address)

    # Receive response
    data,_ = sock.recvfrom(18)
    r_type, r_sess_id, payload = struct.unpack('>bi{}s'.format(len(data) - 5), data)
    
    # Check type and session id
    if r_type != QueryPacketTypes.HANDSHAKE or r_sess_id != sess_id:
        raise Exception("Error while getting the handshake")

    # Parse token
    token = int(payload.split(b'\0')[0])
    return token

def basic_stats(sock: socket.socket, address: tuple, token: int):
    # Send request
    sess_id = _session_id()
    packet = struct.pack('>Hbii', MAGIC, QueryPacketTypes.STAT, sess_id, token)
    sock.sendto(packet, address)

    # Receive response
    data,_ = sock.recvfrom(4096)
    r_type, r_sess_id, payload = struct.unpack('>bi{}s'.format(len(data) - 5), data)
    
    # Check type and session id
    if r_type != QueryPacketTypes.STAT or r_sess_id != sess_id:
        raise Exception("Error while getting basic stats")

    # Parse the data
    items = payload.rstrip(b'\0').split(b'\0')
    items[-1:] = struct.unpack('<h{}s'.format(len(items[-1]) - 2), items[-1])
    motd, gtype, gmap, nplayers, maxplayers, hostp, hostip = items

    # Return response
    return {
        'motd': motd.decode('ascii'),
        'game_type': gtype.decode('ascii'),
        'map': gmap.decode('ascii'),
        'n_players': (int(nplayers), int(maxplayers)),
        'host': (hostip.decode('ascii'), hostp)
    }

def full_stats(sock: socket.socket, address: tuple, token: int):
    # Send request
    sess_id = _session_id()
    packet = struct.pack('>HbiiI', MAGIC, QueryPacketTypes.STAT, sess_id, token, PADDING)
    sock.sendto(packet, address)

    # Receive response
    fpayload = bytes()
    while 1:
        data,_ = sock.recvfrom(4096)
        r_type, r_sess_id, _, r_last_pkt, _, payload = struct.unpack('>bi9sBb{}s'.format(len(data) - 16), data)
        
        # Check type and session id
        if r_type != QueryPacketTypes.STAT or r_sess_id != sess_id:
            raise Exception("Error while getting full stats")

        # Add data and check if end
        fpayload += payload
        if r_last_pkt == LAST_PACKET:
            break

    # Parse data
    info, players = fpayload.split(SPLIT_PADDING)
    split_info = info.rstrip(b'\0').split(b'\0')
    split_players = players.rstrip(b'\0').split(b'\0')

    info = dict([(split_info[i].decode('ascii'), split_info[i+1]) for i in range(0, len(split_info), 2)])
    players = [p.decode('ascii') for p in split_players if p]

    # Return response
    return {
        'motd': info['hostname'].decode('ascii'),
        'game_type': info['gametype'].decode('ascii'),
        'game_id': info['game_id'].decode('ascii'),
        'version': info['version'].decode('ascii'),
        'plugins': info['plugins'].decode('ascii'),
        'map': info['map'].decode('ascii'),
        'n_players': (int(info['numplayers']), int(info['maxplayers'])),
        'host': (info['hostip'].decode('ascii'), int(info['hostport'])),
        'players': players 
    }
