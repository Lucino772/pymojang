import enum
import socket
from functools import partial
from typing import Optional, Tuple

from ._structures import SLPResponse
from .post_netty import ping as mping
from .pre_netty import ping_fe, ping_fe01


class PingVersion(enum.IntFlag):
    """
    :param int V1_7: Use the ping protocol for version 1.7 and higher
    :param int V1_6: Use the ping protocol for version 1.6
    :param int V1_4: Use the ping protocol for version 1.4 and 1.5
    :param int V1_3: Use the ping protocol for version 1.3 and lower
    :param int V_ALL: Use all the ping protocol
    """

    V1_7 = 1
    V1_6 = 2
    V1_4 = 4
    V1_3 = 8
    V_ALL = 15


def ping(
    addr: Tuple[str, int],
    timeout: int = 3,
    flags: int = PingVersion.V_ALL,
) -> Optional[SLPResponse]:
    """Ping the server for information

    :param tuple addr: The address and the port to connect to
    :param int timeout: Time to wait before closing pending connection (default to 3)
    :param int flags: Which version of the ping version to use

    :Example:

    >>> from mojang.minecraft import slp
    >>> slp.ping(('localhost', 25565))
    SLPResponse(
        protocol_version=754,
        version='1.16.5',
        motd='A Minecraft Server',
        players=Players(total=(0, 20), list=[]),
        ping=1
    )
    """
    _methods = []
    if PingVersion.V1_7 & flags:
        _methods.append(partial(mping, hostname=addr[0], port=addr[1]))
    if PingVersion.V1_6 & flags:
        _methods.append(partial(ping_fe01, hostname=addr[0], port=addr[1]))
    if PingVersion.V1_4 & flags:
        _methods.append(partial(ping_fe01))
    if PingVersion.V1_3 & flags:
        _methods.append(partial(ping_fe))

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
