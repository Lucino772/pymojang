import json
import socket
import struct
import time
from typing import Optional

from .._structures import Players, SLPResponse
from .packets import Packets
from .types import String, VarInt


def ping(sock: socket.socket, hostname: Optional[str] = 'locahost', port: Optional[int] = 25565) -> SLPResponse:
    pcks = Packets(sock)

    # Send handshake packet    
    with pcks.send() as buffer:
        VarInt.write(buffer, 0x00)
        VarInt.write(buffer, 0)
        String.write(buffer, hostname)
        buffer.write(struct.pack('>H', port))
        VarInt.write(buffer, 0x01)

    # Send request packet
    with pcks.send() as buffer:
        VarInt.write(buffer, 0x00)
    
    # Receive response
    with pcks.recv() as buffer:
        _ = VarInt.read(buffer)
        response = json.loads(String.read(buffer))

    # Ping
    with pcks.send() as buffer:
        VarInt.write(buffer, 0x01)
        buffer.write(struct.pack('>q', int(time.time() * 1000)))
    
    # Pong
    with pcks.recv() as buffer:
        _ = VarInt.read(buffer)
        ping_start = struct.unpack('>q', buffer.read(8))[0]

    players = None
    if 'players' in response:
        players = Players(
            (response['players']['online'], response['players']['max']), 
            response['players'].get('sample', []))


    return SLPResponse(
        protocol_version=response.get('version', {}).get('protocol', 'unknown'), 
        version=response.get('version', {}).get('name', 'unknown'), 
        motd=response.get('description', {}).get('text', 'unknown'),
        players=players,
        ping=(time.time() * 1000) - ping_start
    )
