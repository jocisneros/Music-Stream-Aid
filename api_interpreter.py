import requests

from logger import log_print


class WebInterpreter:
    def __init__(self, auth_code: str, auth_data: {str: str}, auth_header: {str: str}):
        self.auth_code = auth_code
        self.auth_data = auth_data
        self.auth_header = auth_header
        self.access_token = None

    def set_token(self, value) -> None:
        self.access_token = value

    def get_new_token_data(self, url: str, refresh_data=None, refresh_header=None) -> dict:
        old_token = self.access_token
        if refresh_data:
            token_data = requests.post(url, data=refresh_data, headers=self.auth_header).json()
        new_token = self.access_token
        log_print(f"TOKEN UPDATE: Tokens Different? {old_token == new_token}")

    @staticmethod
    def get_json_data(url: str, header: {str: str}) -> dict:
        user_request = requests.get(url, header=header)
        if user_request == "<Response [200]>":
            return user_request.json()
        else:
            raise RuntimeError(f"api_interpreter.WebInterpreter: Response Received = {user_request}")

# class APIInterpreter:
#     def __init__(self, auth_code: str):
#         auth_html_data = {'grant_type': 'authorization_code',
#                           'code': auth_code,
#                           'redirect_uri': redirect_uri}
#
#         self.auth_header = {'Authorization': f'Basic {client_data_encode}'}
#
#         token_data = requests.post(access_token_url, data=auth_html_data, headers=self.auth_header).json()
#         self.access_token = token_data['access_token']
#         self._token_expiration = int(token_data['expires_in'])
#         self._refresh_token = token_data['refresh_token']
#         self._toke_type = token_data["token_type"]
#
#         self.general_html_header = {'Accept': 'application/json',
#                                     'Content-Type': 'application/json',
#                                     'Authorization': f'{self._toke_type} {self.access_token}'}
#
#         self.auth_code = auth_code
#
#     def update_token(self):
#         """Refreshes access_token attribute, intended for use when access_token expires."""
#         old_token = self.access_token
#         refresh_body = {"grant_type": "refresh_token", "refresh_token": self._refresh_token}
#         token_data = requests.post(access_token_url, data=refresh_body, headers=self.auth_header).json()
#         self.access_token = token_data["access_token"]
#         new_token = self.access_token
#         log_print(f"TOKEN UPDATE: Tokens Different? {old_token == new_token}")
#
#     def get_json_data(self, url: str) -> dict:
#         """Pushes GET requests to Spotify API given a valid URL."""
#         self.update_general_header()
#         user_request = requests.get(url, headers=self.general_html_header)
#         try:
#             json_data = user_request.json()
#         except JSONDecodeError:
#             if user_request == "<Response [404]>":
#                 log_print("No Track Playing")
#             return {}
#         return json_data
#
#     def get_expiration_time(self) -> int:
#         """Returns expiration time for access_token attribute."""
#         return self._token_expiration
#
#     def update_general_header(self) -> None:
#         """Updates general_html_header attribute to reflect current _token_type and access_token attribute values"""
#         self.general_html_header = {'Accept': 'application/json',
#                                     'Content-Type': 'application/json',
#                                     'Authorization': f'{self._toke_type} {self.access_token}'}
