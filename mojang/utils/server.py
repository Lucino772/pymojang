import socket
from ..api.net import query, rcon, slp

class Server:

    def __init__(self, hostname: str, port: int, rcon_port=None, rcon_password=None, query_port=None):
        self.__hostname = hostname
        self.__port = port
        self.__rcon_password = rcon_password
        self.__rcon_port = rcon_port
        self.__query_port = query_port

        self.__rcon_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__rcon_sock.settimeout(2)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    # Rcon
    def connect_rcon(self):
        if not self.__rcon_password or not self.__rcon_port:
            raise Exception("Missing rcon port or rcon password")

        self.__rcon_sock.connect((self.__hostname, self.__rcon_port))
        rcon.authenticate(self.__rcon_sock, self.__rcon_password)

    def _close_rcon(self):
        self.__rcon_sock.close()

    def run_cmd(self, command: str):
        return rcon.run_command(self.__rcon_sock, command)

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


    def close(self):
        self._close_rcon()
