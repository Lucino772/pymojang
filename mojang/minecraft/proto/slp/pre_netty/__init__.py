import socket
import struct
import time
from typing import Optional

from .._structures import Players, SLPResponse


def ping_fe01(sock: socket.socket, hostname: Optional[str] = None, port: Optional[int] = -1):
    if hostname is not None and len(hostname) > 0 and port > 0:
        encoded_hostname = hostname.encode('utf-16be')
        packet = struct.pack(
            f'>BBBh22shBh{len(encoded_hostname)}si',
            0xFE, 0x01, 0xFA,                           # Packet info
            11, 'MC|PingHost'.encode('utf-16be'),       # MC|Pingost
            7 + len(encoded_hostname),                  # Length of data
            80, len(hostname), encoded_hostname, port   # Data
        )
    else:
        packet = struct.pack('>BB', 0xFE, 0x01)

    start = time.time() * 1000
    sock.send(packet)

    with sock.makefile('rb') as buffer:
        buffer.read1(9) # Skip 9 first bytes
        resp = buffer.read().decode('utf-16-be').split('\x00')
    
    latency = (time.time() * 1000) - start

    return SLPResponse(
        protocol_version=resp[0], 
        version=resp[1], 
        motd=resp[2],
        players=Players((int(resp[3]), int(resp[4])), []),
        ping=latency
    )


def ping_fe(sock: socket.socket):
    start = time.time() * 1000
    sock.send(struct.pack('>B', 0xFE))

    with sock.makefile('rb') as buffer:
        buffer.read(3) # Skip 3 first bytes
        resp = buffer.read().decode('utf-16-be').split('\xa7')
    
    latency = (time.time() * 1000) - start

    return SLPResponse(
        protocol_version=None, 
        version=None, 
        motd=resp[0],
        players=Players((int(resp[1]), int(resp[2])), []),
        ping=latency
    )
