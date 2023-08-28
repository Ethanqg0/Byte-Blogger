import json
import requests
from config.supabase_config import *
from flask import redirect, request

def attempt_create_account(username, email, password):
    try:
        uuid = user_signup_with_email(email, password)
        if uuid is None:
            return 'Account creation failed'
        else:
            supabase.table('username_mapping').insert( {"username": username, "email": email, "uuid": uuid} ).execute()
            return 'Account created'
    except:
        return 'Account creation failed'
    
def attempt_login(email, password):
    url = os.environ.get('API_URL') + '/auth/v1/token?grant_type=password'
    headers = {
    'apikey': os.environ.get('API_KEY'),
    'Content-Type': 'application/json'
    }   

    data = {
        "email": email,
        "password": password
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return f'Login successful\nEmail: {email}\nPassword: {password}'
    else:
        return 'Login failed, yikers'


#-- Account Functions
def user_signup_with_email(email, password):
    api_url = os.environ.get('API_URL') + '/auth/v1/signup'
    supabase_key = os.environ.get('API_KEY')

    data = {
        "email": email,
        "password": password
    }

    headers = {
        "apikey": supabase_key,
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data.get('user', {}).get('id')  # Extract the user's unique ID
        return user_id  # Return the user's unique ID
    else:
        return None
    
def is_a_user(username):
    usernames = supabase.table('username_mapping').select("username").execute().model_dump_json()
    usernames = json.loads(usernames)['data']
    for user in usernames:
        if user['username'] == username:
            return True
    return False

def access_username_mapping_database():
    usernames = supabase.table('username_mapping').select("username").execute().model_dump_json()
    emails = supabase.table('username_mapping').select("email").execute().model_dump_json()
    uuid = supabase.table('username_mapping').select("uuid").execute().model_dump_json()
    created_at = supabase.table('username_mapping').select("created_at").execute().model_dump_json()
    third_party_uuid = supabase.table('username_mapping').select("third_party_uuid").execute().model_dump_json()
    third_party_provider = supabase.table('username_mapping').select("third_party_provider").execute().model_dump_json()

    username = json.loads(usernames)['data']
    emails = json.loads(emails)['data']
    uuid = json.loads(uuid)['data']
    created_at = json.loads(created_at)['data']
    third_party_uuid = json.loads(third_party_uuid)['data']
    third_party_provider = json.loads(third_party_provider)['data']

    return username, emails, uuid, created_at, third_party_uuid, third_party_provider

def organize_into_accounts():
    usernames, emails, uuid, created_at, third_party_uuid, third_party_provider = access_username_mapping_database()

    accounts = []

    for i in range(len(usernames)):
        item = {
            'username': usernames[i]['username'],
            'email': emails[i]['email'],
            'uuid': uuid[i]['uuid'],
            'created_at': created_at[i]['created_at'],
            'third_party_uuid': third_party_uuid[i]['third_party_uuid'],
            'third_party_provider': third_party_provider[i]['third_party_provider']
        }

        accounts.append(item)

    return accounts

def get_all_accounts():
    accounts = organize_into_accounts()
    return accounts

def find_username_by_email(email):
    accounts = organize_into_accounts()
    for account in accounts:
        if account['email'] == email:
            username = account['username']
        return username
    return None

def find_uuid_by_email(email):
    accounts = organize_into_accounts()
    for account in accounts:
        if account['email'] == email:
            uuid = account['uuid']
        return uuid
    return None

def route_to_github():
    github_auth_url = f'https://github.com/login/oauth/authorize?client_id=207218418f7984fd3f39&redirect_uri=http://127.0.0.1:5000/github-callback'
    return redirect(github_auth_url)

def route_from_github_callback():
    code = request.args.get('code')