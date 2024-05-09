from __future__ import annotations

from typing import NamedTuple


class ServerStats(NamedTuple):
    motd: str
    game_type: str
    game_id: str
    version: str
    map: str
    host: tuple[str, int]
    plugins: list[str]
    players: tuple[int, int]
    player_list: list[str]
