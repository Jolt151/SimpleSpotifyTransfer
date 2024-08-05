from model.spotify_track import SpotifyTrack
from typing import List


def getTrackNames(tracks):
    return list(map(lambda track: track["track"]["name"], tracks))


def getPlaylistNames(playlists):
    return list(
        map(
            lambda playlist: f'{playlist["name"]} • {playlist["owner"]["display_name"]}',
            playlists,
        )
    )


def trackToSpotifyTrack(track):
    return SpotifyTrack(track["name"], trackToArtistString(track))


def playlistToSpotifyTracks(playlist) -> List[SpotifyTrack]:
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
