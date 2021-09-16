import unittest

import mojang
from mojang.account.structures.base import NameInfoList, UserProfile, UUIDInfo, NameInfo
from mojang.account.structures.session import Cape, Skin


class TestMojangAPI(unittest.TestCase):

    def test_existent_uuid(self):
        self.assertEqual(mojang.get_uuid('Notch').uuid, '069a79f444e94726a5befca90e38aaf5')
        self.assertEqual(mojang.get_uuid('jeb_').uuid, '853c80ef3c3749fdaa49938b674adae6')
    
    def test_unexistent_uuid(self):
        self.assertEqual(mojang.get_uuid('UNEXISTENT_PLAYER'), None)

    def test_existent_uuids(self):
        self.assertEqual(mojang.get_uuids(['Notch','jeb_']), [UUIDInfo('Notch','069a79f444e94726a5befca90e38aaf5'), UUIDInfo('jeb_','853c80ef3c3749fdaa49938b674adae6')])
        self.assertEqual(mojang.get_uuids(['jeb_','Notch']), [UUIDInfo('jeb_','853c80ef3c3749fdaa49938b674adae6'), UUIDInfo('Notch','069a79f444e94726a5befca90e38aaf5')])

    def test_unexistent_uuids(self):
        self.assertEqual(mojang.get_uuids(['jeb_','UNEXISTENT_PLAYER']), [UUIDInfo('jeb_','853c80ef3c3749fdaa49938b674adae6'),None])
        self.assertEqual(mojang.get_uuids(['UNEXISTENT_PLAYER1','UNEXISTENT_PLAYER2']), [None,None])

    def test_existent_names(self):
        self.assertEqual(mojang.names('069a79f444e94726a5befca90e38aaf5'), NameInfoList([NameInfo('Notch', None)]))
        self.assertEqual(mojang.names('853c80ef3c3749fdaa49938b674adae6'), NameInfoList([NameInfo('jeb_', None)]))

    def test_unexistent_names(self):
        self.assertEqual(mojang.names('069a79f444e94726a5befca90e38aaf6'), NameInfoList([]))

    def test_existent_profile(self):
        self.assertEqual(mojang.user('069a79f444e94726a5befca90e38aaf5'), UserProfile('Notch', '069a79f444e94726a5befca90e38aaf5', False, False, NameInfoList([NameInfo('Notch', None)]), Skin('http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680', 'classic'), None))
        self.assertEqual(mojang.user('853c80ef3c3749fdaa49938b674adae6'), UserProfile('jeb_', '853c80ef3c3749fdaa49938b674adae6', False, False, NameInfoList([NameInfo('jeb_', None)]), Skin('http://textures.minecraft.net/texture/7fd9ba42a7c81eeea22f1524271ae85a8e045ce0af5a6ae16c6406ae917e68b5', 'classic'), Cape('http://textures.minecraft.net/texture/9e507afc56359978a3eb3e32367042b853cddd0995d17d0da995662913fb00f7', None)))

    def test_unexistent_profile(self):
        self.assertEqual(mojang.user('069a79f444e94726a5befca90e38aaf6'), None)
