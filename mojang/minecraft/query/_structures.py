from typing import List, NamedTuple, Tuple


class ServerStats(NamedTuple):
    motd: str
    game_type: str
    game_id: str
    version: str
    map: str
    host: Tuple[str, int]
    plugins: List[str]
    players: Tuple[int, int]
    player_list: List[str]
