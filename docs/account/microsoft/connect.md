If you have a migrated account, you can't use the [`connect`][mojang.account.ext.session.connect] function. You will need to use the [`OAuth flow provided by Microsoft`](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow).

To do so you will first need to create an [`Microsoft Azure App`](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app) to get your **client id** and **client secret**. Once you have those credentials, you can call the [`microsoft_app`][mojang.account.ext.microsoft.microsoft_app] function with your credentials and it will create a [`MicrosotApp`][mojang.account.ext.microsoft.MicrosoftApp] for you. 

Now to authenticate a user, he will need to visit the [`authorization_url`][mojang.account.ext.microsoft.MicrosoftApp.authorization_url] and grant access to your app, he will then be redirected to an url with a **code** parameter. The value of this parameter can the be used when calling the function [`authenticate`][mojang.account.ext.microsoft.MicrosoftApp.authenticate] that will return the same [`UserSession`][mojang.account.ext.session.UserSession] object as the [`connect`][mojang.account.ext.session.connect] function.


::: mojang.account.ext.microsoft
    handler: python
    rendering:
        show_source: false
        show_root_toc_entry: false
    selection:
        members:
            - microsoft_app

::: mojang.account.ext.microsoft
    handler: python
    rendering:
        show_source: false
        show_root_toc_entry: false
    selection:
        members:
            - MicrosoftApp
