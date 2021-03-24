Mojang Authentication with Yggdrasil
===

::: mojang.api.auth.yggdrasil
    handler: python
    selection:
      members:
        - authenticate_user
        - refresh_token
        - validate_token
        - signout_user
        - invalidate_token
    rendering:
      show_root_heading: true
      show_source: true