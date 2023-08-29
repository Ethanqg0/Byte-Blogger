import json
import requests
from config.supabase_config import *
from flask import redirect, request

def user_signup_email(email, password, api_key):
    url = os.environ.get('SUPABASE_URL') + '/auth/v1/signup'
    headers = {
        'apikey': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'email': email,
        'password': password
    }

    response = requests.post(url, headers=headers, json=data)
    return response

#accomplished through accessing token via Supabase ROPC Grant Type
def user_login_email(email, password, api_key):
    url = os.environ.get('SUPABASE_URL') +  +'/auth/v1/token'
    headers = {
        'apikey': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'grant_type': 'password',
        'email': email,
        'password': password
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def is_a_user(username):
    usernames = supabase.table('username_mapping').select("username").execute().model_dump_json()
    usernames = json.loads(usernames)['data']
    for user in usernames:
        if user['username'] == username:
            return True
    return False