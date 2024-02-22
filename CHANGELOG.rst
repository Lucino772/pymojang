PyMojang v2.0.6 (2023-02-2024)
==============================

Misc
----

- `#80 <https://github.com/Lucino772/pymojang/issues/80>`_, `#89 <https://github.com/Lucino772/pymojang/issues/89>`_, `#94 <https://github.com/Lucino772/pymojang/issues/94>`_, `#98 <https://github.com/Lucino772/pymojang/issues/98>`_, `#110 <https://github.com/Lucino772/pymojang/issues/110>`_, `#116 <https://github.com/Lucino772/pymojang/issues/116>`_, `#120 <https://github.com/Lucino772/pymojang/issues/120>`_, `#126 <https://github.com/Lucino772/pymojang/issues/126>`_, `#134 <https://github.com/Lucino772/pymojang/issues/134>`_, `#138 <https://github.com/Lucino772/pymojang/issues/138>`_, `#150 <https://github.com/Lucino772/pymojang/issues/150>`_, `#162 <https://github.com/Lucino772/pymojang/issues/162>`_


PyMojang v2.0.5 (2023-04-04)
============================

Bugfixes
--------

- Fixed issue when passing form-data in change_user_skin (`#75 <https://github.com/Lucino772/pymojang/issues/75>`_)


PyMojang v2.0.4 (2023-03-27)
===========================

Bugfixes
--------

- Fixed issue with date format in get_user_name_change (`#72 <https://github.com/Lucino772/pymojang/issues/72>`_)


Deprecations and Removals
-------------------------

- Removed old authentication scheme: yggdrasil (`#69 <https://github.com/Lucino772/pymojang/issues/69>`_)


PyMojang v2.0.3 (2023-03-16)
============================

Bugfixes
--------

- fixing issue with NotFound errors in get_username & get_uuid (`#66 <https://github.com/Lucino772/pymojang/issues/66>`_)


PyMojang v2.0.2 (2023-02-08)
============================

Bugfixes
--------

- Fixed issue with status code returned by the APIs used in get_uuid & get_username (`#61 <https://github.com/Lucino772/pymojang/issues/61>`_)


PyMojang v2.0.1 (2023-02-04)
============================

Bugfixes
--------

- Fixed issue with return status code in get_uuid & get_username (`#59 <https://github.com/Lucino772/pymojang/issues/59>`_)


Improved Documentation
----------------------

- Configure towncrier for changelog generation (`#48 <https://github.com/Lucino772/pymojang/issues/48>`_)
- Fixed issue when getting the package's version in the docs (`#49 <https://github.com/Lucino772/pymojang/issues/49>`_)
- Added new documentation workflow & deployment on GitHub pages (`#50 <https://github.com/Lucino772/pymojang/issues/50>`_)
- Theme Customisation (`#51 <https://github.com/Lucino772/pymojang/issues/51>`_)
- Added missing documentation for *get_blocked_servers* (`#53 <https://github.com/Lucino772/pymojang/issues/53>`_)


PyMojang v2.0.0 (2022-10-27)
============================

Features
--------

- Added cape visibility toggle API (`#14 <https://github.com/Lucino772/pymojang/issues/14>`_)
- Added blocked server API (`#26 <https://github.com/Lucino772/pymojang/issues/26>`_)
- Added get_username function (`#27 <https://github.com/Lucino772/pymojang/issues/27>`_)
- Added check_product_voucher function (`#29 <https://github.com/Lucino772/pymojang/issues/29>`_)
- Added check_username function (`#30 <https://github.com/Lucino772/pymojang/issues/30>`_)
- Added redeem_product_voucher method (`#32 <https://github.com/Lucino772/pymojang/issues/32>`_)
- Added get_version & get_versions methods (`#36 <https://github.com/Lucino772/pymojang/issues/36>`_)


Bugfixes
--------

- Fixed mypy errors (`#7 <https://github.com/Lucino772/pymojang/issues/7>`_)
- Updated reset skin endpoint (`#18 <https://github.com/Lucino772/pymojang/issues/18>`_)


Improved Documentation
----------------------

