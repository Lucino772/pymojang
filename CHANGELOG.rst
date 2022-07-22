`v1.4.0`_ (2021-12-22)
======================
Added
-----
- Add support for multiple **Skins** and **Capes** in `MojangAuthenticatedUser` and `MicrosoftAuthenticatedUser` classes

Fixed
-----
- Fix missing import `import datetime as dt` in **mojang.account.base**


`v1.3.2`_ (2021-11-13)
======================
Changed
-------
- Change the `UserSession` class into `MojangAuthenticatedUser` for **Mojang** account and `MicrosoftAuthenticatedUser` for **Microsoft** account
- Add attributes `id` and `state` to `Skin` and `Cape` classes

Fixed
-----
- Fix error in `get_user_name_change` function, `changedAt` is ignored (:issue:`2`)

Removed
-------
- Remov `AuthenticationInfo` class


`v1.3.1`_ (2021-10-20)
======================
Changed
-------
- The `status` function always returns the same response with an **unknown** status for each service.(`WEB-2303 <https://bugs.mojang.com/browse/WEB-2303>`_)


`v1.3.0`_ (2021-09-16)
======================
Added
-----
- Add `Microsoft Authentication scheme <https://wiki.vg/Microsoft_Authentication_Scheme>`_ support

Changed
-------
- The `connect` function returns a `MigratedAccount` exception when trying to connect with a migrated account (:issue:`1`)


`v1.2.1`_ (2021-06-25)
======================
Changed
-------
- The `ping` function takes a new argument `flags`
- The `get_stats` function does not take a `session_id` argument anymore
- The `ping` function returns a `SLPresponse` even when the server is not ready instead of raising an `Exception`


`v1.2.0`_ (2021-05-10)
======================
Added
-----
- Add `user` function
- Add **RCON Client** for executing command on a Minecraft Server
- Add **Query Client** for querying server properties
- Add **Server List Ping** (SLP) for querying the MOTD, player count, max players and server version via the usual port. It's an alternative to **Query**

Removed
-------
- Remove `get_username` function


`v1.1.0`_ (2021-03-24)
======================
Added
-----
- Add `api_status` function
- Add `get_username` function
- Add `get_uuid` function
- Add `get_uuids` function
- Add `name_history` function
- Add `user` function
- Add `connect` function


.. _v1.4.0: https://github.com/Lucino772/pymojang/compare/v1.3.2...v1.4.0
.. _v1.3.2: https://github.com/Lucino772/pymojang/compare/v1.3.1...v1.3.2
.. _v1.3.1: https://github.com/Lucino772/pymojang/compare/v1.3.0...v1.3.1
.. _v1.3.0: https://github.com/Lucino772/pymojang/compare/v1.2.1...v1.3.0
.. _v1.2.1: https://github.com/Lucino772/pymojang/compare/v1.2.0...v1.2.1
.. _v1.2.0: https://github.com/Lucino772/pymojang/compare/v1.1.0...v1.2.0
.. _v1.1.0: https://github.com/Lucino772/pymojang/releases/tag/v1.1.0