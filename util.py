from model.spotify_track import SpotifyTrack


def getTrackNames(tracks):
    return list(map(lambda track: track["track"]["name"], tracks))


def getPlaylistNames(playlists):
    return list(
        map(
            lambda playlist: (playlist["name"], playlist["owner"]["display_name"]),
            playlists,
        )
    )


def trackToSpotifyTrack(track):
    return SpotifyTrack(track["name"], track["artist"]["name"])


def playlistToSpotifyTracks(playlist):
    return list(
        map(
            lambda track: SpotifyTrack(
                track["track"]["name"], track["track"]["artists"][0]["name"]
            ),
            playlist,
        )
    )
