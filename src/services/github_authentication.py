from supabase import redirect
from flask import request
import requests
import json
import random
import string
from config.supabase_config import *

def route_to_github():
    github_auth_url = f'https://github.com/login/oauth/authorize?client_id=207218418f7984fd3f39&redirect_uri=http://127.0.0.1:5000/github-callback'
    return redirect(github_auth_url)

def route_from_github_callback():
    code = request.args.get('code')

    response = requests.post('https://github.com/login/oauth/access_token', {
        'client_id': '207218418f7984fd3f39',
        'client_secret': 'fc821e712613f139e4363ef37cf7fb6c348230e6',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:5000/github-callback'
    }, headers={'Accept': 'application/json'})

    if response.status_code != 200:
        return "Error obtaining access token from GitHub"

    access_token = response.json().get('access_token')

    user_response = requests.get('https://api.github.com/user', headers={'Authorization': f'Bearer {access_token}'})

    if user_response.status_code != 200:
        return "Error fetching GitHub user information"

    github_user_info = user_response.json()
    github_user_id = github_user_info.get('id')

    # Check if the GitHub user ID already exists in the database
    existing_entry = supabase.table('username_mapping').select("*").eq('third_party_uuid', github_user_id).execute().model_dump_json()
    is_existing = len(json.loads(existing_entry)['data']) > 0

    if not is_existing:
        username = generate_username()
        new_mapping = {
            "username": username,
            "third_party_uuid": github_user_id,
            "third_party_provider": "Github"
        }
        supabase.table('username_mapping').insert(new_mapping).execute()

    return f"GitHub callback completed successfully, {access_token}"

def generate_username():
    def generate_word(length=4):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    word1 = generate_word()
    word2 = generate_word()
    random_numbers = f'{random.randint(10, 99):02}'

    username = f"{word1}-{word2}-{random_numbers}"
    return username