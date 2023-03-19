**************
Authentication
**************

The basic method allows you to easily retrieve information about users and Mojang games, but you might want to go further by authenticating to your minecraft account. To do so you must first create a :py:class:`~mojang.api.auth.models.MojangAuthenticationApp`, this app will then allow you to authenticate to your account.

.. code-block:: pycon

    >>> import mojang
    >>> CLIENT_ID = ... # This is your Azure client id
    >>> CLIENT_SECRET = ... # This is your Azure client secret
    >>> app = mojang.app(CLIENT_ID, CLIENT_SECRET)

After creating your app you can use the :py:meth:`~mojang.api.auth.models.MojangAuthenticationApp.get_session` method, which will return a :py:class:`~~mojang.api.auth.models.MicrosoftAuthenticatedUser`.

.. code-block:: pycon

    >>> # First you must visit the url given by: `app.authorization_url`
    >>> # this will redirect you to a url with a code parameter
    >>> # you can then use this code to get a session
    >>> app.get_session('here goes the code')
    MicrosoftAuthenticatedUser(
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

Here is a full example, you can find the `source code <https://github.com/Lucino772/pymojang/blob/1419595bcedaa1bfddf9ee6576675d3373181313/examples/microsoft_flask/app.py>`_ on github.

.. literalinclude:: ../examples/microsoft_flask/app.py
    :emphasize-lines: 12-14,17-33,40,45
