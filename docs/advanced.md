PyMojang - Advanced Usage
===

## Full profile

To get all the available data about a user, use the function [`user`][mojang.main.user]. It will return a [`UserProfile`][mojang.profile.UserProfile] object

```python
import mojang

profile = mojang.user(username='Notch')

# OR

profile = mojang.user(uuid='069a79f444e94726a5befca90e38aaf5')
```

Once done, you have access to the following attributes:

- `uuid` **(str)** : The uuid of the profile
- `name` **(str)** : The name of the profile
- `is_legacy` **(bool)** : If the account has migrated to Mojang
- `is_demo` **(bool)** : If the account is a demo account
- `names` **(list)** : The name history of the profile
- `skins` **(list)** : The skins of the profiles
- `capes` **(list)** : The capes of the profiles


## Authenticated User

To connect with a **username** and **password**, use the function [`connect`][mojang.main.connect]. It will return a [`UserSession`][mojang.session.UserSession] object.

The [`connect`][mojang.main.connect] function also take a **client_token** parameter, but it's optional. It will be, by default, automaticly generated.

```python
session = mojang.connect('YOUR_USERNAME','YOUR_PASSWORD')
```

Once authenticated, you will have access to all the profile's attributes and also to the following new attributes:

- `name_change_allowed` **(bool)** : If the account can change name
- `created_at` **(datetime.datetime)** : the date and time at which the profile was created

You will also have access to the following methods:

- [`change_name`][mojang.session.UserSession.change_name] : Change the account username
- [`change_skin`][mojang.session.UserSession.change_skin] : Change the account skin
- [`reset_skin`][mojang.session.UserSession.reset_skin] : Reset the account skin to the default one

### Security

The first time you are going to try to connect to your account you might have some problem with certain fonctionnality, and this is because your **IP** is no verified. See [Security Question Answer Flow](https://wiki.vg/Mojang_API#Security_question-answer_flow).

Once your authenticated, you can check if your IP is secure with the [`secure`][mojang.session.UserSession.secure] attribute:  

```python
if not session.secure:
    # Do something
```

If your IP is not secure, you must complete the challenges (questions). You can get them like so:

```python
session.challenges
```

Each challenge is a tuple, the first item is the answer's id and the second one is the challenge:

```python
[
    (123, "What is your favorite pet's name?"),
    (456, "What is your favorite movie?"),
    (789, "What is your favorite author's last name?")
]
```

To verify your ip, you must send your answers, they must have the same format as the questions:

```python
answers = [
    (123, "foo"),
    (456, "bar"),
    (789, "baz")
]

session.verify(answers)
```