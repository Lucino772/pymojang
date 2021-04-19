import socket
from ..api.net import slp
from ..api.net.query import QueryClient
from ..api.net.rcon import RconClient

class Server:

    def __init__(self, hostname: str, port: int, rcon_port=None, rcon_password=None, query_port=None):
        self.__hostname = hostname
        self.__port = port
        self.__rcon_client = None
        self.__query_client = None
        if rcon_port and rcon_password:
            self.__rcon_client = RconClient(self.__hostname, rcon_port, rcon_password)
        if query_port:
            self.__query_client = QueryClient(self.__hostname, query_port)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        if self.__rcon_client:
            self.__rcon_client.close()

    # Rcon
    def connect_rcon(self):
        if self.__rcon_client:
            self.__rcon_client.connect()

    def run_cmd(self, command: str):
        if self.__rcon_client:
            return self.__rcon_client.run_cmd(command)

    # Query
    def get_stats(self, full=False):
        if self.__query_client:
            return self.__query_client.stats(full)

    # SLP
    def ping(self):
        return slp.ping(self.__hostname, self.__port)

