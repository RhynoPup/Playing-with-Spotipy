import os
import configparser

import spotipy
import spotipy.oauth2 as oauth2

from features_extraction import get_features as features
import json,os

# config = configparser.ConfigParser()
# config.read('features_extraction/config.cfg')
# client_id = config.get('SPOTIFY', 'CLIENT_ID')
# client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
# print(client_id,client_secret)

auth = oauth2.SpotifyClientCredentials(
    client_id = os.environ.get('SPOTIFY_CLIENT_ID'),
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
)

token = auth.get_access_token()
spotify = spotipy.Spotify(auth=token)
output_folder = 'bin/data'

username=os.environ.get('SPOTIFY_TEST_USER')
if token:
    sp = spotipy.Spotify(auth=token)
    os.makedirs(output_folder,exist_ok=True)
    user_playlists_file =  os.path.join(output_folder,'playlists_'+str(username)+'.json')
    if not os.path.exists(user_playlists_file):
        with open(user_playlists_file,'w') as f:
            playlists = features.get_playlist_names(sp,username)
            f.write(json.dumps(playlists,indent=4))

    features.get_playlist_tracks(sp,username,user_playlists_file,output_folder)

    features.compile_tracks(sp,'track_repo.json',output_folder,overwrite=False)

    features.build_spreadsheet(output_folder,'track_repo.json')



else:
    print("Can't get token for", username)