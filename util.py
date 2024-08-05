from model.spotify_track import SpotifyTrack
from typing import List


def get_track_names(tracks):
    return list(map(lambda track: track["track"]["name"], tracks))


def get_playlist_names(playlists):
    return list(
        map(
            lambda playlist: f'{playlist["name"]} • {playlist["owner"]["display_name"]}',
            playlists,
        )
    )


def track_to_spotify_track(track):
    return SpotifyTrack(track["name"], trackToArtistString(track))


def playlist_to_spotify_tracks(playlist) -> List[SpotifyTrack]:
    return list(
        map(
            lambda track: SpotifyTrack(
                track["track"]["name"], trackToArtistString(track)
            ),
            playlist,
        )
    )


def trackToArtistString(track) -> str:
    artists = track["track"]["artists"]
    artistNames = list(map(lambda artist: artist["name"], artists))
    return ", ".join(artistNames)
