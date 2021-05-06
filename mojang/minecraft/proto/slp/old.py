import socket
import struct

from ._structures import Players, SLPResponse


def slp_1_6(sock: socket.socket, hostname: str = 'localhost', port: int = 25565):
    # Send request
    encoded_hostname = hostname.encode('utf-16be')
    header = struct.pack('>BBBh22s', 0xFE, 0x01, 0xFA, 11,'MC|PingHost'.encode('utf-16be'))
    body = struct.pack('>hBh{}si'.format(len(encoded_hostname)), 7 + len(encoded_hostname), 80, len(hostname), encoded_hostname, port)
    packet = header + body

    sock.send(packet)

    # Receive response
    with sock.makefile('rb') as buffer:
        buffer.read(9) # Skip 9 first bytes
        protocol_ver, version, motd, nplayers, maxplayers = buffer.read().decode('utf-16-be').split('\x00')
    
    return SLPResponse(
        protocol_version=protocol_ver, 
        version=version, 
        motd=motd,
        players=Players((int(nplayers), int(maxplayers)), []),
        ping=None
    )

def slp_prior_1_6(sock: socket.socket, *args):
    sock.send(struct.pack('>BB', 0xFE, 0x01))

    with sock.makefile('rb') as buffer:
        buffer.read(9) # Skip 9 first bytes
        protocol_ver, version, motd, nplayers, maxplayers = buffer.read().decode('utf-16-be').split('\x00')
    
    return SLPResponse(
        protocol_version=protocol_ver, 
        version=version, 
        motd=motd,
        players=Players((int(nplayers), int(maxplayers)), []),
        ping=None
    )

def slp_prior_1_4(sock: socket.socket, *args):
    sock.send(struct.pack('>B', 0xFE))

    with sock.makefile('rb') as buffer:
        buffer.read(3) # Skip 3 first bytes
        motd, nplayers, maxplayers = buffer.read().decode('utf-16-be').split('\xa7')
    
    return SLPResponse(
        protocol_version=None, 
        version=None, 
        motd=motd,
        players=Players((int(nplayers), int(maxplayers)), []),
        ping=None
    )
