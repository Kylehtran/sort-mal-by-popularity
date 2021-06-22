import json
import requests
import secrets
import pathlib
import datetime
import os.path, time


CLIENT_ID = '7374f25516574c506768e71a9bb4503f'
CLIENT_SECRET = 'e646965485bafdbf1a638905697b8902970c061eb4c7c06a6fb99cdfeb5cd099'


def load_access_token():

    f = open('token.json')
    data = json.load(f)
    
    fname = pathlib.Path('token.json')
    creation_time = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
    expiration_time = creation_time + datetime.timedelta(seconds =  data["expires_in"])
    
    if expiration_time >= datetime.datetime.now():
        refresh_token()
        f = open('token.json')
        data = json.load(f)
    return data


def refresh_token():
    
    j = open('token.json')
    data = json.load(j)


    refresh_token = data['refresh_token']
    token = generate_new_token(refresh_token)
    j.close()

    



def generate_new_token(refresh_token: str) -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token', #change to refresh_token for refresh (was authorization token before)
        'refresh_token': refresh_token

    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the requests contains errors

    token = response.json()
    response.close()

    with open('token.json', 'w') as file:
        json.dump(token, file, indent = 4)

    return token



