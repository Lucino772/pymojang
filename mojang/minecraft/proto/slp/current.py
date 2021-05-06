import socket
import struct
import io
import time
import json
from typing import IO

from ._structures import SLPResponse, Players

# Types helper
def _write_varint(buffer: IO, value: int):
    while True:
        byte = value & 0x7f
        value >>= 7

        if value > 0:
            byte |= 0x80
        
        buffer.write(struct.pack('B', byte))
        
        if value == 0:
            break

def _read_varint(buffer: IO):
    val = 0

    for i in range(5):
        byte = buffer.read(1)
        if len(byte) == 0:
            break

        val |= (ord(byte) & 0x7f) << (7*i)
        
        if ord(byte) & 0x80 == 0:
            break

    return val

def _write_string(buffer: IO, value: str, encoding: str = 'utf-8'):
    value = value.encode(encoding)
    _write_varint(buffer, len(value))
    buffer.write(value)

def _read_string(buffer: IO, encoding: str = 'utf-8'):
    length = _read_varint(buffer)
    return buffer.read(length).decode(encoding)

# Packet helper
def _write_packet(sock: socket.socket, packet: bytes):
    with sock.makefile('wb') as buffer:
        _write_varint(buffer, len(packet))
        buffer.write(packet)

def _read_packet(sock: socket.socket):
    with sock.makefile('rb') as buffer:
        length = _read_varint(buffer)
        packet = buffer.read(length)

    return packet


def slp(sock: socket.socket, hostname: str = 'locahost', port: int = 25565):
    # Send handshake packet
    with io.BytesIO() as buffer:
        _write_varint(buffer, 0x00)
        _write_varint(buffer, 0)
        _write_string(buffer, hostname)
        buffer.write(struct.pack('>h', port))
        _write_varint(buffer, 0x01)

        _write_packet(sock, buffer.getvalue())
        
    # Send request packet
    with io.BytesIO() as buffer:
        _write_varint(buffer, 0x00)

        _write_packet(sock, buffer.getvalue())
    
    # Receive response
    packet = _read_packet(sock)    
    with io.BytesIO(packet) as buffer:
        packet_id = _read_varint(buffer)
        response = json.loads(_read_string(buffer))
    
    # Ping
    with io.BytesIO() as buffer:
        _write_varint(buffer, 0x01)
        buffer.write(struct.pack('>q', int(time.time() * 1000)))

        _write_packet(sock, buffer.getvalue())
    
    # Pong
    packet = _read_packet(sock)
    with io.BytesIO(packet) as buffer:
        packet_id = _read_varint(buffer)
        ping_start = struct.unpack('>q', buffer.read(8))[0]
    
    return SLPResponse(
        protocol_version=response['version']['protocol'], 
        version=response['version']['name'], 
        motd=response['description']['text'],
        players=Players((response['players']['online'], response['players']['max']), response['players'].get('sample', [])),
        ping=int(time.time() * 1000) - ping_start
    )
