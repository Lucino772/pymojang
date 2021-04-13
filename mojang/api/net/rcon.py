import struct
import enum
import socket
import time

class RconPacketTypes(enum.IntEnum):
    SERVERDATA_AUTH = 3
    SERVERDATA_EXECOMMAND = 2
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_RESPONSE_VALUE = 0


def _request_id():
    return int(time.time())

def _write_packet(sock: socket.socket, _type: int, payload: str):
    # Prepare packet
    req_id = _request_id()
    packet = struct.pack('<ii{}s2s'.format(len(payload)), req_id, _type, payload.encode('ascii'), b'\0\0')
    header = struct.pack('<i', len(packet))

    # Send packet
    data_sent = sock.send(header + packet)
    return req_id, data_sent

def _read_packet(sock: socket.socket):
    # Recv data
    length_bytes = sock.recv(4)
    length = struct.unpack('<i', length_bytes)[0]
    data = bytes()

    # Ensure that all the data was read
    while length > len(data):
        data += sock.recv(length - len(data))

    # Parse data
    r_req_id, r_type, payload = struct.unpack('<ii{}s'.format(len(data) - 8), data)
    return r_req_id, r_type, payload

def authenticate(sock: socket.socket, password: str):
    req_id = _write_packet(sock, RconPacketTypes.SERVERDATA_AUTH, password)[0]

    r_req_id, r_type, _ = _read_packet(sock)

    if r_type != RconPacketTypes.SERVERDATA_AUTH_RESPONSE or r_req_id == -1:
        raise Exception('Authentication failed')

def run_command(sock: socket.socket, command: str):
    req_id = _write_packet(sock, RconPacketTypes.SERVERDATA_EXECOMMAND, command)[0]

    fpayload = bytes()
    try:
        # Receive message until no more
        while 1:
            r_req_id, r_type, payload = _read_packet(sock)

            if r_type != RconPacketTypes.SERVERDATA_RESPONSE_VALUE or r_req_id != req_id:
                raise Exception('Error occured while executing a command')

            fpayload += payload
    finally:
        return fpayload.decode('ascii')
