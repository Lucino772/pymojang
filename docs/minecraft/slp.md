**Server List Ping** (SLP) is an interface provided by Minecraft servers which supports querying the MOTD, player count, max players and server version via the usual port. SLP is part of the **Protocol**, so unlike [`Query`](query.md), the interface is always enabled


## Code
::: mojang.minecraft.slp
    handler: python
    rendering:
        show_source: false
        show_root_toc_entry: false
        heading_level: 3
    selection:
        members:
            - ping
