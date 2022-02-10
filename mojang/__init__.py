"""
Pymojang module
---------------

Pymojang is a full wrapper around the [Mojang API](https://wiki.vg/Mojang_API)
and [Mojang Authentication API](https://wiki.vg/Authentication)

Checkout the [`documentation`](https://pymojang.readthedocs.io/en/latest/)
"""
from . import _version
from .api import (
    connect,
    get_blocked_servers,
    get_names,
    get_profile,
    get_sales,
    get_status,
    get_username,
    get_uuid,
    get_uuids,
    microsoft_app,
)

__version__ = _version.get_versions()["version"]
