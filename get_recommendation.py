from annoy import AnnoyIndex
import sqlite3
from get_audio_features import search_input, search_tracks, choose_right_track, get_audio_features
import ipdb
import pandas as pd
import requests
from authenticate import authenticate



def load_index(path, metric='angular'):
    index = AnnoyIndex(12, metric)
    index.load(path)
    return index

def find_neighbours(index, vector, n=10):
    rownum_list = index.get_nns_by_vector(vector, n)
    return tuple(rownum_list)

def get_recommended_tracks(rownum_list):
    data_path = 'data/spotify.sqlite'
    conn = sqlite3.connect(data_path)
    cursor = conn.cursor()
    
    query = f"""
        SELECT *
        FROM tracks_data
        WHERE rownum IN {rownum_list};
    """
    
    cursor.execute(query)
    data = cursor.fetchall()
    print(pd.DataFrame(data))
    recommended_tracks = {'title': [], 'artist': [], 'id': []}
    for track in data: 
        recommended_tracks['title'].append(track[2])
        recommended_tracks['artist'].append(track[4])
        recommended_tracks['id'].append(track[1])
    return recommended_tracks

def get_preview_cover(token, ids):
    url = f'https://api.spotify.com/v1/tracks/'
    params = {'market': 'JP', 'ids': f"{','.join(ids)}"}
    header = {'Authorization': f"Bearer {token}"}
    
    response = requests.get(
        url = url,
        params = params,
        headers = header
    ).json()
    
    previews = []
    covers = []
    for track in response['tracks']:
        previews.append(track['preview_url'])
        covers.append(track['album']['images'][0]['url'])
        
    return previews, covers

if __name__ == '__main__':
    token = authenticate()
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

        index = load_index('230331-test-4000000_tracks-100_trees-euclidean-norm.ann', 'euclidean')
        rownum_list = find_neighbours(index, audio_features)
        print(rownum_list)
        recommended_tracks = get_recommended_tracks(rownum_list)
        previews, covers = get_preview_cover(token, recommended_tracks['id'])

        for index, id in enumerate(recommended_tracks['id']):
            st.image(covers[index])
            st.markdown(f"{index + 1}. {recommended_tracks['title'][index]} - {recommended_tracks['artist'][index]}")
            st.audio(previews[index], format='audio/mp3')