- Migrate documentation from mkdocs to sphinx (`#5 <https://github.com/Lucino772/pymojang/issues/5>`_)
- Added changelog section in documentation (`#13 <https://github.com/Lucino772/pymojang/issues/13>`_)
- Updated references section in docs (`#39 <https://github.com/Lucino772/pymojang/issues/39>`_)
- Added documentation for get_version & get_versions (`#42 <https://github.com/Lucino772/pymojang/issues/42>`_)


Deprecations and Removals
-------------------------

- Removed username history API (`#46 <https://github.com/Lucino772/pymojang/issues/46>`_)


Misc
----

- `#6 <https://github.com/Lucino772/pymojang/issues/6>`_, `#8 <https://github.com/Lucino772/pymojang/issues/8>`_, `#9 <https://github.com/Lucino772/pymojang/issues/9>`_, `#10 <https://github.com/Lucino772/pymojang/issues/10>`_, `#11 <https://github.com/Lucino772/pymojang/issues/11>`_, `#12 <https://github.com/Lucino772/pymojang/issues/12>`_, `#15 <https://github.com/Lucino772/pymojang/issues/15>`_, `#20 <https://github.com/Lucino772/pymojang/issues/20>`_, `#21 <https://github.com/Lucino772/pymojang/issues/21>`_, `#22 <https://github.com/Lucino772/pymojang/issues/22>`_, `#23 <https://github.com/Lucino772/pymojang/issues/23>`_, `#24 <https://github.com/Lucino772/pymojang/issues/24>`_, `#28 <https://github.com/Lucino772/pymojang/issues/28>`_, `#33 <https://github.com/Lucino772/pymojang/issues/33>`_, `#34 <https://github.com/Lucino772/pymojang/issues/34>`_, `#35 <https://github.com/Lucino772/pymojang/issues/35>`_, `#37 <https://github.com/Lucino772/pymojang/issues/37>`_


PyMojang v1.4.0 (2021-12-22)
============================

Features
--------

- Add support for multiple Skins & Capes (`1ea73f6 <https://github.com/Lucino772/pymojang/commit/1ea73f6>`_)


Misc
----

- `326f486 <https://github.com/Lucino772/pymojang/commit/326f486>`_, `7ad3960 <https://github.com/Lucino772/pymojang/commit/7ad3960>`_, `8d2e749 <https://github.com/Lucino772/pymojang/commit/8d2e749>`_, `8f6fa73 <https://github.com/Lucino772/pymojang/commit/8f6fa73>`_, `c505de2 <https://github.com/Lucino772/pymojang/commit/c505de2>`_, `da6cd27 <https://github.com/Lucino772/pymojang/commit/da6cd27>`_, `6127716 <https://github.com/Lucino772/pymojang/commit/6127716>`_


PyMojang v1.3.2 (2021-11-13)
============================

Bugfixes
--------

- Fixed issue with keywords in mojang.account.session.get_user_name_change (`03f6ae9 <https://github.com/Lucino772/pymojang/commit/03f6ae9>`_)


Improved Documentation
----------------------

- Fixed docs due to refactoring (`9740ed7 <https://github.com/Lucino772/pymojang/commit/9740ed7>`_)


Misc
----

- `5645a93 <https://github.com/Lucino772/pymojang/commit/5645a93>`_, `969c5c4 <https://github.com/Lucino772/pymojang/commit/969c5c4>`_, `9749e10 <https://github.com/Lucino772/pymojang/commit/9749e10>`_, `cc55c99 <https://github.com/Lucino772/pymojang/commit/cc55c99>`_, `d7a482b <https://github.com/Lucino772/pymojang/commit/d7a482b>`_


PyMojang v1.3.1 (2021-10-20)
============================

Improved Documentation
----------------------

- Added Microsoft authentication example with Flask (`1419595 <https://github.com/Lucino772/pymojang/commit/1419595>`_)


Deprecations and Removals
-------------------------

- Deprecation of mojang.account.base.status method (`b8cafb1 <https://github.com/Lucino772/pymojang/commit/b8cafb1>`_)


PyMojang v1.3.0 (2021-09-16)
============================

