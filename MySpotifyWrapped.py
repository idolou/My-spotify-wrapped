
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import datetime
import gspread
import time

#getting the spotify API
SPOTIPY_CLIENT_ID='565c01064dff41558b4d81cfe369cfb0'
SPOTIPY_CLIENT_SECRET='3c3d619c67774eaba2ce9f9692960a83'
SPOTIPY_REDIRECT_URI='http://127.0.0.1:9090'
SCOPE="user-top-read"


spty=spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))



top_tracks_short = spty.current_user_top_tracks(limit=20, offset=0, time_range="short_term")



#get all track ids from current user yop tracks
def get_track_id(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids



track_ids = get_track_id(top_tracks_short)


#get all track geatures - album, name etc.
def get_track_features(Id):
    meta = spty.track(Id)
    #meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']
    track_info = [name, album, artist, spotify_url, album_cover]
    return track_info




get_track_features(track_ID)


# loop over all trck ids
tracks = []
for i in range(len(track_ids)):
    time.sleep(.5)
    track = get_track_features(track_ids[i])
    tracks.append(track)





#create dataset using pandas DF
data_frame = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'spotify_url', 'album_cover'])
data_frame.head(10)


#import all data to google sheets
gc = gspread.service_account(filename='C:\IDDO\projects\spotifit-341616-746d2c46b1e2.json')


sh = gc.open("My Spotify Wrapped")


worksheet = sh.worksheet("short_term")

val = worksheet.acell('B5').value



# worksheet.update([data_frame.columns.values.tolist()] + data_frame.values.tolist())


#function to insert data to sheet
def insert_to_gsheet(track_ids):
    #loop over the tracks
    tracks = []
    for i in range(len(track_ids)):
        time.sleep(.5)
        track = get_track_features(track_ids[i])
        tracks.append(track)
        #create the data frame
        data_frame = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'spotify_url', 'album_cover'])
        #insert to google sheets
        gc = gspread.service_account(filename='C:\IDDO\projects\spotifit-341616-746d2c46b1e2.json')
        sh = gc.open('My Spotify Wrapped')
        worksheet = sh.worksheet(f'{time_period}')
        worksheet.update([data_frame.columns.values.tolist()] + data_frame.values.tolist())
        print('Done')


time_ranges = ['short_term', 'medium_term', 'long_term']
for time_period in time_ranges:
    top_tracks = spty.current_user_top_tracks(limit=20, offset=0, time_range=time_period)
    track_ids = get_track_id(top_tracks)
    insert_to_gsheet(track_ids)
