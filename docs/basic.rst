User Guide
==========

.. currentmodule:: mojang

Install
-------

.. code-block:: bash

    $ pip install pymojang


Status
------

Mojang have multiple APIs, you can check their status by calling the method :py:func:`~mojang.api.base.get_status`.

.. caution::

    Since the begin of October 2021, Mojang closed down the status page (Issue `WEB-2303 <https://bugs.mojang.com/browse/WEB-2303?focusedCommentId=1086543&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-1086543>`_). The :py:func:`~mojang.api.base.get_status` function now always returns the same response with an *unknown* status for each service.

.. code-block:: pycon

    >>> import mojang
    >>> mojang.get_status()
    (
        ServiceStatus(name='minecraft.net', status='green'),
        ServiceStatus(name='session.minecraft.net', status='green'),
        ServiceStatus(name='account.mojang.com', status='green'),
        ServiceStatus(name='authserver.mojang.com', status='green'),
        ServiceStatus(name='sessionserver.mojang.com', status='red'),
        ServiceStatus(name='api.mojang.com', status='green'),
        ServiceStatus(name='textures.minecraft.net', status='green'),
        ServiceStatus(name='mojang.com', status='green')
    )


Blocked Servers
---------------

You can fetch a list of all the blocked servers by calling the method :py:meth:`~mojang.api.base.get_blocked_servers`.
For more details checkout `wiki.vg <https://wiki.vg/Mojang_API#Blocked_Servers>`_.

.. code-block:: pycon

    >>> import mojang
    >>> mojang.get_blocked_servers()
    [
        'dc2c735b3e6aba51ece294d7de21b947379aac4d',
        'dc2c735b3e6aba51ece294d7de21b947379aac4d',
        '780874bcade721dfccdf2ccd51cec3eb3a35c958',
        'efed28c35a3bf3433c582397f238f824bf4494b3',
        'ac7e715494da3b381bd37e87419c44e7d506f01b',
        'e41ddcf7d4b37611b676701060eae90fa65f11d1',
        'ab8724e0fac2ec56bda2f774dc5464bf0520da27',
        'c8f090859ea7c0afdab8b22a842532b979235951',
        ...
    ]


User Information
----------------

UUID (:py:meth:`~mojang.api.base.get_uuid`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> import mojang
    >>> mojang.get_uuid('Notch')
    '069a79f444e94726a5befca90e38aaf5'

UUIDs (:py:meth:`~mojang.api.base.get_uuids`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: **Limited Endpoint**
    :class: note

    The Mojang API only allow 10 usernames maximum, if more than 10 usernames are given to the function, multiple request will be made.

.. code-block:: pycon

    >>> import mojang
    >>> mojang.get_uuids(['Notch', '_jeb'])
    {
        'notch': '069a79f444e94726a5befca90e38aaf5',
        '_jeb': '45f50155c09f4fdcb5cee30af2ebd1f0'
    }

Username (:py:meth:`~mojang.api.base.get_username`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> import mojang
    >>> mojang.get_username('069a79f444e94726a5befca90e38aaf5')
    'Notch'

User Profile (:py:meth:`~mojang.api.base.get_profile`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> import mojang
    >>> mojang.get_profile('069a79f444e94726a5befca90e38aaf5')
    UnauthenticatedProfile(
        name='Notch',
        uuid='069a79f444e94726a5befca90e38aaf5',
        is_legacy=False,
        is_demo=False,
        skin=Skin(source='...', variant='classic'),
        cape=None
    )
