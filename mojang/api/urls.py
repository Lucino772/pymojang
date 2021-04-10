from ..utils.web import URL

# Base urls
MOJANG_AUTHSERVER = URL('https://authserver.mojang.com')
MOJANG_API = URL('https://api.mojang.com')
MOJANG_STATUS = URL('https://status.mojang.com')
MOJANG_SESSION = URL('https://sessionserver.mojang.com')
MINECRAFT_SERVICES = URL('https://api.minecraftservices.com')
LAUNCHER_META = URL('https://launchermeta.mojang.com')
RESOURCES = URL('http://resources.download.minecraft.net')

# Game Files
MC_VERSIONS  = LAUNCHER_META.join('mc/game/version_manifest.json')
RESOURCES_DOWNLOAD = RESOURCES.join('{}/{}')

# Status check
STATUS_CHECK = MOJANG_STATUS.join('check')

# Mojang authserver
AUTHENTICATE = MOJANG_AUTHSERVER.join('authenticate')
VALIDATE = MOJANG_AUTHSERVER.join('validate')
REFRESH = MOJANG_AUTHSERVER.join('refresh')
SIGNOUT = MOJANG_AUTHSERVER.join('signout')
INVALIDATE = MOJANG_AUTHSERVER.join('invalidate')

# Security Check
SECURITY_CHECK = MOJANG_API.join('user/security/location')
SECURITY_CHALLENGES = MOJANG_API.join('user/security/challenges')

# Other
NAME_HISTORY = MOJANG_API.join('user/profiles/{uuid}/names')
GET_UUID = MOJANG_API.join('users/profiles/minecraft/{name}')
GET_UUIDS = MOJANG_API.join('profiles/minecraft')

CHECK_NAME_CHANGE = MINECRAFT_SERVICES.join('minecraft/profile/namechange')
CHANGE_NAME = MINECRAFT_SERVICES.join('minecraft/profile/name/{name}')

UPLOAD_SKIN = MINECRAFT_SERVICES.join('minecraft/profile/skins')
RESET_SKIN = MOJANG_API.join('user/profile/{uuid}/skin')

GET_PROFILE = MOJANG_SESSION.join('session/minecraft/profile/{uuid}')
GET_AUTH_PROFILE = MINECRAFT_SERVICES.join('minecraft/profile')
