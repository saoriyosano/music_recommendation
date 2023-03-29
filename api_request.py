import requests
import os
import base64
import ipdb

def authentication():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET')}

    response = requests.post(
        url = auth_url,
        data = auth_data
    ).json()
    
    return response['access_token']

def search_song_ids(token, title=None, artist=None, limit=20):
    search_url = 'https://api.spotify.com/v1/search'
    if not title or artist:
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
    track_list = {
        'track_name': [], 
        'track_id': [], 
        'artist_name': []
    }
    for i in response['tracks']['items']:
        track_list['track_name'].append(i['name'])
        track_list['track_id'].append(i['id'])
        artists = ','.join([artist['name'] for artist in i['artists']])
        track_list['artist_name'].append(artists)
    return track_list

# TODO: let user choose the correct track and get audio features of the track

if __name__ == '__main__':
    token = authentication()
    result = search_song_ids(token=token, title='Sour candy')
    print(result)