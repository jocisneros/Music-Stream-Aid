import urllib.parse
from json.decoder import JSONDecodeError

import requests

from logger import log_print
from secret.client_cred import SpotifyCredentials

base_url = 'https://accounts.spotify.com/'

redirect_uri = 'http://127.0.0.1:5000/spotify/callback'

api_base_url = 'https://api.spotify.com/v1/'

access_token_url = base_url + 'api/token'

spotify_cred = SpotifyCredentials()

# Scopes provide the bot to view information of the user once they have granted access and logged in.
#   playlist-read-private: used for viewing private playlists
#   user-modify-playback-state: used to skip, add to queue, and change volume of current track
#   user-read-playback-state: used to get current song played, and what device it's playing on
scopes = "playlist-read-private, user-modify-playback-state, user-read-playback-state"

query_parameters = urllib.parse.urlencode({
    'client_id': spotify_cred.get_id(), 'response_type': 'code',
    'redirect_uri': redirect_uri, 'scope': scopes,
    'code_challenge_method': "S256",
    'code_challenge': spotify_cred.get_code_challenge()
})

auth_url = base_url + 'authorize?' + query_parameters


class SpInterpreter:
    def __init__(self, auth_code: str):
        self.auth_code = auth_code
        auth_html_data = {"client_id": spotify_cred.get_id(),
                          'grant_type': 'authorization_code',
                          'code': auth_code,
                          'redirect_uri': redirect_uri,
                          "code_verifier": spotify_cred.get_code_verifier()}

        token_data = requests.post(access_token_url, data=auth_html_data).json()

        self.access_token = token_data['access_token']
        self._token_expiration = int(token_data['expires_in'])
        self._refresh_token = token_data['refresh_token']
        self._token_type = token_data["token_type"]

        self.general_html_header = {'Accept': 'application/json',
                                    'Content-Type': 'application/json',
                                    'Authorization': f'{self._token_type} {self.access_token}'}

    def update_token(self):
        """Refreshes access_token attribute, intended for use when access_token expires."""
        old_token = self.access_token
        refresh_body = {"grant_type": "refresh_token", "refresh_token": self._refresh_token,
                        "client_id": spotify_cred.get_id()}
        token_data = requests.post(access_token_url, data=refresh_body).json()
        self.access_token = token_data["access_token"]
        new_token = self.access_token
        log_print(f"TOKEN UPDATE: Tokens Different? {old_token == new_token}")

    def get_json_data(self, url: str) -> dict:
        """Pushes GET requests to Spotify API given a valid URL."""
        self.update_general_header()
        user_request = requests.get(url, headers=self.general_html_header)
        try:
            json_data = user_request.json()
        except JSONDecodeError:
            if user_request == "<Response [404]>":
                log_print("No Track Playing")
            return {}
        return json_data

    def get_expiration_time(self) -> int:
        """Returns expiration time for access_token attribute."""
        return self._token_expiration

    def update_general_header(self) -> None:
        """Updates general_html_header attribute to reflect current _token_type and access_token attribute values"""
        self.general_html_header = {'Accept': 'application/json',
                                    'Content-Type': 'application/json',
                                    'Authorization': f'{self._token_type} {self.access_token}'}
