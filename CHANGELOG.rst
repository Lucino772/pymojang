v1.2.1 (2021-06-25)
===================

Features
--------

- Added argument `flags` to the `ping` function


Bugfixes
--------

- The `ping` function now returns a `SLPresponse` even when the server is not ready instead of raising an `Exception`


Deprecations and Removals
-------------------------

- Removed argument `session_id` from `get_stats` function


v1.2.0 (2021-05-10)
===================

Features
--------

- Added **RCON Client** for executing command on a Minecraft Server
- Added **Query Client** for querying server properties
- Added **Server List Ping** (SLP) for querying the MOTD, player count, max players and server version via the usual port. It's an alternative to **Query**


Improved Documentation
----------------------

- The Documentation has been completely renewed


Deprecations and Removals
-------------------------

- `get_username` was removed, instead use `user` to retrieve username by UUID


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
