from spotipy.client import *
from src.util import util
from .track_matcher import TrackMatcher
from .local_library_repository import LocalLibraryRepository
from . import nml_writer
from dotenv import load_dotenv
import os
from src.auth import auth

load_dotenv()

LOCAL_REPO_PATH = os.environ["LOCAL_REPOSITORY_PATH"]


def main():
    user = auth.get_user_1()

    print("User1 is " + user.me()["email"])
    # Prompt for continuation
    continue_input = input("Do you want to continue? (y/[N]): ")
    if continue_input.lower() != "y":
        exit()

    playlists = get_playlists(user)
    playlist_names = util.get_playlist_names(playlists)
    print("Which playlist would you like to convert?")
    for index, playlist in enumerate(playlist_names):
        print(f"{index}: {playlist}")

    playlist_index = None
    while (
        playlist_index is None
        or playlist_index < 0
        or playlist_index >= len(playlist_names)
    ):
        playlist_index = input("Select a playlist index: ")
        try:
            playlist_index = int(playlist_index)
        except ValueError:
            continue

    playlist_id = playlists[playlist_index]["id"]
    playlist = get_playlist(user, playlist_id)
    playlist_name = playlist_names[playlist_index]
    print(f"You selected {playlist_name}")

    spotify_tracks = util.playlist_to_spotify_tracks(playlist)

    local_repository = LocalLibraryRepository(LOCAL_REPO_PATH)

    track_matcher = TrackMatcher(local_repository, [], [])
    track_matcher.match(spotify_tracks)

    print(f"Found {len(track_matcher.found_tracks)} tracks")
    for found_track in track_matcher.found_tracks:
        print(
            f"Found {found_track.local_track.artist} - {found_track.local_track.title}"
        )

    print(f"Missing {len(track_matcher.pending_tracks)}")
    for pendingTrack in track_matcher.pending_tracks:
        print(
            f"missing {pendingTrack.spotify_track.artist} - {pendingTrack.spotify_track.title}"
        )
        print(f"    Possible finds:")
        for index, result in enumerate(pendingTrack.search_results):
            print(f"{index}: {result}")
        manual_track = input("Select the matching track, or enter to skip: ")
        try:
            manual_track = int(manual_track)
        except ValueError:
            continue
        if manual_track < 0 or manual_track >= len(pendingTrack.search_results):
            continue
        else:
            success = track_matcher.add_match(
                pendingTrack.index, pendingTrack.search_results[manual_track]
            )
            print(f"Added match: {success}")

    print(f"Found {len(track_matcher.found_tracks)} tracks")
    for found_track in track_matcher.found_tracks:
        print(f"Found {found_track.local_track.title}")

    ordered_tracks = local_repository.order_songs_as_filepaths(
        track_matcher.found_tracks
    )
    print(nml_writer.write_file(playlist_name, ordered_tracks))


def get_playlists(user: Spotify):
    results = user.current_user_playlists()
    playlists = results["items"]
    while results["next"]:
        results = user.next(results)
        playlists.extend(results["items"])
    return playlists


def get_playlist(user: Spotify, playlist_id):
    results = user.playlist_tracks(playlist_id)
    tracks = results["items"]
    while results["next"]:
        results = user.next(results)
        tracks.extend(results["items"])
    return tracks
