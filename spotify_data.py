from spotify_api_interpreter import SpInterpreter, api_base_url
import re


class Track:
    def __init__(self, json_data: dict):
        self._title = json_data["name"]
        self._album = json_data["album"]["name"]
        self._id = json_data["id"]
        self._artists = [artist["name"] for artist in json_data["artists"]]
        self._track_len = int(json_data["duration_ms"])

    def get_title(self) -> str:
        return self._title

    def get_album_title(self) -> str:
        return self._album

    def get_artists(self) -> [str]:
        return self._artists

    def track_info(self) -> str:
        return f'"{self._title}" by ' + ", ".join(self._artists)

    def __len__(self):
        return self._track_len

    def __str__(self) -> str:
        return f'Track(title = "{self._title}", artists = {self._artists}, ' \
               f'album_name = "{self._album}", track_length = {self._track_len})'


class Playlist:
    def __init__(self, json_data={}):
        if json_data:
            self._title = json_data["name"]
            self._author = json_data["owner"]["display_name"]
            self._num_tracks = json_data["tracks"]["total"]
            self._tracks = [Track(track_data["track"]) for track_data in json_data["items"]]

    def get_title(self) -> str:
        return self._title

    def get_author(self) -> str:
        return self._author

    def get_track_titles(self) -> [str]:
        return [track.get_title() for track in self._tracks]

    def get_tracks(self) -> [Track]:
        return self._tracks

    def add_missing_track(self, track_data: dict) -> None:
        self._tracks.append(Track(track_data))

    def get_num_tracks(self) -> int:
        return self._num_tracks

    def __len__(self) -> int:
        return len(self._tracks)

    def __str__(self) -> str:
        return f'Playlist(title="{self._title}", playlist_author={self._author}, ' \
               f'f"num_tracks={len(self)} | DEBUG_COUNT={self._num_tracks}, "tracks={self._tracks})'


class User(SpInterpreter):
    def __init__(self, auth_code: str):
        SpInterpreter.__init__(self, auth_code)
        self.player_data = self.get_json_data(api_base_url + "me/player")

    def get_display_name(self) -> str:
        return self.get_json_data(api_base_url + "me")["display_name"]

    def get_current_track(self) -> Track:
        self.update_player_data()
        return Track(self.player_data["item"])

    def get_playlist(self) -> Playlist:
        self.update_player_data()
        data = self.player_data["context"]
        if data.get("href"):
            playlist_href = data["href"]
            json_response = self.get_json_data(playlist_href + "/tracks")
            user_playlist = Playlist(json_response)
            while len(user_playlist) < user_playlist.get_num_tracks():
                extra_tracks = self.get_json_data(playlist_href + "/tracks?offset=100")
                for track in extra_tracks["items"]:
                    user_playlist.add_missing_track(track["track"])
        else:
            user_playlist = Playlist()

        return user_playlist

    def update_player_data(self) -> None:
        self.player_data = self.get_json_data(api_base_url + "me/player")
