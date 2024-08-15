import time
from src.util import util
from src.auth import auth


# Gets the user's liked songs
def getLikedSongs(spotifyUser):
    results = spotifyUser.current_user_saved_tracks()
    tracks = results["items"]
    while results["next"]:
        results = spotifyUser.next(results)
        tracks.extend(results["items"])
    return getSortedTracks(tracks)


def getSortedTracks(tracks):
    sortedTracks = sorted(tracks, key=lambda track: track["added_at"])
    return sortedTracks


def transferLikedSongs(user1, user2, dryRun):
    tracks = getLikedSongs(user1)

    print(f"Adding the following tracks: {util.get_track_names(tracks)}")
    # Prompt for continuation
    continue_input = input("Do you want to continue? (y/[N]): ")
    if continue_input.lower() != "y":
        exit()

    for track in tracks:
        print("adding " + track["track"]["name"])
        tracks = [track["track"]["id"]]
        print(tracks)
        if not dryRun:
            user2.current_user_saved_tracks_add(tracks)
            time.sleep(1)


def main():
    user1 = auth.get_user_1()
    user2 = auth.get_user_2()
    print("User1 (Source) is " + user1.me()["email"])
    print("User2 (Destination) is " + user2.me()["email"])

    # Prompt for continuation
    continue_input = input("Do you want to continue? (y/[N]): ")
    if continue_input.lower() != "y":
        exit()

    # Prompt for dry run
    dry_run = input("Dry run? ([Y]/n")
    dry_run = dry_run.lower() != "n"

    transferLikedSongs(user1, user2, dryRun=dry_run)
