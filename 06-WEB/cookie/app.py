import random
import string
from flask import Flask, request, make_response, render_template_string, render_template
import base64
import urllib.parse
import os

app = Flask(__name__)

# Admin cookie for comparison, URL encoded
admin_cookie_encoded = urllib.parse.quote(base64.b64encode(b'O:4:"User":4:{s:8:"username";s:5:"admin";s:7:"isAdmin";b:1;s:9:"loggedIn";b:1;s:5:"token";i:0;}').decode('utf-8'))

@app.route('/')
def index():
    # Generate a random letter token
    token = ''.join(random.choices(string.ascii_letters, k=10))  # Generate a 10-letter random token
    # Generate a generic agent cookie with loggedIn and token
    agent_cookie_data = f'O:4:"User":4:{{s:8:"username";s:6:"agent";s:7:"isAdmin";b:0;s:9:"loggedIn";b:1;s:5:"token";s:{len(token)}:"{token}";}}'
    agent_cookie = base64.b64encode(agent_cookie_data.encode('utf-8')).decode('utf-8')
    response = make_response("Welcome, please login. Ask the Administrator for the login page path")
    response.set_cookie("user_info", agent_cookie)
    return response





@app.route('/admin')
def admin():
    user_info_encoded = request.cookies.get('user_info', '')
    print(user_info_encoded)
    # Decode the URL-encoded cookie
    user_info = base64.b64decode(urllib.parse.unquote(user_info_encoded)).decode('utf-8')

    x_forwarded_for = request.headers.get('X-Forwarded-For', '')
    user_agent = request.headers.get('User-Agent', '')

    # Re-encode the user_info for comparison
    user_info_encoded_for_comparison = urllib.parse.quote(base64.b64encode(user_info.encode('utf-8')).decode('utf-8'))

    # Check if the cookie matches the admin cookie
    if user_info_encoded_for_comparison == admin_cookie_encoded:
        # Check for local IP address
        if x_forwarded_for == "127.1":
            # Check for specific user agent
            if user_agent == "shadowAgent":
                return "<h1>Flag: bhbureauCTF{w3b--i$--fun}</h1>"
            else:
                return "Access Denied: Incorrect User-Agent."
        elif x_forwarded_for in ["localhost", "127.0.0.1"]:
            return "Access Denied: WAF Blocking."
        else:
            return "Access Denied: Invalid *LOCAL* IP."
    else:
        return "Access Denied: Invalid credentials."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))  # Default to 8000 if PORT is not set
    app.run(debug=False, host='0.0.0.0', port=port)