import typing
import datetime as dt


ServiceStatus = typing.NamedTuple(
    "ServiceStatus", [("name", str), ("status", str)]
)

NameInfo = typing.NamedTuple(
    "NameInfo",
    [("name", str), ("changed_to_at", typing.Optional[dt.datetime])],
)
