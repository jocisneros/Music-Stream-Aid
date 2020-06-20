from spotify_api_interpreter import SpInterpreter, api_base_url
import requests
import re

PLAYER_DATA_STATE = False


class Track:
    def __init__(self, json_data: dict):
        if json_data:
            self._title = json_data["name"]
            self._album = json_data["album"]["name"]
            self._id = json_data["id"]
            self._artists = [artist["name"] for artist in json_data["artists"]]
            self._track_len = int(json_data["duration_ms"])

            # Album Art Notes: In the returned Spotify Data exists an "images" list within the album dictionary
            # in this list includes ~3 different resolutions of the same image, I am assigning the 2nd highest
            # resolution image to be returned to be scaled down to fit whatever resolution the GUI requires.
            album_art_url = json_data["album"]["images"][1]["url"]
            self._album_art = requests.get(album_art_url).content
        else:
            self._title = "No Current Song"
            self._album = ""
            self._id = ""
            self._artists = []
            self._track_len = 0
            self._album_art = bytes()

    def get_title(self) -> str:
        return self._title

    def get_album_title(self) -> str:
        return self._album

    def get_album_art(self) -> bytes:
        return self._album_art

    def get_artists(self) -> [str]:
        return self._artists

    def track_info(self) -> str:
        global PLAYER_DATA_STATE
        return f'"{self._title}" by ' + ", ".join(self._artists) if PLAYER_DATA_STATE else self._title

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
            self._num_tracks = int(json_data["tracks"]["total"])
            self._tracks = [Track(track_data["track"]) for track_data in json_data["items"]]
        else:
            self._title = "Not Playing From Playlist"
            self._author = ""
            self._num_tracks = 0
            self._tracks = []

    def get_title(self) -> str:
        return self._title

    def get_author(self) -> str:
        return self._author

    def get_track_titles(self) -> [str]:
        return [track.get_title() for track in self._tracks]

    def get_tracks(self) -> [Track]:
        return self._tracks

    def playlist_info(self) -> str:
        return f'"{self._title}" by {self._author}'

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
        return Track(self.player_data["item"] if self.player_data else self.player_data)

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

    def get_playback_art(self) -> str:
        self.update_player_data()
        if self.player_data:
            images = self.player_data["item"]["album"]["images"]
            medium_res = images[1]["url"]
            return medium_res
        else:
            return ""

    def update_player_data(self) -> None:
        self.player_data = self.get_json_data(api_base_url + "me/player")
        global PLAYER_DATA_STATE
        PLAYER_DATA_STATE = True if self.player_data else False
