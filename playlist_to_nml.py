import spotipy
from spotipy.client import *
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy import cache_handler
import util
from local_song_repository import LocalSongRepository
from track_matcher import TrackMatcher
import nml_writer


def main(user: Spotify):
    playlists = getPlaylists(user)
    playlistNames = util.getPlaylistNames(playlists)
    print("Which playlist would you like to copy?")
    for index, playlist in enumerate(playlistNames):
        print(f"{index}: {playlist}")

    number = None
    while not number:
        try:
            # index = 2
            index = input("Select a playlist number:")
            number = int(index)
        except ValueError:
            print("Invalid value")
    print(f"You selected {util.getPlaylistNames(playlists)[number]}")

    playlistId = playlists[number]["id"]
    playlist = getPlaylist(user, playlistId)
    spotifyTracks = util.playlistToSpotifyTracks(playlist)

    localRepositoryPath = "/home/ubuntu/music/MusicRoot"
    localRepository = LocalSongRepository(localRepositoryPath)

    trackMatcher = TrackMatcher(localRepository, [], [])
    trackMatcher.match(spotifyTracks)

    print(f"found {len(trackMatcher.pending_tracks)} tracks")
    for foundTrack in trackMatcher.found_tracks:
        print(f"Found {foundTrack.song.title}")

    print(f"missing {len(trackMatcher.found_tracks)}")
    for pendingTrack in trackMatcher.pending_tracks:
        print(f"missing {pendingTrack.spotify_track.title}")
        print(f"    Possible finds:")
        for index, result in enumerate(pendingTrack.search_results):
            print(f"{index}: {result}")
        manualTrack = input("Select the matching track, or enter to skip:")
        try:
            manualTrack = int(manualTrack)
        except ValueError:
            continue
        if manualTrack == -1:
            continue
        else:
            success = trackMatcher.add_match(
                pendingTrack.index, pendingTrack.search_results[manualTrack]
            )
            print(f"Added match: {success}")

    print(f"found {len(trackMatcher.found_tracks)} tracks")
    for foundTrack in trackMatcher.found_tracks:
        print(f"Found {foundTrack.song.title}")

    print(nml_writer.write_file("playlist name", trackMatcher.found_tracks))


def getPlaylists(user: Spotify):
    results = user.current_user_playlists()
    playlists = results["items"]
    while results["next"]:
        results = user.next(results)
        playlists.extend(results["items"])
    return playlists


def getPlaylist(user: Spotify, id):
    results = user.playlist_tracks(id)
    tracks = results["items"]
    while results["next"]:
        results = user.next(results)
        tracks.extend(results["items"])
    return tracks
