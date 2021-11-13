Getting a user profile is great, but you can also connect to your account and retrieve usefull information. The [`connect`][mojang.account.ext.session.connect] function is the easy way to doe it. 

Both [`connect`][mojang.account.ext.session.connect] and [`MojangAuthenticatedUser`][mojang.account.ext._profile.MojangAuthenticatedUser] use more low-level functions, you can view them in the following sections: [`Auth API`](./auth_api.md), [`Security API`](./auth_security.md) and [`Session API`](./auth_session.md).

!!! note "Microsoft Users"
    The following function works for Mojang account, for Microsoft accounts view
    [this](./microsoft/connect.md)

::: mojang.account.ext.session
    handler: python
    rendering:
        show_source: false
        show_root_toc_entry: false
    selection:
        members:
            - connect

::: mojang.account.ext._profile.MojangAuthenticatedUser
    handler: python
    rendering:
        show_source: false
        show_root_heading: true
        show_root_toc_entry: false
        show_root_full_path: false
    selection:
        inherited_members: true
        members:
            - refresh
            - close
            - change_name
            - change_skin
            - reset_skin
            - secure
            - challenges
            - verify
