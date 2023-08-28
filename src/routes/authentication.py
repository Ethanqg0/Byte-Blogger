from src.routes.init_common_route import *
from src.services.authentication_services import *

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup_email', methods=['POST'])
@cross_origin()
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    supabase_api_key = os.environ.get('SUPABASE_KEY')

    response = user_signup_email(email, password, supabase_api_key)
    
    if response.status_code == 200:
        return jsonify({'message': 'User signed up successfully!'})
    else:
        return jsonify({'message': 'User signup failed.'}), response.status_code


@auth_bp.route('/login_email', methods=['POST'])
@cross_origin()
def login():
    url = os.environ.get('SUPABASE_URL') + '/auth/v1/token?grant_type=password'
    headers = {
    'apikey': os.environ.get('SUPABASE_KEY'),
    'Content-Type': 'application/json'
    }   
    email = request.json.get('email')
    password = request.json.get('password')

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
    
@auth_bp.route('/signup_phone', methods=['POST'])
@cross_origin()
def signup_phone():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')
    supabase_api_key = os.environ.get('SUPABASE_KEY')

    response = user_signup_phone(phone, password, supabase_api_key)
    
    if response.status_code == 200:
        return jsonify({'message': 'User signed up successfully!'})
    else:
        return jsonify({'message': 'User signup failed.'}), response.status_code
    
@auth_bp.route('/login_phone', methods=['POST'])
@cross_origin()
def login_phone():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')
    supabase_api_key = os.environ.get('SUPABASE_KEY')

    response = user_phone_login(phone, password, supabase_api_key)
    
    if response.status_code == 200:
        return jsonify({'message': 'User signed up successfully!'})
    else:
        return jsonify({'message': 'User signup failed.'}), response.status_code