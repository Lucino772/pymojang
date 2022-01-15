v1.2.0 (2021-05-10)
===================

Features
--------

- Added **RCON Client** for executing command on a Minecraft Server (`#2 <https://github.com/Lucino772/pymojang/issues/2>`__)
- Added **Query Client** for querying server properties (`#3 <https://github.com/Lucino772/pymojang/issues/3>`__)
- Added **Server List Ping** (SLP) for querying the MOTD, player count, max players and server version via the usual port. It's an alternative to **Query** (`#4 <https://github.com/Lucino772/pymojang/issues/4>`__)


Improved Documentation
----------------------

- The Documentation has been completely renewed (`#5 <https://github.com/Lucino772/pymojang/issues/5>`__)


Deprecations and Removals
-------------------------

- `get_username` was removed, instead use `user` to retrieve username by UUID (`#1 <https://github.com/Lucino772/pymojang/issues/1>`__)


v1.1.0 (2021-03-24)
===================

Features
--------

- Added `api_status` function
- Added `get_username` function
- Added `get_uuid` function
- Added `get_uuids` function
- Added `name_history` function
- Added `user` function
- Added `connect` function
