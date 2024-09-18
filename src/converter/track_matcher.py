from typing import List
from src.converter.local_library_repository import LocalLibraryRepository
from src.model.local_track import LocalTrack
from src.model.spotify_track import SpotifyTrack
from src.model.found_track import FoundTrack
from src.model.pending_track import PendingTrack


class TrackMatcher:
    def __init__(
        self,
        local_library_repository: LocalLibraryRepository,
        found_tracks: List[FoundTrack],
        pending_tracks: List[PendingTrack],
    ):
        self.local_library_repository = local_library_repository
        self.library = local_library_repository.library
        self.found_tracks = found_tracks.copy()
        self.pending_tracks = pending_tracks.copy()

    def match(self, spotify_tracks: List[SpotifyTrack]):
        for index, spotify_track in enumerate(spotify_tracks):
            matching_tracks = self.library.get(spotify_track.title)
            if (
                matching_tracks is not None
                and len(matching_tracks) == 1
                and matching_tracks[0].title == spotify_track.title
                and matching_tracks[0].artist == spotify_track.artist
            ):
                # This is an exact match based on title and artist. Add it.
                self.found_tracks.append(FoundTrack(matching_tracks[0], index))
            else:
                search_results = self.search_for_matches(spotify_track)
                self.pending_tracks.append(
                    PendingTrack(
                        spotify_track, index, matching_tracks, search_results
                    )
                )

    def add_match(self, index: int, track: LocalTrack):
        self.found_tracks.append(FoundTrack(track, index))

    def add_match(self, index: int, track_path: str) -> bool:
        song = self.local_library_repository.get_single(track_path)
        if song:
            self.found_tracks.append(FoundTrack(song, index))
            self.pending_tracks = [
                pt for pt in self.pending_tracks if pt.index != index
            ]
            return True
        else:
            return False

    def search_for_matches(self, spotify_track: SpotifyTrack) -> List[str]:
        return self.local_library_repository.search_library(
            f"{spotify_track.artist} - {spotify_track.title}", 10
        )
