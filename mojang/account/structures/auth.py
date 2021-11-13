from typing import NamedTuple


## Security
class ChallengeInfo(NamedTuple):
    """
    Attributes:
        id (int): The id of the challenge
        challenge (str): The challenge to complete
    """

    id: int
    challenge: str
