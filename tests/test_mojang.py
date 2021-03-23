import unittest
import mojang

class TestMojangAPI(unittest.TestCase):

    def test_existent_uuid(self):
        self.assertEqual(mojang.get_uuid('Notch'), '069a79f444e94726a5befca90e38aaf5')
        self.assertEqual(mojang.get_uuid('jeb_'), '853c80ef3c3749fdaa49938b674adae6')
    
    def test_unexistent_uuid(self):
        self.assertEqual(mojang.get_uuid('UNEXISTENT_PLAYER'), None)

    def test_existent_uuids(self):
        self.assertEqual(mojang.get_uuids(['Notch','jeb_']), ['069a79f444e94726a5befca90e38aaf5','853c80ef3c3749fdaa49938b674adae6'])
        self.assertEqual(mojang.get_uuids(['jeb_','Notch']), ['853c80ef3c3749fdaa49938b674adae6','069a79f444e94726a5befca90e38aaf5'])

    def test_unexistent_uuids(self):
        self.assertEqual(mojang.get_uuids(['jeb_','UNEXISTENT_PLAYER']), ['853c80ef3c3749fdaa49938b674adae6',None])
        self.assertEqual(mojang.get_uuids(['UNEXISTENT_PLAYER1','UNEXISTENT_PLAYER2']), [None,None])

    def test_existent_name(self):
        self.assertEqual(mojang.get_username('069a79f444e94726a5befca90e38aaf5'), 'Notch')
        self.assertEqual(mojang.get_username('853c80ef3c3749fdaa49938b674adae6'), 'jeb_')

    def test_unexistent_name(self):
        self.assertEqual(mojang.get_username('069a79f444e94726a5befca90e38aaf6'), None)
    
    def test_existent_names(self):
        self.assertEqual(mojang.name_history('069a79f444e94726a5befca90e38aaf5'), [('Notch',None)])
        self.assertEqual(mojang.name_history('853c80ef3c3749fdaa49938b674adae6'), [('jeb_', None)])

    def test_unexistent_names(self):
        self.assertEqual(mojang.name_history('069a79f444e94726a5befca90e38aaf6'), [])
    