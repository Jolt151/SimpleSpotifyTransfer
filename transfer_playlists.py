import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy import cache_handler
import time
import util


def getPlaylists(user):
    playlists = user.current_user_playlists()
    # Very TODO
