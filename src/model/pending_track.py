from src.model.local_track import LocalTrack
from src.model.spotify_track import SpotifyTrack
from typing import List
from typing import Optional


class PendingTrack:
    def __init__(
        self,
        spotify_track: SpotifyTrack,
        index: int,
        matches: Optional[List[LocalTrack]],
        search_results: List[str],
    ):
        self.spotify_track = spotify_track
        self.index = index
        self.matches = matches
        self.search_results = search_results
