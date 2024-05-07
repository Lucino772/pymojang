import json
import socket
import struct
import time
from typing import Optional

from .._structures import Players, SLPResponse
from .packets import Packets
from .types import String, VarInt


def ping(
    sock: socket.socket,
    hostname: str = "locahost",
    port: int = 25565,
) -> SLPResponse:
    pcks = Packets(sock)

    # Send handshake packet
    with pcks.send() as buffer:
        VarInt.write(buffer, 0x00)
        VarInt.write(buffer, 0)
        String.write(buffer, hostname)
        buffer.write(struct.pack(">H", port))
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
        buffer.write(struct.pack(">q", int(time.time() * 1000)))

    # Pong
    with pcks.recv() as buffer:
        _ = VarInt.read(buffer)
        ping_start = struct.unpack(">q", buffer.read(8))[0]

    players = Players((-1, -1), [])
    if "players" in response:
        players = Players(
            (
                int(response["players"]["online"]),
                int(response["players"]["max"]),
            ),
            response["players"].get("sample", []),
        )

    print(response)

    return SLPResponse(
        protocol_version=response.get("version", {}).get(
            "protocol", "unknown"
        ),
        version=response.get("version", {}).get("name", "unknown"),
        motd=response.get("description", None),
        players=players,
        ping=(time.time() * 1000) - ping_start,
    )
