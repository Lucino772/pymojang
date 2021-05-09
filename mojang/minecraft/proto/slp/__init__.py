import socket
from typing import Tuple

from ._structures import SLPResponse
from .current import slp
from .old import slp_1_6, slp_prior_1_4, slp_prior_1_6


def ping(addr: Tuple[str, int], timeout: int = 3) -> SLPResponse:
    """Ping the server for information

    Args:
        addr (tuple): The address and the port to connect to
        timeout (int, optional): Time to wait before closing pending connection (default to 3) 

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
    response = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(addr)
        sock.settimeout(timeout)

        _methods = [slp, slp_1_6, slp_prior_1_6, slp_prior_1_6]
        while len(_methods) > 0 and response is None:
            method = _methods.pop(0)
            try:
                response = method(sock, addr[0], addr[1])
            except socket.error:
                pass
        
    return response
                