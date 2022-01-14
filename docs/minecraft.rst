Minecraft
=========

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

**Query** can be used for querying server properties. An alternative is the :ref:`minecraft:server list ping`.

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

**Server List Ping** (SLP) is an interface provided by Minecraft servers which supports querying the MOTD, player count, max players and server version via the usual port. **SLP is part of the Protocol**, so unlike :ref:`minecraft:query`, the interface is always enabled.

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
