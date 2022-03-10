import typing

from ..models import Cape, Skin
from .base import NameInfo

UnauthenticatedProfile = typing.NamedTuple(
    "UnauthenticatedProfile",
    [
        ("name", str),
        ("uuid", str),
        ("is_legacy", bool),
        ("is_demo", bool),
        ("names", typing.List[NameInfo]),
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
        ("names", typing.List[NameInfo]),
        ("skins", typing.List[Skin]),
        ("capes", typing.List[Cape]),
    ],
)
