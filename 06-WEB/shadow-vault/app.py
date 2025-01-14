from flask import Flask, request, render_template, Response, make_response, redirect, url_for, session
from flask_httpauth import HTTPTokenAuth
import base64
import os
from urllib.parse import urlparse



app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "c2hhZG93TWFuOnBhc3N3b3Jk":"shadowMan",
    "Ym9iOmJvYg==": "bob",
    "This-is-not-The-SOulition": "reset"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]
    else:
        return False

def generate_token(username, password):
            credentials = f"{username}:{password}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            return encoded_credentials


@app.route('/')
def index():
    if 'auth' in request.cookies and request.cookies['auth'] == 'c2hhZG93TWFuOnBhc3N3b3Jk':
        return render_template('index2.html', user=tokens[request.cookies['auth']])
    
    elif 'auth' in request.cookies and request.cookies['auth'] == 'This-is-not-The-SOulition': # incase they brute force 
        return render_template('index2.html', user=tokens[request.cookies['auth']])

    elif 'auth' in request.cookies and request.cookies['auth'] == '':
        return render_template('index.html', user='Guest')
    
    else:
        return render_template('index.html', user='Guest')
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
    
        #  you can generate a token using a library like JWT
        token = generate_token(username, password)
        
        if verify_token(token) != False:
            response = make_response(redirect(url_for('two_factor_auth')))
            response.set_cookie('auth', 'bnVsbDpudWxs', httponly=True)
            return response
        else: 
             return Response('Could not verify your login!', 400, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        
    
    else:
        return '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
            font-family: Arial, sans-serif;
            margin: 0;
        }
        .login-container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        h1 {
            margin-bottom: 1rem;
            color: #333;
        }
        p {
            margin-bottom: 2rem;
            color: #666;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 0.5rem;
            margin-bottom: 1rem;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        input[type="submit"] {
            width: 100%;
            padding: 0.5rem;
            background: #ff9a9e;
            border: none;
            border-radius: 5px;
            color: white;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        input[type="submit"]:hover {
            background: #fad0c4;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>Login</h1>
        <p>Please log in to access the Crypt Wallet.</p>
        <form method="post">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <input type="submit" value="Login">
        </form>
    </div>
</body>
</html>
        '''


@app.route('/2fa', methods=['GET', 'POST'])
def two_factor_auth():
    if request.method == 'POST':
        def generate_2fa_code(secret_key):
            # Add your code here to generate the 2FA code
            # Replace this with your actual 2FA code generation logic
            return "2fa"  # Example code, replace with your actual implementation
        
        def verify_2fa_code(code):
            # Add your code here to verify the 2FA code
            secret_key = 'secret-key'  # Replace with your actual secret key
            expected_code = generate_2fa_code(secret_key)  # Replace with your actual 2FA code generation logic
            if code == expected_code:
                return True
            else:
                return False
            return True  # Replace this with your actual verification logic


        code = request.form['code']
        if verify_2fa_code(code):
                response = make_response(redirect(url_for('index')))
                response.set_cookie('auth', 'This-is-not-The-SOulition')
                response.set_cookie('user', 'reset')
                return response
        else:
            return Response('Invalid 2FA code!', 400, {'WWW-Authenticate': 'Basic realm="2FA code required!"'})
    else:
        referrer = request.referrer
        if referrer:
            referrer_path = urlparse(referrer).path
            if referrer_path in ['/2fa', '/login', '/login?']:
                return '''
                <form method="post">
                    2FA Code: <input type="text" name="code"><br>
                    <input type="submit" value="Submit">
                </form>
                '''
        else: 
           
            return Response('Invalid Referrer!', 400, {'WWW-Authenticate': 'Basic realm="2FA code required!"'})

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index'))) 
    response.set_cookie('auth', ' ', expires=0, path='/', domain='localhost')
    return response


@app.route('/crypt-wallet')

def crypt_wallet():
    if 'auth' in request.cookies and request.cookies['auth'] == 'c2hhZG93TWFuOnBhc3N3b3Jk':
       return '''<h1> Here's your flag: bhbureauCTF{'y0u_4r3_4_r34l_h4ck3r'} </h1>'''
    else: 
        return Response('You are not authorized to view this page! (Try reseting/changing your cookie)', 404, {'WWW-Authenticate': 'Basic realm="Login required!"'})
   

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))  # Default to 8000 if PORT is not set
    app.run(debug=False, host='0.0.0.0', port=port)