from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, verify_jwt_in_request
from functools import wraps
import logging
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '276c628ce33a59b398e4bc8f961874f454c57cfcc77cd0c27e4efc429095bd52945f465786371701f96ec5782d9379b287fe8aa6b5d00ce47f65f89fd12bc665'  # Change this to a secure key
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Configure JWT to read from cookies
app.config['JWT_ACCESS_COOKIE_NAME'] = 'session'  # Set the cookie name to 'session'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disable CSRF protection for simplicity

# Configure CORS to allow all origins
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Initialize JWT
jwt = JWTManager(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Serve static files from the 'public' directory
@app.route('/public/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

# Serve login.html for GET requests to the root URL
@app.route('/')
def serve_login():
    return send_from_directory('public', 'login.html')

# Endpoint to handle login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # For demonstration purposes, we're using a hardcoded username and password
    if username == 'shadowAgent' and password == 'blackhats':  # change password later.
        # Create a token
        token = create_access_token(identity=username)

        logging.info(f'User {username} logged in successfully.')

        # Create a response object
        response = make_response(jsonify(message='Login successful', redirectUrl='/hackme', token=token), 200)
        
        # Set the token as a cookie
        response.set_cookie('session', token, httponly=True)

        return response
    else:
        logging.info(f'Failed login attempt for username: {username}')
        return jsonify(message='Invalid credentials'), 401

# Custom decorator to verify JWT and check username
def jwt_required_and_check_username(username):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Verify JWT in request
                verify_jwt_in_request()
                current_user = get_jwt_identity()
                if current_user != username:
                    return jsonify(message='Unauthorized user'), 403
            except Exception as e:
                return jsonify(message=str(e)), 401
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Custom decorator to verify JWT and check if user is admin
def jwt_required_and_check_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Verify JWT in request
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            if current_user != 'StarLight':
                return jsonify(message='Unauthorized user'), 403
        except Exception as e:
            return jsonify(message=str(e)), 401
        return fn(*args, **kwargs)
    return wrapper

# Middleware to verify JWT and check username
@app.route('/hackme')
@jwt_required_and_check_username('shadowAgent')
def hackme():
    current_user = get_jwt_identity()
    logging.info(f'User {current_user} accessed /hackme')
    return '<h1>HACK ME!</h1>'

# Route to list contents of the 'public' directory
@app.route('/public', methods=['GET'])
def list_public_directory():
    try:
        files = os.listdir('flask/public')
        return jsonify(files=files)
    except Exception as e:
        return jsonify(message=str(e)), 500

# Route to access the 'flag' directory, only accessible by admin
@app.route('/flag', methods=['GET'])
@jwt_required_and_check_admin
def access_flag_directory():
    try:
        return '<h1>shadowCTF{SolvingJWTwithTOOLS_isCool2024}</h1>'
    except Exception as e:
        return jsonify(message=str(e)), 500

# Start the server
if __name__ == '__main__':
    app.run(port=3000)