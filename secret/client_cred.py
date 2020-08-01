from base64 import urlsafe_b64encode
from hashlib import sha256
from random import shuffle, randint

# Spotify Client ID of Jose Cisneros, MusicStreamAid
#   email: j0zy@outlook.com
#   GitHub: github.com/jocisneros
spotify_client_id = "c011cf5f4b3447ca977164d3da00cb69"


class Credentials:
    def __init__(self, client_id: str):
        self._client_id = client_id

    def get_id(self) -> str:
        """Returns client_id of Credentials Object"""
        return self._client_id


class SpotifyCredentials(Credentials):
    def __init__(self):
        Credentials.__init__(self, spotify_client_id)
        options = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123)) + [126, 45, 46, 95]
        shuffle(options)
        self._code_verify = "".join(chr(options[randint(0, len(options) - 1)]) for _ in range(randint(43, 128)))
        self._code_challenge = urlsafe_b64encode(sha256(self._code_verify.encode()).digest()).decode()[:-1]

    def get_code_verifier(self) -> str:
        """Returns Code Verify string object, used to receive Spotify API token."""
        return self._code_verify

    def get_code_challenge(self) -> str:
        """Returns Code Challenge, used to initialize Spotify API communication."""
        return self._code_challenge
