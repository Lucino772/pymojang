import socket
from contextlib import contextmanager
from typing import Callable, Optional, Tuple

from .packets import Packets


@contextmanager
def session(addr: Tuple[str, int], password: str, timeout: Optional[float] = 3) -> Callable[[str], str]:
    """Open a RCON connection

    Args:
        addr (tuple): The address and the port to connect to
        password (str): The RCON password set in the server properties
        timeout (int, optional): Time to wait before closing pending connection (default to 3) 

    Returns:
        A function to send command
        
    Example:

        ```python
        from mojang.minecraft import rcon

        with rcon.session(('localhost', 25575), 'my_super_password') as send:
            result = send('help') # This execute the /help command
        ```

    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect(addr)
    pcks = Packets(sock)

    packet_id = pcks.send(3, password)[0]
    r_packet_id, r_type = pcks.recv()[:2]

    # Check packet id and packet type
    if r_packet_id != packet_id or r_type != 2:
        raise Exception('Authentication failed')

    def send(command: str):
        # TODO: Parse command response
        packet_id = pcks.send(2, command)[0]
        r_packet_id, r_type, payload, size = pcks.recv()

        # Check packet id and packet type
        if r_packet_id != packet_id or r_type != 0:
            raise Exception('Command error')

        return payload.strip(b'\0').decode('ascii')

    try:
        yield send
    finally:
        sock.close()
