import requests

from spotify_modules.spotify_interpreter import SpInterpreter, api_base_url

PLAYER_DATA_STATE = False


class Track:
    def __init__(self, json_data={}):
        self.player_data = json_data
        if json_data:
            self._title = json_data["name"]
            self._album = json_data["album"]["name"]
            self._id = json_data["id"]
            self._artists = [artist["name"] for artist in json_data["artists"]]
            self._track_len = int(json_data["duration_ms"])

            # Album Art Notes: In the returned Spotify Data exists an "images" list within the album dictionary
            # in this list includes ~3 different resolutions of the same image, I am assigning the 2nd highest
            # resolution image to be returned to be scaled down to fit whatever resolution the GUI requires.
            self._art_url = json_data["album"]["images"][1]["url"]
        else:
            self._title = "No Current Track"
            self._album = ""
            self._id = ""
            self._artists = []
            self._track_len = 0
            self._album_art = bytes()

    def get_title(self) -> str:
        """Returns title of the track."""
        return self._title

    def get_album_title(self) -> str:
        """Returns album title of the track."""
        return self._album

    def get_album_art(self) -> bytes:
        """Returns a bytes object of the album art of the track."""
        return requests.get(self._art_url).content if self.player_data else bytes()

    def get_artists(self) -> [str]:
        """Returns a list of the artists on the track."""
        return self._artists

    def get_id(self) -> str:
        """Returns Spotify id of the track."""
        return self._id

    def get_track_info(self) -> str:
        """Returns a formatted string of the track's info in format: "Track Title" by Artists."""
        global PLAYER_DATA_STATE
        return f'"{self._title}" by ' + ", ".join(self._artists) if self.player_data else self._title

    def __bool__(self) -> bool:
        return bool(self._id)

    def __eq__(self, other) -> bool:
        if type(other) == type(self):
            return other.get_id() == self.get_id()
        else:
            raise TypeError(f"spotify_data.Track: Cannot compare Track object and {type(other)} object")

    def __len__(self) -> int:
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
        """Returns title of the playlist."""
        return self._title

    def get_author(self) -> str:
        """Returns author/creator name of the playlist."""
        return self._author

    def get_track_titles(self) -> [str]:
        """Returns list of titles of all tracks in the playlist."""
        return [track.get_title() for track in self._tracks]

    def get_tracks(self) -> [Track]:
        """Returns list of tracks in the playlist."""
        return self._tracks

    def playlist_info(self) -> str:
        """Returns a formatted string of the playlist's info in format: "Playlist Title" by Author."""
        return f'"{self._title}" by {self._author}'

    def add_missing_track(self, track_data: dict) -> None:
        """
        Adds missing tracks to playlist, intended to complete playlist
        with over 100 songs as Spotify's API only sends 100 tracks per
        request.
        """
        self._tracks.append(Track(track_data))

    def get_num_tracks(self) -> int:
        """Returns true number of tracks on the playlist."""
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
        """Returns User's display name."""
        return self.get_json_data(api_base_url + "me")["display_name"]

    def get_current_track(self) -> Track:
        """Returns track object of currently playing Spotify track."""
        self.update_player_data()
        return Track(self.player_data["item"] if self.player_data and self.player_data.get("item") else {})

    def get_playlist(self) -> Playlist:
        """Returns Playlist object for the context of the currently playing Spotify track."""
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
        """Updates data for player_data attribute"""
        self.player_data = self.get_json_data(api_base_url + "me/player")
        global PLAYER_DATA_STATE
        PLAYER_DATA_STATE = True if self.player_data else False
