import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy import cache_handler
import time
import transfer_liked_songs
import util
from dotenv import load_dotenv

load_dotenv()
import os

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

scope = "user-library-read,user-library-modify,user-read-email,user-read-private"
cache = cache_handler.CacheFileHandler(cache_path=".spotcache")
cacheUser2 = cache_handler.CacheFileHandler(cache_path=".spotcache2")
auth_manager = spotipy.SpotifyOAuth(
    scope=scope,
    cache_handler=cache,
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://localhost:8080",
)
auth_manager2 = spotipy.SpotifyOAuth(
    scope=scope,
    cache_handler=cacheUser2,
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://localhost:8080",
)
spotifyUser1 = spotipy.Spotify(auth_manager=auth_manager)
spotifyUser2 = spotipy.Spotify(auth_manager=auth_manager2)
token = cache.get_cached_token()
if token is None:
    url = auth_manager.get_authorize_url()
    print("Account 1: ")
    print(url)
    response = auth_manager.get_auth_response()
    token_data = auth_manager.get_access_token(code=response)
    cache.save_token_to_cache(token_data)
    print(cache.get_cached_token())

tokenUser2 = cacheUser2.get_cached_token()
if tokenUser2 is None:
    url = auth_manager2.get_authorize_url()
    print("Account 2: ")
    print(url)
    response = auth_manager2.get_auth_response()
    token_data = auth_manager2.get_access_token(code=response)
    cacheUser2.save_token_to_cache(token_data)
    print(cacheUser2.get_cached_token())

print("User1 (Source) is " + spotifyUser1.me()["email"])
print("User2 (Destination) is " + spotifyUser2.me()["email"])

# Prompt for continuation
continue_input = input("Do you want to continue? (y/[N]): ")
if continue_input.lower() != "y":
    exit()

transfer_liked_songs.transferLikedSongs(spotifyUser1, spotifyUser2, dryRun=False)
