import unittest
import mojang


class TestMojangUser(unittest.TestCase):

    def test_existent_profile(self):
        profile = mojang.user('Notch')
        self.assertEqual(profile.name, 'Notch')
        self.assertEqual(profile.uuid, '069a79f444e94726a5befca90e38aaf5')
        self.assertEqual(profile.is_legacy, False)
        self.assertEqual(profile.is_demo, False)
        self.assertEqual(profile.names, [('Notch', None)])   

    def test_unexistent_profile(self):
        self.assertEqual(mojang.user('UNEXISTENT_PLAYER'), None)
