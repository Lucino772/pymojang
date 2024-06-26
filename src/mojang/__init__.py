"""
Pymojang module
---------------

Pymojang is a full wrapper around the [Mojang API](https://wiki.vg/Mojang_API)
and [Mojang Authentication API](https://wiki.vg/Authentication)

Checkout the [`documentation`](https://pymojang.readthedocs.io/en/latest/)
"""

from mojang.api import (
    app,
    get_blocked_servers,
    get_profile,
    get_status,
    get_username,
    get_uuid,
    get_uuids,
)

try:
    from mojang._version import __version__
except ImportError:
    __version__ = None

__all__ = [
    "__version__",
    "app",
    "get_blocked_servers",
    "get_profile",
    "get_status",
    "get_username",
    "get_uuid",
    "get_uuids",
]
