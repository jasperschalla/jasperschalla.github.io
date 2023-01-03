import webbrowser
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import os
from git import Repo
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('/home/pi/Documents/python/jasperschalla.github.io/.env')

PATH_OF_GIT_REPO = '/home/pi/Documents/python/jasperschalla.github.io/.git'  
COMMIT_MESSAGE = 'Update Spotify data'

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

    results_artist_long = sp.current_user_top_artists(limit=20,offset=0,time_range='long_term')
    results_artist_medium = sp.current_user_top_artists(limit=20,offset=0,time_range='medium_term')
    results_artist_short = sp.current_user_top_artists(limit=20,offset=0,time_range='short_term')

    artist_artists_long = []
    artist_covers_long = []
    artist_id_long = []

    artist_artists_medium = []
    artist_covers_medium = []
    artist_id_medium = []

    artist_artists_short = []
    artist_covers_short = []
    artist_id_short = []

    for i in results_artist_long["items"]:

        artist_artists_long.append(i["name"])
        artist_covers_long.append(i["images"][0]["url"])
        artist_id_long.append(i["id"])

    for i in results_artist_medium["items"]:

        artist_artists_medium.append(i["name"])
        artist_covers_medium.append(i["images"][0]["url"])
        artist_id_medium.append(i["id"])

    for i in results_artist_short["items"]:

        artist_artists_short.append(i["name"])
        artist_covers_short.append(i["images"][0]["url"])
        artist_id_short.append(i["id"])

    results_song_long = sp.current_user_top_tracks(limit=20,offset=0,time_range='long_term')
    results_song_medium = sp.current_user_top_tracks(limit=20,offset=0,time_range='medium_term')
    results_song_short = sp.current_user_top_tracks(limit=20,offset=0,time_range='short_term')

    song_artists_long = []
    song_songs_long = []
    song_covers_long = []

    song_artists_medium = []
    song_songs_medium = []
    song_covers_medium = []

    song_artists_short = []
    song_songs_short = []
    song_covers_short = []

    for i in results_song_long["items"]:

        song_songs_long.append(i["name"])
        song_artists_long.append(i["artists"][0]["name"])
        song_covers_long.append(i['album']['images'][0]['url'])

    for i in results_song_medium["items"]:

        song_songs_medium.append(i["name"])
        song_artists_medium.append(i["artists"][0]["name"])
        song_covers_medium.append(i['album']['images'][0]['url'])

    for i in results_song_short["items"]:

        song_songs_short.append(i["name"])
        song_artists_short.append(i["artists"][0]["name"])
        song_covers_short.append(i['album']['images'][0]['url'])


    song_stats_long = {"artists":song_artists_long,"songs":song_songs_long,"covers":song_covers_long}
    song_stats_medium = {"artists":song_artists_medium,"songs":song_songs_medium,"covers":song_covers_medium}
    song_stats_short = {"artists":song_artists_short,"songs":song_songs_short,"covers":song_covers_short}

    artist_stats_long = {"artists":artist_artists_long,"covers":artist_covers_long,"ids":artist_id_long}
    artist_stats_medium = {"artists":artist_artists_medium,"covers":artist_covers_medium,"ids":artist_id_medium}
    artist_stats_short = {"artists":artist_artists_short,"covers":artist_covers_short,"ids":artist_id_short}

    top_stats = {"songs":{"long":song_stats_long,"medium":song_stats_medium,"short":song_stats_short},
                 "artists":{"long":artist_stats_long,"medium":artist_stats_medium,"short":artist_stats_short},
                 "updated":datetime.today().strftime('%Y-%m-%d %H:%M:%S')}

    with open("/home/pi//Documents/python/jasperschalla.github.io/spotify_stats.json","w") as fp:
        json.dump(top_stats,fp)

    repo = Repo(PATH_OF_GIT_REPO)
    repo.git.add(update=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()

else:
    print("Can't get token for", username)
