import streamlit as st
from get_audio_features import authentication_sl, search_tracks, choose_right_track_sl, get_audio_features

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

if st.button("Search", key = "search"):
    token = authentication_sl()
    track_list = search_tracks(token, title, artist, limit=50)
    if track_list == None:
        st.error("No tracks matched your search. Please try again with different key words", icon = "🙉")
    else:
        if len(track_list['track_id']) > 1:
            track_id = choose_right_track_sl(track_list)
        else:
            track_id = track_list['track_id']
        audio_features = get_audio_features(token, track_id)
        st.table(audio_features)