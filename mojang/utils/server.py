import socket
from ..api.net import query, slp
from ..api.net.rcon import RconClient

class Server:

    def __init__(self, hostname: str, port: int, rcon_port=None, rcon_password=None, query_port=None):
        self.__hostname = hostname
        self.__port = port
        self.__rcon_client = RconClient(self.__hostname, rcon_port, rcon_password)
        self.__query_port = query_port

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.__rcon_client.close()

    # Rcon
    def connect_rcon(self):
        self.__rcon_client.connect()

    def run_cmd(self, command: str):
        return self.__rcon_client.run_cmd(command)

    # Query
    def get_stats(self, full=False):
        if not self.__query_port:
            raise Exception("Missing query port")

        stats = None
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(2)
            token = query.handshake(sock, (self.__hostname, self.__query_port))
            if not full:
                stats = query.basic_stats(sock, (self.__hostname, self.__query_port), token)
            else:
                stats = query.full_stats(sock, (self.__hostname, self.__query_port), token)

        return stats

    # SLP
    def ping(self):
        return slp.ping(self.__hostname, self.__port)

