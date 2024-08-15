import spotipy
from spotipy import cache_handler
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
scope = "user-library-read,user-library-modify,user-read-email,user-read-private"


def get_user(user_id: int):
    """
    Gets the user associated with a constant id
    :param user_id: Defined by the caller, and used to cache and maintain constant access to a single user
    :return: The spotify user
    """
    if user_id is None:
        raise Exception("userId must be a valid int")

    cache = cache_handler.CacheFileHandler(cache_path=f".spotcache{user_id}")
    auth_manager = spotipy.SpotifyOAuth(
        scope=scope,
        cache_handler=cache,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8080",
    )
    user = spotipy.Spotify(auth_manager=auth_manager)
    token = cache.get_cached_token()
    if token is None:
        url = auth_manager.get_authorize_url()
        print(f"Account {user_id}: ")
        print(url)
        response = auth_manager.get_auth_response()
        token_data = auth_manager.get_access_token(code=response)
        cache.save_token_to_cache(token_data)
        print(f"Successfully logged in user {user_id}")
        print(cache.get_cached_token())
    return user


def get_user_1():
    return get_user(1)


def get_user_2():
    return get_user(2)
