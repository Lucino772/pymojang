import io
import json
import socket
import struct
import time

from .utils import *


def _slp_current(sock: socket.socket, hostname='localhost', port=25565):
    ## Prepare and send handshake
    buffer = io.BytesIO()
    _write_varint(0x00, buffer)
    _write_varint(0x00, buffer)
    _write_string(hostname, buffer)
    _write_short(port,buffer)
    _write_varint(0x01,buffer)

    with sock.makefile('wb') as fp:
        _write_varint(len(buffer.getvalue()), fp)
        fp.write(buffer.getvalue())

    ## Receive server info
    buffer = io.BytesIO()
    _write_varint(0x00, buffer)

    with sock.makefile('wb') as fp:
        _write_varint(len(buffer.getvalue()), fp)
        fp.write(buffer.getvalue())

    with sock.makefile('rb') as fp:
        packet_length = _read_varint(fp)
        packet_id = _read_varint(fp)
        data = json.loads(_read_string(fp))

    ## Ping
    buffer = io.BytesIO()
    _write_varint(0x01, buffer)
    _write_long(int(time.time() * 1000), buffer)

    with sock.makefile('wb') as fp:
        _write_varint(len(buffer.getvalue()), fp)
        fp.write(buffer.getvalue())

    with sock.makefile('rb') as fp:
        packet_length = _read_varint(fp)
        packet_id = _read_varint(fp)
        itime = _read_long(fp)
    
    ping = int(time.time() * 1000) - itime
    return {
        'protocol_version': data['version']['protocol'],
        'version': data['version']['name'],
        'motd': data['description']['text'],
        'players': {
            'count': (data['players']['online'], data['players']['max']),
            'list': data['players'].get('sample', []),
        },
        'ping': ping
    }

def _slp_1_6(sock: socket.socket, hostname='localhost', port=25565):
    # TODO:  Test with a 1.6 server
    # Send request
    header = struct.pack('>BBB', 0xFE, 0x01, 0xFA)
    command = struct.pack('>h22s', 11, 'MC|PingHost'.encode('utf-16be'))
    encoded_hostname = hostname.encode('utf-16be')
    rest = struct.pack('>hBh{}si'.format(len(encoded_hostname)), 7 + len(encoded_hostname), 80, len(hostname), encoded_hostname, port)
    packet = header + command + rest
    
    sock.send(packet)

    d = sock.recv(1024)
    print(d)

def _slp_prior_1_6(sock: socket.socket, **kwargs):
    sock.send(struct.pack('>BB', 0xFE, 0x01))

    with sock.makefile('rb') as fp:
        data = fp.read()
        protocol_ver, version, motd, nplayers, maxplayers = data[9:].decode('utf-16-be').split('\x00')

    return {
        'protocol_version': protocol_ver,
        'version': version,
        'motd': motd,
        'players': {
            'count': (nplayers, maxplayers),
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
            'count': (nplayers, maxplayers),
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
                _slp_result = _slp(sock, hostname=host, port=port)
                
                # Check if version worked
                if _slp_result:
                    result = _slp_result
                    break
        except:
            pass

    return result
