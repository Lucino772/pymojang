v1.4.0 (2021-12-22)
===================

Features
--------

- Added support for multiple **Skins** and **Capes** in `MojangAuthenticatedUser` and `MicrosoftAuthenticatedUser` classes


Bugfixes
--------

- Added missing import `import datetime as dt` in **mojang.account.base**


v1.3.2 (2021-11-13)
===================

Features
--------

- Separated `UserSession` class into 2 classes: `MojangAuthenticatedUser` for **Mojang** account and `MicrosoftAuthenticatedUser` for **Microsoft** account
- Added attributes `id` and `state` to `Skin` and `Cape` classes


Bugfixes
--------

- Fixed error in `get_user_name_change` function, `changedAt` is ignored (`#2 <https://github.com/Lucino772/pymojang/issues/2>`__)


Deprecations and Removals
-------------------------

- Removed `AuthenticationInfo` class


v1.3.1 (2021-10-20)
===================

Bugfixes
--------

- The `status` function always returns the same response with an **unknown** status for each service.(`WEB-2303 <https://bugs.mojang.com/browse/WEB-2303?focusedCommentId=1086543&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-1086543>`_)


v1.3.0 (2021-09-16)
===================

Features
--------

- Added `Microsoft Authentication scheme <https://wiki.vg/Microsoft_Authentication_Scheme>`_ support


Bugfixes
--------

- The `connect` function returns a `MigratedAccount` exception when trying to connect with a migrated account (`#1 <https://github.com/Lucino772/pymojang/issues/1>`__)


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
