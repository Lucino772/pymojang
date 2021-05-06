from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass(frozen=True)
class ServerStats:
    motd: str = field()
    game_type: str = field()
    game_id: str = field()
    version: str = field()
    map: str = field()
    host: Tuple[str, int] = field()
    plugins: List[str] = field(repr=False)
    players: Tuple[int, int] = field()
    player_list: List[str] = field()
