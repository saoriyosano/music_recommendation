import requests
import streamlit as st
import os

def authenticate():
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

def authenticate_sl():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': st.secrets['CLIENT_ID'],
        'client_secret': st.secrets['CLIENT_SECRET']
    }

    response = requests.post(
        url = auth_url,
        data = auth_data
    ).json()
    
    return response['access_token']