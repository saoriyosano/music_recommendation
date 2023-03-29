import requests
import os
import base64
import pandas as pd
import ipdb

def authentication():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET')
    }

    response = requests.post(
        url = auth_url,
        data = auth_data
    ).json()
    
    return response['access_token']

def search_input():
    title = input("Title of the track: ")
    artist = input("Artist: ")
    return title, artist

def search_tracks(token, title=None, artist=None, limit=20):
    search_url = 'https://api.spotify.com/v1/search'
    if not (title or artist):
        print('Error: please specify title or artist of the track')
    
    search_header = {'Authorization': f"Bearer {token}"}
    
    if title and artist:
        q = f'track:"{title}" artist:"{artist}"'
    elif title:
        q = f'track:"{title}"'
    else:
        q = f'artist:"{artist}"'
    search_params = {'q': q, 'limit': limit, 'type': 'track'}
    
    response = requests.get(
        url = search_url,
        params = search_params,
        headers = search_header
    ).json()
    
    if len(response['tracks']['items']) == 0:
        return None
    
    track_list = {
        'track_name': [], 
        'track_id': [], 
        'artist_name': []
    }    
    for i in response['tracks']['items']:
        track_list['track_name'].append(i['name'])
        track_list['track_id'].append(i['id'])
        artists = ', '.join([artist['name'] for artist in i['artists']])
        track_list['artist_name'].append(artists)
    return track_list

def choose_right_track(track_list):
    df = pd.DataFrame(
        track_list, 
        columns=['track_name', 'artist_name'],
        index=list(range(1, len(track_list['track_id'])+1))
        ).rename(
            columns={'track_name': 'Track name', 'artist_name': 'Artist name(s)'}
        )
    print(df)
    correct_num = int(input(
            "\nThe tracks above matched your search; please type the number of the track you'd like to use: "
        ))-1
    return track_list['track_id'][correct_num]    

def get_audio_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    get_af_header = {'Authorization': f"Bearer {token}"}
    response = requests.get(
        url = url,
        headers = get_af_header
    ).json()
    features = [
        'acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 
        'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence'
    ]
    af_vector = [response[feature] for feature in features]
    return af_vector
    
if __name__ == '__main__':
    token = authentication()
    title, artist = search_input()
    track_list = search_tracks(token=token, title=title, artist=artist)
    if track_list == None:
        print("No track matched your search. Please try again")
    else:
        if len(track_list['track_id']) > 1:
            track_id = choose_right_track(track_list)
        else:
            track_id = track_list['track_id']
        audio_features = get_audio_features(token, track_id)
        print(audio_features)