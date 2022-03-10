import datetime as dt
import typing

NameChange = typing.NamedTuple(
    "NameChange", [("allowed", bool), ("created_at", dt.datetime)]
)