Features
--------

- Added support for Microsoft Authentication API (`381bb4d <https://github.com/Lucino772/pymojang/commit/381bb4d>`_)
- Added microsoft_app function (`c69ef52 <https://github.com/Lucino772/pymojang/commit/c69ef52>`_)


Improved Documentation
----------------------

- Updated authentication documentation (`b909ba7 <https://github.com/Lucino772/pymojang/commit/b909ba7>`_)


Misc
----

- `23aa9f3 <https://github.com/Lucino772/pymojang/commit/23aa9f3>`_, `c8784fa <https://github.com/Lucino772/pymojang/commit/c8784fa>`_


PyMojang v1.2.1 (2021-06-25)
============================

Misc
----

- `8081cf8 <https://github.com/Lucino772/pymojang/commit/8081cf8>`_, `a2dd3f0 <https://github.com/Lucino772/pymojang/commit/a2dd3f0>`_, `c8e91b3 <https://github.com/Lucino772/pymojang/commit/c8e91b3>`_, `f978ad7 <https://github.com/Lucino772/pymojang/commit/f978ad7>`_


PyMojang v1.2.0 (2021-05-10)
============================

Features
--------

- Added Server List Ping (SLP) support (`04024b0 <https://github.com/Lucino772/pymojang/commit/04024b0>`_)
- Added API wrapper for minecraft versions (`32043a1 <https://github.com/Lucino772/pymojang/commit/32043a1>`_)
- Added SLP support for minecraft version 1.6 (`a235196 <https://github.com/Lucino772/pymojang/commit/a235196>`_)
- Added RCON & Query protocol support (`c3b5895 <https://github.com/Lucino772/pymojang/commit/c3b5895>`_)


Improved Documentation
----------------------

