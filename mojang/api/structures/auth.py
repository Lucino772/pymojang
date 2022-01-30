from typing import NamedTuple


## Security
class ChallengeInfo(NamedTuple):
    """
    :var int id: The id of the challenge
    :var str challenge: The challenge to complete
    """

    id: int
    challenge: str
