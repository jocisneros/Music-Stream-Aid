import requests
import urllib.parse
import base64
from client_cred import client_id, client_secret

base_url = 'https://accounts.spotify.com/'

redirect_uri = 'http://127.0.0.1:5000/spotify/callback'

api_base_url = 'https://api.spotify.com/v1/'

access_token_url = base_url + 'api/token'

# Scopes provide the bot to view information of the user once they have granted access and logged in.
#   playlist-read-private: used for viewing private playlists
#   user-modify-playback-state: used to skip, add to queue, and change volume of current track
#   user-read-playback-state: used to get current song played, and what device it's playing on
scopes = "playlist-read-private, user-modify-playback-state, user-read-playback-state"

client_data_encode = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()

query_parameters = urllib.parse.urlencode({
    'client_id': client_id, 'response_type': 'code',
    'redirect_uri': redirect_uri, 'scope': scopes,
    "show_dialog": "true"})

auth_url = base_url + 'authorize?' + query_parameters


class SpInterpreter:
    def __init__(self, auth_code: str):
        auth_html_data = {'grant_type': 'authorization_code',
                          'code': auth_code,
                          'redirect_uri': redirect_uri}

        self.auth_header = {'Authorization': f'Basic {client_data_encode}'}

        token_data = requests.post(access_token_url, data=auth_html_data, headers=self.auth_header).json()

        self.access_token = token_data['access_token']
        self.token_expiration = int(token_data['expires_in'])
        self.refresh_token = token_data['refresh_token']

        self.general_html_header = {'Accept': 'application/json',
                                    'Content-Type': 'application/json',
                                    'Authorization': f'{token_data["token_type"]} {self.access_token}'}

        self.auth_code = auth_code

    def update_token(self):
        refresh_body = {"grant_type": "refresh_token", "refresh_token": self.refresh_token}
        token_data = requests.post(access_token_url, data=refresh_body, headers=self.auth_header).json()
        self.access_token = token_data["access_token"]

    def get_json_data(self, url: str) -> dict:
        return requests.get(url, headers=self.general_html_header).json()
