from __future__ import annotations

from typing import NamedTuple


class Players(NamedTuple):
    total: tuple[int, int]
    list: list[str]


class SLPResponse(NamedTuple):
    protocol_version: int
    version: str
    motd: str
    players: Players
    ping: float
