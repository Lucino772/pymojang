from typing import List, NamedTuple, Tuple


class Players(NamedTuple):
    total: Tuple[int, int]
    list: List[str]


class SLPResponse(NamedTuple):
    protocol_version: int
    version: str
    motd: str
    players: Players
    ping: float
