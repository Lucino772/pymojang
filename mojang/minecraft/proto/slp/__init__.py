import socket
from typing import Tuple

from .current import slp
from .old import slp_1_6, slp_prior_1_4, slp_prior_1_6


def ping(addr: Tuple[str, int], timeout: int = 3):
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
                