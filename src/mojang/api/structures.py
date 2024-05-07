import datetime as dt
import typing

from mojang.api.models import Cape, Skin

## Base
ServiceStatus = typing.NamedTuple(
    "ServiceStatus", [("name", str), ("status", str)]
)

## Session
NameChange = typing.NamedTuple(
    "NameChange", [("allowed", bool), ("created_at", dt.datetime)]
)

## Profile
UnauthenticatedProfile = typing.NamedTuple(
    "UnauthenticatedProfile",
    [
        ("name", str),
        ("uuid", str),
        ("is_legacy", bool),
        ("is_demo", bool),
        ("skin", typing.Optional[Skin]),
        ("cape", typing.Optional[Cape]),
    ],
)


AuthenticatedUserProfile = typing.NamedTuple(
    "AuthenticatedUserProfile",
    [
        ("name", str),
        ("uuid", str),
        ("is_legacy", bool),
        ("is_demo", bool),
        ("skins", typing.List[Skin]),
        ("capes", typing.List[Cape]),
    ],
)
