import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import os
import requests
from dotenv import load_dotenv   


load_dotenv()                  

username = "veka33"
client_secret = os.environ.get("SECRET")
client_id = os.environ.get("CLIENTID")
redirect_uri = 'http://localhost:8888/callback'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-top-read'
token = util.prompt_for_user_token(username=username, scope=scope,redirect_uri=redirect_uri,
                                   client_id=client_id,client_secret=client_secret,show_dialog=False)


if token:
    sp = spotipy.Spotify(auth=token)
    results_long = sp.current_user_top_tracks(limit=20,offset=0,time_range='long_term')
    results_medium = sp.current_user_top_tracks(limit=20,offset=0,time_range='medium_term')
    results_short = sp.current_user_top_tracks(limit=20,offset=0,time_range='short_term')

    artists_long = []
    songs_long = []
    covers_long = []

    artists_medium = []
    songs_medium = []
    covers_medium = []

    artists_short = []
    songs_short = []
    covers_short = []

    for i in results_long["items"]:

        songs_long.append(i["name"])
        artists_long.append(i["artists"][0]["name"])
        covers_long.append(i['album']['images'][0]['url'])

    for i in results_medium["items"]:

        songs_medium.append(i["name"])
        artists_medium.append(i["artists"][0]["name"])
        covers_medium.append(i['album']['images'][0]['url'])

    for i in results_short["items"]:

        songs_short.append(i["name"])
        artists_short.append(i["artists"][0]["name"])
        covers_short.append(i['album']['images'][0]['url'])


    stats_long = {"artists":artists_long,"songs":songs_long,"covers":covers_long}
    stats_medium = {"artists":artists_medium,"songs":songs_medium,"covers":covers_medium}
    stats_short = {"artists":artists_short,"songs":songs_short,"covers":covers_short}

    top_songs = {"long":stats_long,"medium":stats_medium,"short":stats_short}

    with open("./top_songs.json","w") as fp:
        json.dump(top_songs,fp)
else:
    print("Can't get token for", username)