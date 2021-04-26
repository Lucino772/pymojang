import io
import json
import socket
import struct
import time

from .packets.types import VarInt
from .packets.current import SLPCurrentHandshakePacket, SLPCurrentRequestPacket, SLPCurrentResponsePacket
from .packets.ping import SLPPingPacket, SLPPongPacket

def _slp_current(sock: socket.socket, hostname='localhost', port=25565):
    # Send handshake
    packet = SLPCurrentHandshakePacket(proto_version=0, server_address=hostname, server_port=port, next_state=0x01)
    with sock.makefile('wb') as buffer:
        VarInt().write(len(packet.data), buffer)
        packet.write(buffer)
    
    # Send request
    packet = SLPCurrentRequestPacket()
    with sock.makefile('wb') as buffer:
        VarInt().write(len(packet.data), buffer)
        packet.write(buffer)

    # Receive response
    with sock.makefile('rb') as buffer:
        length = VarInt().read(buffer)
        rpacket = SLPCurrentResponsePacket.from_bytes(buffer.read(length))

    # Ping-Pong
    packet = SLPPingPacket(payload=int(time.time() * 1000))
    with sock.makefile('wb') as buffer:
        VarInt().write(len(packet.data), buffer)
        packet.write(buffer)

    with sock.makefile('rb') as buffer:
        length = VarInt().read(buffer)
        pong_packet = SLPPongPacket.from_bytes(buffer.read(length))

    return {
        'protocol_version': int(rpacket.response['version']['protocol']),
        'version': rpacket.response['version']['name'],
        'motd': rpacket.response['description']['text'],
        'players': {
            'count': (int(rpacket.response['players']['online']), int(rpacket.response['players']['max'])),
            'list': rpacket.response['players'].get('sample', [])
        },
        'ping': int(time.time() * 1000) - pong_packet.payload
    }

def _slp_1_6(sock: socket.socket, hostname='localhost', port=25565):
    # Send request
    header = struct.pack('>BBB', 0xFE, 0x01, 0xFA)
    command = struct.pack('>h22s', 11, 'MC|PingHost'.encode('utf-16be'))
    encoded_hostname = hostname.encode('utf-16be')
    rest = struct.pack('>hBh{}si'.format(len(encoded_hostname)), 7 + len(encoded_hostname), 80, len(hostname), encoded_hostname, port)
    packet = header + command + rest
    
    sock.send(packet)

    with sock.makefile('rb') as fp:
        data = fp.read()
        protocol_ver, version, motd, nplayers, maxplayers = data[9:].decode('utf-16-be').split('\x00')
    
    return {
        'protocol_version': int(protocol_ver),
        'version': version,
        'motd': motd,
        'players': {
            'count': (int(nplayers), int(maxplayers)),
            'list': []
        },
        'ping': None
    }

def _slp_prior_1_6(sock: socket.socket, **kwargs):
    sock.send(struct.pack('>BB', 0xFE, 0x01))

    with sock.makefile('rb') as fp:
        data = fp.read()
        protocol_ver, version, motd, nplayers, maxplayers = data[9:].decode('utf-16-be').split('\x00')

    return {
        'protocol_version': int(protocol_ver),
        'version': version,
        'motd': motd,
        'players': {
            'count': (int(nplayers), int(maxplayers)),
            'list': []
        },
        'ping': None
    }

def _slp_prior_1_4(sock: socket.socket, **kwargs):
    sock.send(struct.pack('>B', 0xFE))

    with sock.makefile('rb') as fp:
        data = fp.read()
        motd, nplayers, maxplayers = data[3:].decode('utf-16-be').split('\xa7')
    
    return {
        'protocol_version': None,
        'version': None,
        'motd': motd,
        'players': {
            'count': (int(nplayers), int(maxplayers)),
            'list': []
        },
        'ping': None
    }


def ping(host: str, port: int):
    result = None
    _versions = [_slp_current, _slp_1_6, _slp_prior_1_6, _slp_prior_1_4]

    while len(_versions) > 0:
        _slp = _versions.pop(0)

        try:
            # Try a slp version
            with socket.socket() as sock:
                sock.connect((host, port))
                sock.settimeout(2)
                _slp_result = _slp(sock, hostname=host, port=port)
                
                # Check if version worked
                if _slp_result:
                    result = _slp_result
                    break
        except:
            pass

    return result
