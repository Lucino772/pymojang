import random
import socket
import struct
from contextlib import contextmanager
from typing import IO, Tuple, Callable, Any


def get_request_id():
    return random.randint(0,2**31)

def _read_fully(buffer: IO, length: int):
    data = buffer.read(length)
    
    while len(data) < length:
        _data =  buffer.read(length - len(data))
        if _data:
            data += _data

    return data

def _write_packet(sock: socket.socket, packet_type: int, payload: str):
    packet_id = get_request_id()
    payload = payload.encode('ascii') + b'\00'
    packet = struct.pack('<ii{}s'.format(len(payload)), packet_id, packet_type, payload)

    with sock.makefile('wb') as buffer:
        buffer.write(len(packet).to_bytes(4, 'little'))
        buffer.write(packet)

    return packet_id


@contextmanager
def session(addr: Tuple[str, int], password: str, timeout: float = 3) -> Callable[[str], Any]:
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

    # Send login request
    packet_id = _write_packet(sock, 3, password)

    # Receive login response
    with sock.makefile('rb') as buffer:
        length = int.from_bytes(buffer.read(4), 'little')
        r_packet_id, r_type = struct.unpack_from('<ii', buffer.read(length))
    
    # Check packet id and packet type
    if r_packet_id != packet_id or r_type != 2:
        raise Exception('Authentication failed')

    def send(command: str):
        # TODO: Parse command and command response

        # Send command
        packet_id = _write_packet(sock, 2, command)

        # Receive response
        with sock.makefile('rb') as buffer:
            length = int.from_bytes(buffer.read(4), 'little')
            r_packet_id, r_type, payload = struct.unpack_from('<ii{}s'.format(length-10), _read_fully(buffer, length))
        
        # Check packet id and packet type
        if r_packet_id != packet_id or r_type != 0:
            raise Exception('Command error')

        return payload.decode('ascii')
    
    try:
        yield send
    finally:
        sock.close()
