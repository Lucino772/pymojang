import socket
from functools import partial
from typing import Tuple

from ._structures import SLPResponse
from .post_netty import ping as mping
from .pre_netty import ping_fe, ping_fe01

V1_7 = 1
V1_6 = 2
V1_4 = 4
V1_3 = 8
V_ALL = V1_7 | V1_6 | V1_4 | V1_3

def ping(addr: Tuple[str, int], timeout: int = 3, flags: int = V_ALL) -> SLPResponse:
    """Ping the server for information

    Args:
        addr (tuple): The address and the port to connect to
        timeout (int, optional): Time to wait before closing pending connection (default to 3) 
        flags (int, optional): Which version of the ping version to use

    Returns:
        SLPResponse

    Example:

        ```python
        from mojang.minecraft import slp

        stats = slp.ping(('localhost', 25565))
        print(stats)
        ```
        ```bash
        SLPResponse(
            protocol_version=754,
            version='1.16.5', 
            motd='A Minecraft Server', 
            players=Players(count=(0, 20), list=[]),
            ping=1
        )
        ```

    """
    _methods = []
    if V1_7 & flags:
        _methods.append(partial(mping, hostname=addr[0], port=addr[1]))
    if V1_6 & flags:
        _methods.append(partial(ping_fe01, hostname=addr[0], port=addr[1]))
    if V1_4 & flags:
        _methods.append(ping_fe01)
    if V1_3 & flags:
        _methods.append(ping_fe)

    response = None
    while len(_methods) > 0 and response is None:
        method = _methods.pop(0)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            try:
                sock.connect(addr)
                response = method(sock)
            except socket.error:
                pass
    
    return response
        