import os
import json
from flask import render_template, session, redirect, url_for, current_app, request
import requests
from urllib.parse import quote
from . import main
import pprint 


#  Client Keys
CLIENT_ID = os.environ.get('SPOTIFY_APP_KEY')
CLIENT_SECRET = os.environ.get('SPOTIFY_APP_SECRET')

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://localhost"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    "show_dialog": "true",
    "client_id": CLIENT_ID
}


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/me')
def me():
  return render_template('me.html')

@main.route('/test')
def test():
  return render_template('test.html', user_id=session.get('spotify_id'), display_name=session.get('display_name'), spotify_email=session.get('spotify_email'), external_url=session.get('external_url'), link_href=session.get('link_href'), image_url=session.get('image_url'))

@main.route('/login')
def login():
  # Auth Step 1: Call spoftify authorize
  url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
  auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
  # Spotify handles Auth Step 2 and 3 through their API
  return redirect(auth_url)

@main.route('/callback/q')
def callback():
  # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)

    # Combine profile and playlist data to display
    display_arr = [profile_data] + playlist_data["items"]
    session['spotify_id'] = profile_data.get('id')
    session['display_name'] = profile_data.get('display_name')
    session['spotify_email'] = profile_data.get('email')
    #session['external_url'] = profile_data.get('exertnal_urls').get('spotify')
    session['link_href'] = profile_data.get('href')
    session['image_url'] = profile_data.get('images')[0].get('url')
    return redirect(url_for('.test'))

    # <h1>Logged in as {{display_name}}</h1>
    #         <div class="media">
    #           <div class="pull-left">
    #             <img class="media-object" width="150" src="{{images.0.url}}" />
    #           </div>
    #           <div class="media-body">
    #             <dl class="dl-horizontal">
    #               <dt>Display name</dt><dd class="clearfix">{{display_name}}</dd>
    #               <dt>Id</dt><dd>{{id}}</dd>
    #               <dt>Email</dt><dd>{{email}}</dd>
    #               <dt>Spotify URI</dt><dd><a href="{{external_urls.spotify}}">{{external_urls.spotify}}</a></dd>
    #               <dt>Link</dt><dd><a href="{{href}}">{{href}}</a></dd>
    #               <dt>Profile Image</dt><dd class="clearfix"><a href="{{images.0.url}}">{{images.0.url}}</a></dd>
    #               <dt>Country</dt><dd>{{country}}</dd>