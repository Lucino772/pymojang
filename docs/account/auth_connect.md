Getting a user profile is great, but you can also connect to your account and retrieve usefull information. The [`connect`][mojang.account.ext.session.connect] function is the easy way to doe it. 

Both [`connect`][mojang.account.ext.session.connect] and [`UserSession`][mojang.account.ext.session.UserSession] use more low-level functions, you can view them in the following sections: [`Auth API`](./auth_api.md), [`Security API`](./auth_security.md) and [`Session API`](./auth_session.md).


::: mojang.account.ext.session
    handler: python
    rendering:
        show_source: false
        show_root_toc_entry: false
    selection:
        members:
            - connect

::: mojang.account.ext.session
    handler: python
    rendering:
        show_source: false
        show_root_toc_entry: false
    selection:
        members:
            - UserSession
