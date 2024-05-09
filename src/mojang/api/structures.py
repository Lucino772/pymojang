from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import datetime as dt

    from mojang.api.models import Cape, Skin


# Base
class ServiceStatus(NamedTuple):
    name: str
    status: str


# Session
class NameChange(NamedTuple):
    allowed: bool
    created_at: dt.datetime


# Profile
class UnauthenticatedProfile(NamedTuple):
    name: str
    uuid: str
    is_legacy: bool
    is_demo: bool
    skin: Skin | None
    cape: Cape | None


class AuthenticatedUserProfile(NamedTuple):
    name: str
    uuid: str
    is_legacy: bool
    is_demo: bool
    skins: list[Skin]
    capes: list[Cape]
