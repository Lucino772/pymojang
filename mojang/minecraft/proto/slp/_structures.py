from dataclasses import dataclass, field
from typing import Tuple, List

@dataclass(frozen=True)
class Players:
    count: Tuple[int, int] = field()
    list: List[str] = field()

@dataclass(frozen=True)
class SLPResponse:
    protocol_version: int = field()
    version: str = field()
    motd: str = field()
    players: Players = field()
    ping: int = field()
