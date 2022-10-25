# URLs for basic api
api_check_status = "https://status.mojang.com/check"
api_get_blocked_servers = "https://sessionserver.mojang.com/blockedservers"
api_get_uuid = (
    lambda username: f"https://api.mojang.com/users/profiles/minecraft/{username}"
)
api_get_uuids = "https://api.mojang.com/profiles/minecraft"
api_get_username = lambda uuid: f"https://api.mojang.com/user/profile/{uuid}"
api_user_profile = (
    lambda uuid: f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
)

# URLs for Authenticated users
api_session_product_voucher = (
    lambda voucher: f"https://api.minecraftservices.com/productvoucher/{voucher}"
)
api_session_check_username = (
    lambda username: f"https://api.minecraftservices.com/minecraft/profile/name/{username}/available"
)
api_session_name_change = (
    "https://api.minecraftservices.com/minecraft/profile/namechange"
)
api_session_change_name = (
    lambda name: f"https://api.minecraftservices.com/minecraft/profile/name/{name}"
)
api_session_change_skin = (
    "https://api.minecraftservices.com/minecraft/profile/skins"
)
api_session_reset_skin = (
    "https://api.minecraftservices.com/minecraft/profile/skins/active"
)
api_session_ownership = (
    "https://api.minecraftservices.com/entitlements/mcstore"
)
api_session_profile = "https://api.minecraftservices.com/minecraft/profile"

api_session_cape_visibility = (
    "https://api.minecraftservices.com/minecraft/profile/capes/active"
)

# URLs for authentication with yggdrasil
api_yggdrasil_authenticate = "https://authserver.mojang.com/authenticate"
api_yggdrasil_refresh = "https://authserver.mojang.com/refresh"
api_yggdrasil_validate = "https://authserver.mojang.com/validate"
api_yggdrasil_invalidate = "https://authserver.mojang.com/invalidate"
api_yggdrasil_signout = "https://authserver.mojang.com/signout"

# URLs for security of Mojang accounts
api_security_verify_ip = "https://api.mojang.com/user/security/location"
api_security_challenges = "https://api.mojang.com/user/security/challenges"

# URLs for authentication with Microsoft
api_ms_xbl_authenticate = "https://user.auth.xboxlive.com/user/authenticate"
api_ms_xbl_authorize = "https://xsts.auth.xboxlive.com/xsts/authorize"
api_ms_xbl_login = (
    "https://api.minecraftservices.com/authentication/login_with_xbox"
)