- Added documentation for mojang.api.base (`1e6020f <https://github.com/Lucino772/pymojang/commit/1e6020f>`_)
- Added documentation for mojang.main (`26a39bd <https://github.com/Lucino772/pymojang/commit/26a39bd>`_)
- Added documentation for mojang.api.session (`2c0a31c <https://github.com/Lucino772/pymojang/commit/2c0a31c>`_)
- Added documentation for mojang.profile.UserProfile class (`5e9c091 <https://github.com/Lucino772/pymojang/commit/5e9c091>`_)
- Added documentation for mojang.api.auth.yggdrasil (`609ce40 <https://github.com/Lucino772/pymojang/commit/609ce40>`_)
- Improved docstrings for mojang/account/* (`67579b9 <https://github.com/Lucino772/pymojang/commit/67579b9>`_)
- Added cross-ref in documentation (`a1fc805 <https://github.com/Lucino772/pymojang/commit/a1fc805>`_)
- Added documentation for mojang.session.UserSession class (`d0b590a <https://github.com/Lucino772/pymojang/commit/d0b590a>`_)
- Added documentation for mojang.api.auth.security (`f0e5116 <https://github.com/Lucino772/pymojang/commit/f0e5116>`_)
- Added documentation for mojang.error.exceptions (`6241513 <https://github.com/Lucino772/pymojang/commit/6241513>`_)


Deprecations and Removals
-------------------------

- Removed get_profile method (`74cef82 <https://github.com/Lucino772/pymojang/commit/74cef82>`_)


Misc
----

- `0d7548f <https://github.com/Lucino772/pymojang/commit/0d7548f>`_, `17f7634 <https://github.com/Lucino772/pymojang/commit/17f7634>`_, `474f807 <https://github.com/Lucino772/pymojang/commit/474f807>`_, `54ac4e3 <https://github.com/Lucino772/pymojang/commit/54ac4e3>`_, `5d618fb <https://github.com/Lucino772/pymojang/commit/5d618fb>`_, `64119c6 <https://github.com/Lucino772/pymojang/commit/64119c6>`_, `69f789f <https://github.com/Lucino772/pymojang/commit/69f789f>`_, `6e61e1c <https://github.com/Lucino772/pymojang/commit/6e61e1c>`_, `74cef82 <https://github.com/Lucino772/pymojang/commit/74cef82>`_, `7e42c31 <https://github.com/Lucino772/pymojang/commit/7e42c31>`_, `883434d <https://github.com/Lucino772/pymojang/commit/883434d>`_, `8d97049 <https://github.com/Lucino772/pymojang/commit/8d97049>`_, `a283f76 <https://github.com/Lucino772/pymojang/commit/a283f76>`_, `a32eeca <https://github.com/Lucino772/pymojang/commit/a32eeca>`_, `a66fcd6 <https://github.com/Lucino772/pymojang/commit/a66fcd6>`_, `b19bada <https://github.com/Lucino772/pymojang/commit/b19bada>`_, `be10006 <https://github.com/Lucino772/pymojang/commit/be10006>`_, `c31d13f <https://github.com/Lucino772/pymojang/commit/c31d13f>`_, `e16effb <https://github.com/Lucino772/pymojang/commit/e16effb>`_, `e27c570 <https://github.com/Lucino772/pymojang/commit/e27c570>`_, `ef937a2 <https://github.com/Lucino772/pymojang/commit/ef937a2>`_, `f501c02 <https://github.com/Lucino772/pymojang/commit/f501c02>`_, `f901059 <https://github.com/Lucino772/pymojang/commit/f901059>`_, `3528161 <https://github.com/Lucino772/pymojang/commit/3528161>`_


PyMojang v1.1.0 (2021-03-24)
============================

Features
--------

- Added disconnect_all method to UserSession class (`58a23cf <https://github.com/Lucino772/pymojang/commit/58a23cf>`_)
- Added Skin & Cape classes (`849532b <https://github.com/Lucino772/pymojang/commit/849532b>`_)
- Added change_name, upload_skin & reset_skin methods to UserSession class (`ae6a382 <https://github.com/Lucino772/pymojang/commit/ae6a382>`_)
- Added authententication with Yggdrasil (`b250ec1 <https://github.com/Lucino772/pymojang/commit/b250ec1>`_)
- Added API Wrapper with functions and classes (`d562b9a <https://github.com/Lucino772/pymojang/commit/d562b9a>`_)


Bugfixes
--------

- Fixed arguments in mojang.utils.web.filename_from_url (`62d6320 <https://github.com/Lucino772/pymojang/commit/62d6320>`_)
- Fixed issue in mojang/api/auth/security.py (`77bf08a <https://github.com/Lucino772/pymojang/commit/77bf08a>`_)


Improved Documentation
----------------------

- Improved docstrings (`22c7de4 <https://github.com/Lucino772/pymojang/commit/22c7de4>`_)
- Added docs for basic & advanced API (`733a50e <https://github.com/Lucino772/pymojang/commit/733a50e>`_)


Misc
----

- `1a6da4e <https://github.com/Lucino772/pymojang/commit/1a6da4e>`_, `1cf7b7f <https://github.com/Lucino772/pymojang/commit/1cf7b7f>`_, `4a26bda <https://github.com/Lucino772/pymojang/commit/4a26bda>`_, `55767fc <https://github.com/Lucino772/pymojang/commit/55767fc>`_, `58ba8c1 <https://github.com/Lucino772/pymojang/commit/58ba8c1>`_, `5ab5819 <https://github.com/Lucino772/pymojang/commit/5ab5819>`_, `5ad9eb1 <https://github.com/Lucino772/pymojang/commit/5ad9eb1>`_, `6a3a5b2 <https://github.com/Lucino772/pymojang/commit/6a3a5b2>`_, `960e889 <https://github.com/Lucino772/pymojang/commit/960e889>`_, `afcf300 <https://github.com/Lucino772/pymojang/commit/afcf300>`_, `cc320dc <https://github.com/Lucino772/pymojang/commit/cc320dc>`_, `e65b11a <https://github.com/Lucino772/pymojang/commit/e65b11a>`_, `f014231 <https://github.com/Lucino772/pymojang/commit/f014231>`_, `f61fe5a <https://github.com/Lucino772/pymojang/commit/f61fe5a>`_, `7702018 <https://github.com/Lucino772/pymojang/commit/7702018>`_
