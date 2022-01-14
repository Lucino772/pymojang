**************
Authentication
**************

Mojang Authentication
---------------------

Getting a user profile is great, but you can also connect to your account and retrieve usefull information. The :py:meth:`mojang.connect` function is the easy way to doe it.

Both connect and MojangAuthenticatedUser use more low-level functions, you can view them in the following sections: Auth API, Security API and Session API.

.. code-block:: pycon

    >>> import mojang
    >>> mojang.connect('USERNAME_OR_EMAIL', 'PASSWORD')
    MojangAuthenticatedUser(
        name='PLAYER_NAME',
        uuid='PLAYER_UUID',
        is_legacy=False,
        is_demo=False,
        names=(NameInfo(name='PLAYER_NAME', changed_to_at=None),),
        skin=Skin(source='http://...', variant='classic'),
        cape=None,
        created_at=datetime.datetime(2006, 4, 29, 10, 10, 10),
        name_change_allowed=True
    )

Microsoft Authentication
------------------------

If you have a migrated account, you can't use the :py:meth:`mojang.connect` function. You will need to use the OAuth flow provided by Microsoft.

To do so you will first need to create an **Microsoft Azure App** to get your **client id** and **client secret**. Once you have those credentials, you can call the :py:meth:`mojang.microsoft_app` function with your credentials and it will create a MicrosotApp for you.

Now to authenticate a user, he will need to visit the authorization_url and grant access to your app, he will then be redirected to an url with a code parameter. The value of this parameter can the be used when calling the function authenticate that will return a MicrosoftAuthenticatedUser object.


Here is an example, you can find the `source code <https://github.com/Lucino772/pymojang/blob/1419595bcedaa1bfddf9ee6576675d3373181313/examples/microsoft_flask/app.py>`_ on github.

.. literalinclude:: ../examples/microsoft_flask/app.py
    :emphasize-lines: 11-13,16-29,36-37
