**Query** can be used for querying server properties. An alternative is the [`Server List Ping`](slp.md).

!!! Note
    **Query** was introduced in 1.9pre4. It will not work on older servers

## Server Config
Query is disabled by default, it requires the following configuration to be enabled.
```
enable-query=true
query.port=25585
```

## Code
::: mojang.minecraft.query
    handler: python
    rendering:
        show_source: false
        show_root_toc_entry: false
        heading_level: 3
    selection:
        members:
            - get_stats
