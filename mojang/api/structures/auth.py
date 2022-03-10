import typing

## Security
ChallengeInfo = typing.NamedTuple(
    "ChallengeInfo",
    [("id", int), ("challenge", str)],
)
