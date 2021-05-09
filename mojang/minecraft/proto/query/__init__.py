import io
import socket
import struct
import time
from typing import IO, Tuple, Union

from ._structures import ServerStats


def read_null_terminated_string(buffer: IO, encoding='utf-8'):
    res = b''
    char = buffer.read(1)
    while char != b'\0':
        res += char
        char = buffer.read(1)

    return res.decode(encoding)

def get_session_id():
    return int(time.time()) & 0x0F0F0F0F


def _handshake(sock: socket.socket, addr: Tuple[str, int], session_id: int):
    # Send handshake request
    packet = struct.pack('>Hbi', 0xFEFD, 9, session_id)
    sock.sendto(packet, addr)

    # Receive token
    data = sock.recvfrom(18)[0]
    r_type, r_session_id = struct.unpack('>bi', data[:5])
    token_str = data[5:-1]

    if r_type != 9 or r_session_id != session_id:
        raise Exception('An error occured while handshaking')

    return int(token_str)
    
def _get_stats(sock: socket.socket, addr: Tuple[str, int], session_id: int, token: int):
    # Send request
    packet = struct.pack('>HbiiI', 0xFEFD, 0, session_id, token, 0xFFFFFF01)
    sock.sendto(packet, addr)

    # Receive response
    total_data = b''
    packet_id = 0
    while packet_id != 0x80:
        data = sock.recvfrom(4096)[0]
        r_type, r_session_id, _, packet_id, _ = struct.unpack('>bi9sBb', data[:16])

        if r_type != 0 or r_session_id != session_id:
            raise Exception('An error occured while getting stats')

        total_data += data[16:]

    with io.BytesIO(total_data) as buffer:
        # Read server info
        info = {}
        for _ in range(10):
            key = read_null_terminated_string(buffer)
            value = read_null_terminated_string(buffer)
            info[key] = value

        # TODO: Parse plugins
        info['motd'] = info.pop('hostname')
        info['game_type'] = info.pop('gametype')
        info['players'] = (int(info.pop('numplayers')), int(info.pop('maxplayers')))
        info['host'] = (info.pop('hostip'), int(info.pop('hostport')))
        
        buffer.seek(11, 1) # Skip next 11 bytes
        
        # Read players
        players = []
        player_name = read_null_terminated_string(buffer)
        while len(player_name) != 0:
            players.append(player_name)
            player_name = read_null_terminated_string(buffer)

    return ServerStats(**info, player_list=players)

def get_stats(addr: Tuple[str, int], session_id: int = None, timeout: float = 3) -> ServerStats:
    """Returns full stats about server using the Query protocol

    Args:
        addr (tuple): tuple with the address and the port to connect to
        session_id (int, optional): A session id used for the requests (default to None)
        timeout (int, optional): Time to wait before closing pending connection (default to 3)
    
    Returns:
        ServerStats

    Example:

        ```python
        from mojang.minecraft import query

        stats = query.get_stats(('localhost', 25585))
        print(stats)
        ```
        ```bash
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
        ```

    """
    session_id = get_session_id() if not session_id else session_id

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as conn:
        conn.settimeout(timeout)

        token = _handshake(conn, addr, session_id)
        stats = _get_stats(conn, addr, session_id, token)

    return stats
