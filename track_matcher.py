from typing import List, Dict, Optional
import local_song_repository
from local_song_repository import LocalSongRepository
from model.song import Song
from model.spotify_track import SpotifyTrack
from model.found_track import FoundTrack
from model.pending_track import PendingTrack


class TrackMatcher:
    def __init__(
        self,
        localSongRepository: LocalSongRepository,
        found_tracks: List[FoundTrack],
        pending_tracks: List[PendingTrack],
    ):
        self.localSongRepository = localSongRepository
        self.library = localSongRepository.library
        self.found_tracks = found_tracks.copy()
        self.pending_tracks = pending_tracks.copy()

    def match(self, spotify_tracks: List[SpotifyTrack]):
        for index, spotify_track in enumerate(spotify_tracks):
            matching_tracks = self.library.get(spotify_track.title)
            if matching_tracks:
                if len(matching_tracks) == 1:
                    self.found_tracks.append(FoundTrack(matching_tracks[0], index))
                else:
                    search_results = self.search_for_matches(spotify_track)
                    self.pending_tracks.append(
                        PendingTrack(
                            spotify_track, index, matching_tracks, search_results
                        )
                    )
            else:
                search_results = self.search_for_matches(spotify_track)
                self.pending_tracks.append(
                    PendingTrack(spotify_track, index, None, search_results)
                )

    def add_match(self, index: int, track: Song):
        self.found_tracks.append(FoundTrack(track, index))

    def add_match(self, index: int, track_path: str) -> bool:
        song = self.localSongRepository.get_single(track_path)
        if song:
            self.found_tracks.append(FoundTrack(song, index))
            self.pending_tracks = [
                pt for pt in self.pending_tracks if pt.index != index
            ]
            return True
        else:
            return False

    def search_for_matches(self, spotify_track: SpotifyTrack) -> List[str]:
        return self.localSongRepository.search_library(spotify_track.title, 10)
