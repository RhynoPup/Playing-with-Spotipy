import spotipy
import os,pprint,glob,json
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import spotipy
import spotipy.util as util


token = util.prompt_for_user_token("5lCsyOWMR1u6pmGFoRgb5A","user-library-read",client_id="0c409e49863a4c99a2f772cae321b490",client_secret="a12478e603e74c0286dc0715cdcae587", redirect_uri='127.0.0.1:5000')

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('rhyno7605')
while playlists:
  for i, playlist in enumerate(playlists['items']):
    print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
# export SPOTIPY_CLIENT_ID='0c409e49863a4c99a2f772cae321b490'
# export SPOTIPY_CLIENT_SECRET='a12478e603e74c0286dc0715cdcae587'
# export SPOTIPY_REDIRECT_SECRET=''   
# token = util.prompt_for_user_token("rhyno7605")

# ryan_full_id = "5lCsyOWMR1u6pmGFoRgb5A"


# auth_id = ''
# auth_secret = 'a12478e603e74c0286dc0715cdcae587'
# ryan_UN = "rhyno7605"
# ryan = "spotify:playlist:4x8woU8j7oZYK2oEbxAwRw?si=DKOIWFssR0e7oBiD8d1-xQ"
# spotify = spotipy.Spotify()
# songs = spotify.user_playlist_tracks(ryan,"4x8woU8j7oZYK2oEbxAwRw?si=DKOIWFssR0e7oBiD8d1-xQ")
# pprint.pprint(songs)