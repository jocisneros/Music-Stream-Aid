import requests
import urllib.parse
import base64

base_url = 'https://accounts.spotify.com/'

redirect_uri = 'http://127.0.0.1:5000/spotify/callback'

api_base_url = 'https://api.spotify.com/v1/'

access_token_url = base_url + 'api/token'

client_id = '9c7cc50bd7e949ca8bfe244b691215c3'

client_secret = '3f0943eb7f9c4c7e97737233f6e0f318'

to_encode = f'{client_id}:{client_secret}'

client_data_encode = base64.b64encode(to_encode.encode()).decode()

query_parameters = urllib.parse.urlencode({
    'client_id': client_id, 'response_type': 'code',
    'redirect_uri': redirect_uri, 'scope': 'playlist-read-private'
})

auth_url = base_url + 'authorize?' + query_parameters
