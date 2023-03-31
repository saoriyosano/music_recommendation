import streamlit as st
from authenticate import authenticate_sl
from get_audio_features import search_tracks, choose_right_track_sl, get_audio_features
from get_recommendation import load_index, find_neighbours, get_recommended_tracks, get_preview_cover

search_button_pressed = False
go_button_pressed = False 

st.markdown('# 🎶 Borderless Music Recommendation 🌏')

title = st.text_input(
    "Title", 
    key="title",
    help=None
)

artist = st.text_input(
    "Artist", 
    key = "artist",
    help=None
)

if title or artist or (title and artist):
    token = authenticate_sl()
    track_list = search_tracks(token, title, artist, limit=50)
    if track_list == None:
        st.error("No tracks matched your search. Please try again with different key words")
    else:
        if len(track_list['track_id']) > 1:
            track_id = choose_right_track_sl(track_list)
            go_button = st.button("Go", key = "go")
        else:
            track_id = track_list['track_id']
            go_button = True
        if go_button:
            audio_features = get_audio_features(token, track_id)

            index = load_index('230331-test-4000000_tracks-100_trees-dot-norm.ann', 'dot')
            rownum_list = find_neighbours(index, audio_features)
            print(rownum_list)
            recommended_tracks = get_recommended_tracks(rownum_list)
            previews, covers = get_preview_cover(token, recommended_tracks['id'])
            for index, id in enumerate(recommended_tracks['id']):
                st.markdown(f"{index + 1}. {recommended_tracks['title'][index]} - {recommended_tracks['artist'][index]}")
                if covers[index]:
                    st.image(covers[index], width=150)
                if previews[index]:
                    st.audio(previews[index], format='audio/mp3')
