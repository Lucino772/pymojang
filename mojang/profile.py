import datetime as dt

class UserProfile:

    def __init__(self, name: str, uuid: str, legacy: bool, demo: bool, names: list, created_at: dt.datetime, name_change_allowed: bool, skins: list, capes: list):
        self.name = name
        self.uuid = uuid
        self.is_legacy = legacy
        self.is_demo = demo

        self.names = names

        self.created_at = created_at
        self.name_change_allowed = name_change_allowed

        self.skins = skins
        self.capes = capes

    def update(self, **kwargs):
        self.__dict__.update(kwargs)
