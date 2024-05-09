import datetime as dt
import typing

from mojang.api.models import Cape, Skin


## Base
class ServiceStatus(typing.NamedTuple):
    name: str
    status: str


## Session
class NameChange(typing.NamedTuple):
    allowed: bool
    created_at: dt.datetime


## Profile
class UnauthenticatedProfile(typing.NamedTuple):
    name: str
    uuid: str
    is_legacy: bool
    is_demo: bool
    skin: Skin | None
    cape: Cape | None


class AuthenticatedUserProfile(typing.NamedTuple):
    name: str
    uuid: str
    is_legacy: bool
    is_demo: bool
    skins: list[Skin]
    capes: list[Cape]
