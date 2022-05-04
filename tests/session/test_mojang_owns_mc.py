import unittest
from unittest import mock

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from mojang.api import session
from mojang.exceptions import Unauthorized
from tests.session.mock_server import MockSessionServer

private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=4096, backend=default_backend()
)
public_key = private_key.public_key()

private_pem = (
    private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    .decode("utf-8")
    .strip()
)

public_pem = (
    public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    .decode("utf-8")
    .strip()
)

VALID_ACCESS_TOKEN = "MY_ACCESS_TOKEN"
INVALID_ACCESS_TOKEN = "NOT_MY_ACCESS_TOKEN"

mock_server = MockSessionServer(
    VALID_ACCESS_TOKEN,
    game_private_key=private_pem,
    game_public_key=public_pem,
)


class TestMojangOwnsMinecraft(unittest.TestCase):
    @mock.patch("requests.get", side_effect=mock_server.owns_minecraft)
    def test_valid_token(self, mock_get: mock.MagicMock):
        ok = session.owns_minecraft(
            VALID_ACCESS_TOKEN, verify_sig=True, public_key=public_pem
        )
        self.assertEqual(ok, True)

    @mock.patch("requests.get", side_effect=mock_server.owns_minecraft)
    def test_invalid_token(self, mock_get: mock.MagicMock):
        self.assertRaises(
            Unauthorized, session.owns_minecraft, INVALID_ACCESS_TOKEN
        )
