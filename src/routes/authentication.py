from config.supabase_config import * 
from src.services.authentication_services import *
from flask import Flask, current_app, request, Blueprint
from flask_cors import CORS, cross_origin

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/create_account_with_email', methods=['POST'])
@cross_origin()
def create_account():
    data = request.get_json()  # Get JSON data from the request body

    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if username and email and password:
        result = attempt_create_account(username, email, password)
        response_data = {'message': result}
        status_code = 200
    else:
        response_data = {'message': 'Missing required data'}
        status_code = 400

    # Create a JSON-formatted response using the json module
    response = auth_bp.response_class(
        response=json.dumps(response_data),
        status=status_code,
        mimetype='application/json'
    )

    return response

@auth_bp.route('/login_with_email', methods=['POST'])
@cross_origin()
def login():

    url = os.environ.get('API_URL') + '/auth/v1/token?grant_type=password'
    headers = {
    'apikey': os.environ.get('API_KEY'),
    'Content-Type': 'application/json'
    }   
    email = request.json.get('email')
    password = request.json.get('password')

    print(email)
    print(password)

    data = {
        "email": email,
        "password": password
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get('access_token')

        # Return a JSON response using the json module
        return json.dumps({'token': token}), 200, {'Content-Type': 'application/json'}
    else:
        return 'Login failed', 401

@auth_bp.route('/login_with_github', methods=['GET'])
@cross_origin()
def login_with_github():
    return route_to_github()

@auth_bp.route('/github-callback', methods=['GET'])
def github_callback():
    return route_from_github_callback()
    
@auth_bp.route('/accounts', methods=['GET'])
@cross_origin()
def accounts():
    accounts = get_all_accounts()
    return accounts