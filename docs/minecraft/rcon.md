**RCON** allows server administrators to remotely execute Minecraft commands.

!!! Note
    **RCON** was introduced in 1.9pre4. It will not work on older servers

## Server Configuration
RCON is disabled by default, it requires the following configuration to be enabled.
```
enable-rcon=true
rcon.password=my_super_password
rcon.port=25575
broadcast-rcon-to-ops=false
```

## Code

::: mojang.minecraft.rcon
    handler: python
    rendering:
        show_source: false
        show_root_toc_entry: false
        heading_level: 3
    selection:
        members:
            - session