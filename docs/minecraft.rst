Minecraft
=========

Versions
--------

List versions (:py:meth:`~mojang.minecraft.launchermeta.get_versions`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> from mojang import minecraft
    >>> minecraft.get_versions()
    (['22w18a', '22w17a', '22w16b', ..., 'rd-20090515', 'rd-132328', 'rd-132211'], '1.18.2', '22w18a')

Get a specific version (:py:meth:`~mojang.minecraft.launchermeta.get_version`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: pycon

    >>> from mojang import minecraft
    >>> minecraft.get_version("1.18.1")
    VersionMeta(
        id='1.18.2',
        type='release',
        url='https://launchermeta.mojang.com/v1/packages/86f9645f8398ec902cd17769058851e6fead68cf/1.18.2.json',
        time=datetime.datetime(2022, 2, 28, 10, 48, 16, tzinfo=datetime.timezone.utc),
        release_time=datetime.datetime(2022, 2, 28, 10, 42, 45, tzinfo=datetime.timezone.utc)
    )


RCON
----

**RCON** allows server administrators to remotely execute minecraft commands.

.. note::

    RCON was introduced in 1.9pre4. It will not work on older servers

Server Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block::

    enable-rcon=true
    rcon.password=my_super_password
    rcon.port=25575
    broadcast-rcon-to-ops=false


Example
~~~~~~~

.. code-block:: pycon

    >>> from mojang.minecraft import rcon
    >>> with rcon.session(('localhost', 25575), 'my_super_password') as send:
    ...     send('help') # This execute the /help command

Query
-----

**Query** can be used for querying server properties. An alternative is the `Server List Ping`_.

Server Config
~~~~~~~~~~~~~

Query is disabled by default, it requires the following configuration to be enabled.

.. code-block::

    enable-query=true
    query.port=25585

Example
~~~~~~~

.. code-block:: pycon

    >>> from mojang.minecraft import query
    >>> query.get_stats(('localhost', 25585))
    ServerStats(
        motd='A Minecraft Server',
        game_type='SMP',
        game_id='MINECRAFT',
        version='1.16.5',
        map='world',
        host=('localhost', 25585),
        players=(0, 20),
        player_list=[]
    )

Server List Ping
----------------

**Server List Ping** (SLP) is an interface provided by Minecraft servers which supports querying the MOTD, player count, max players and server version via the usual port. **SLP is part of the Protocol**, so unlike `Query`_, the interface is always enabled.

Example
~~~~~~~

.. code-block:: pycon

    >>> from mojang.minecraft import slp
    >>> slp.ping(('localhost', 25565))
    SLPResponse(
        protocol_version=754,
        version='1.16.5',
        motd='A Minecraft Server',
        players=Players(count=(0, 20), list=[]),
        ping=1
    )
