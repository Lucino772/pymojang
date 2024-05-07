"""
Pymojang module
---------------

Pymojang is a full wrapper around the [Mojang API](https://wiki.vg/Mojang_API)
and [Mojang Authentication API](https://wiki.vg/Authentication)

Checkout the [`documentation`](https://pymojang.readthedocs.io/en/latest/)
"""

from .api import (
    app,
    get_blocked_servers,
    get_profile,
    get_status,
    get_username,
    get_uuid,
    get_uuids,
)

from .__about__ import __version__