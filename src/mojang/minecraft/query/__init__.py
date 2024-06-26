from __future__ import annotations

import contextlib
import io
import socket
import struct
import time
from typing import IO

from mojang.minecraft.query._structures import ServerStats
from mojang.minecraft.query.packets import Packets


def read_null_terminated_string(buffer: IO, encoding: str = "utf-8") -> str:
    res = b""
    char = buffer.read(1)
    while char != b"\0":
        res += char
        char = buffer.read(1)

    return res.decode(encoding)


def _parse_stats(data: bytes) -> ServerStats:
    with io.BytesIO(data) as buffer:
        # Read server info
        info = {}
        for _ in range(10):
            key = read_null_terminated_string(buffer)
            value = read_null_terminated_string(buffer)
            info[key] = value

        motd = str(info.pop("hostname"))
        game_type = str(info.pop("gametype"))
        game_id = str(info.pop("game_id"))
        version = str(info.pop("version"))
        _map = str(info.pop("map"))
        host = (str(info.pop("hostip")), int(info.pop("hostport")))
        # TODO: Parse plugins
        plugins: list[str] = []
        players = (
            int(info.pop("numplayers")),
            int(info.pop("maxplayers")),
        )

        # Skip next 11 bytes
        buffer.seek(11, 1)

        # Read players
        player_list = []
        player_name = read_null_terminated_string(buffer)
        while len(player_name) != 0:
            player_list.append(player_name)
            player_name = read_null_terminated_string(buffer)

    return ServerStats(
        motd=motd,
        game_type=game_type,
        game_id=game_id,
        version=version,
        map=_map,
        host=host,
        plugins=plugins,
        players=players,
        player_list=player_list,
    )


def _handshake(sock: socket.socket, addr: tuple[str, int], session_id: int) -> int:  # noqa: ARG001
    pcks = Packets(sock)
    pcks.send(9, session_id)

    r_type, r_session_id, data = pcks.recv()
    if r_type != 9 or r_session_id != session_id:  # noqa: PLR2004
        msg = "An error occured while handshaking"
        raise Exception(msg)

    return int(data.rstrip(b"\0"))


def _get_stats(
    sock: socket.socket,
    addr: tuple[str, int],  # noqa: ARG001
    session_id: int,
    token: int,
) -> ServerStats:
    pcks = Packets(sock)
    pcks.send(0, session_id, struct.pack(">iI", token, 0xFFFFFF01))

    total_data = b""
    packet_id = 0
    while packet_id != 0x80:  # noqa: PLR2004
        r_type, r_session_id, data = pcks.recv()
        packet_id = struct.unpack(">9xBx", data[:11])[0]

        if r_type != 0 or r_session_id != session_id:
            msg = "An error occured while getting stats"
            raise Exception(msg)

        total_data += data[11:]

    return _parse_stats(total_data)


def get_stats(addr: tuple[str, int], timeout: float | None = 3) -> ServerStats | None:
    """Returns full stats about server using the Query protocol

    :param tuple addr: tuple with the address and the port to connect to
    :param int timeout: Time to wait before closing pending connection (default to 3)

    :Example:

    >>> from mojang.minecraft import query
    >>> query.get_stats(("localhost", 25585))
    ServerStats(
        motd='A Minecraft Server',
        game_type='SMP',
        game_id='MINECRAFT',
        version='1.16.5',
        map='world',
        host=('localhost', 25585),
        players=(0, 20),
        player_list=[]
    )
    """
    session_id = int(time.time()) & 0x0F0F0F0F

    stats = None
    with contextlib.suppress(socket.timeout), socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM
    ) as sock:
        sock.settimeout(timeout)
        sock.connect(addr)

        token = _handshake(sock, addr, session_id)
        stats = _get_stats(sock, addr, session_id, token)

    return stats
