# PyMojang - Basic Usage

## API Status

To get the status of each Mojang services, use the function [`api_status`]()

```python
import mojang

status = mojang.api_status()
```

```json
{
    "minecraft.net": "green", 
    "session.minecraft.net": "green", 
    "account.mojang.com": "green", 
    "authserver.mojang.com": "green", 
    "sessionserver.mojang.com": "red", 
    "api.mojang.com": "green", 
    "textures.minecraft.net": "green", 
    "mojang.com": "green"
}
```

By specifying the name of a service, the function will only return the status for this service

```python
import mojang

status = mojang.api_status('minecraft.net')
```

```bash
green
```

## UUID by Username

To get the UUID of a username, use the function [`get_uuid`]()

```python
import mojang

uuid = mojang.get_uuid('Notch')
```

```bash
069a79f444e94726a5befca90e38aaf5
```


## UUIDs by Usernames

To get the UUID for multiple usernames, use the function [`get_uuids`]()

!!! note
    The Mojang API endpoint only allow 10 usernames, if more than 10 usernames are given to the function, multiple request will be made.

```python
import mojang

uuids = mojang.get_uuids(['Notch','jeb_'])
```

```bash
['069a79f444e94726a5befca90e38aaf5','853c80ef3c3749fdaa49938b674adae6']
```

## Username by UUID

To get the username for a UUID, use the function [`get_username`]()

```python
import mojang

username = mojang.get_username('069a79f444e94726a5befca90e38aaf5')
```

```bash
Notch
```

## Name History

To get the name history for a specific user, use the function [`name_history`]()

```python
import mojang

names = mojang.name_history('65a8dd127668422e99c2383a07656f7a')
```

```python
[
    ('piewdipie', None), 
    ('KOtMotros', datetime.datetime(2020, 3, 4, 18, 45, 26))
]
```