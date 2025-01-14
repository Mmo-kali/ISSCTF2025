from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import base64
import re
import os

app = Flask(__name__)

# Initialize the database
def init_db():
    db_path = os.path.join(os.getcwd(), 'ctf.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpass')")
    c.execute("INSERT INTO users (username, password) VALUES ('user', 'userpass')")
    c.execute('CREATE TABLE IF NOT EXISTS flags (id INTEGER PRIMARY KEY, flag TEXT)')
    c.execute("INSERT INTO flags (flag) VALUES ('bhbureauCTF{b@se64_3nc0d1ng_4v01ds_WAF}')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CTF Login</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background: #000;
                    color: #fff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    height: 100vh;
                    margin: 0;
                    overflow: hidden;
                }
                .container {
                    text-align: center;
                    animation: fadeIn 2s ease-in-out;
                    max-width: 800px;
                    margin: 20px;
                }
                h1 {
                    font-size: 3em;
                    margin-bottom: 20px;
                    animation: glow 1.5s infinite alternate;
                    color: #4CAF50;
                }
                p {
                    font-size: 1.2em;
                    margin-bottom: 20px;
                    animation: fadeIn 3s ease-in-out;
                }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    margin: 20px 0;
                    font-size: 1.2em;
                    color: #fff;
                    background: #4CAF50;
                    border: none;
                    border-radius: 5px;
                    text-decoration: none;
                    transition: background 0.3s ease;
                    animation: slideIn 2s ease-in-out;
                }
                .button:hover {
                    background: #388E3C;
                }
                input[type="text"], input[type="password"] {
                    padding: 10px;
                    margin: 10px 0;
                    border: none;
                    border-radius: 5px;
                    width: 80%;
                    font-size: 1em;
                }
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                @keyframes glow {
                    from { text-shadow: 0 0 10px #4CAF50, 0 0 20px #4CAF50, 0 0 30px #4CAF50, 0 0 40px #4CAF50; }
                    to { text-shadow: 0 0 20px #388E3C, 0 0 30px #388E3C, 0 0 40px #388E3C, 0 0 50px #388E3C; }
                }
                @keyframes slideIn {
                    from { transform: translateY(50px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>CTF Login</h1>
                <form method="post" action="/login">
                    <input type="text" name="username" placeholder="Username"><br>
                    <input type="password" name="password" placeholder="Password"><br>
                    <input type="submit" value="Login" class="button">
                </form>
                {% if error %}
                <p style="color: red;">{{ error }}</p>
                {% endif %}
            </div>
        </body>
        </html>
    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Check for common SQL injection patterns
    if re.search(r"('|\"|;|--|\bOR\b|\bAND\b)", username, re.IGNORECASE) or re.search(r"('|\"|;|--|\bOR\b|\bAND\b)", password, re.IGNORECASE):
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>CTF Login</title>
                <style>
                    body {
                        font-family: 'Arial', sans-serif;
                        background: #000;
                        color: #fff;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        flex-direction: column;
                        height: 100vh;
                        margin: 0;
                        overflow: hidden;
                    }
                    .container {
                        text-align: center;
                        animation: fadeIn 2s ease-in-out;
                        max-width: 800px;
                        margin: 20px;
                    }
                    h1 {
                        font-size: 3em;
                        margin-bottom: 20px;
                        animation: glow 1.5s infinite alternate;
                        color: #4CAF50;
                    }
                    p {
                        font-size: 1.2em;
                        margin-bottom: 20px;
                        animation: fadeIn 3s ease-in-out;
                    }
                    .button {
                        display: inline-block;
                        padding: 10px 20px;
                        margin: 20px 0;
                        font-size: 1.2em;
                        color: #fff;
                        background: #4CAF50;
                        border: none;
                        border-radius: 5px;
                        text-decoration: none;
                        transition: background 0.3s ease;
                        animation: slideIn 2s ease-in-out;
                    }
                    .button:hover {
                        background: #388E3C;
                    }
                    input[type="text"], input[type="password"] {
                        padding: 10px;
                        margin: 10px 0;
                        border: none;
                        border-radius: 5px;
                        width: 80%;
                        font-size: 1em;
                    }
                    @keyframes fadeIn {
                        from { opacity: 0; }
                        to { opacity: 1; }
                    }
                    @keyframes glow {
                        from { text-shadow: 0 0 10px #4CAF50, 0 0 20px #4CAF50, 0 0 30px #4CAF50, 0 0 40px #4CAF50; }
                        to { text-shadow: 0 0 20px #388E3C, 0 0 30px #388E3C, 0 0 40px #388E3C, 0 0 50px #388E3C; }
                    }
                    @keyframes slideIn {
                        from { transform: translateY(50px); opacity: 0; }
                        to { transform: translateY(0); opacity: 1; }
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>CTF Login</h1>
                    <form method="post" action="/login">
                        <input type="text" name="username" placeholder="Username"><br>
                        <input type="password" name="password" placeholder="Password"><br>
                        <input type="submit" value="Login" class="button">
                    </form>
                    <p style="color: red;">SQL injection detected. This will be reported. Please use base64 encoding for special characters.</p>
                </div>
            </body>
            </html>
        ''')
    
    # Decode base64 encoded input if necessary
    try:
        username = base64.b64decode(username).decode('utf-8')
        password = base64.b64decode(password).decode('utf-8')
    except Exception:
        pass
    
    conn = sqlite3.connect('ctf.db')
    c = conn.cursor()
    # Vulnerable to SQL injection
    c.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = c.fetchone()
    conn.close()
    
    if user:
        return redirect(url_for('welcome', username=user[1]))
    else:
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>CTF Login</title>
                <style>
                    body {
                        font-family: 'Arial', sans-serif;
                        background: #000;
                        color: #fff;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        flex-direction: column;
                        height: 100vh;
                        margin: 0;
                        overflow: hidden;
                    }
                    .container {
                        text-align: center;
                        animation: fadeIn 2s ease-in-out;
                        max-width: 800px;
                        margin: 20px;
                    }
                    h1 {
                        font-size: 3em;
                        margin-bottom: 20px;
                        animation: glow 1.5s infinite alternate;
                        color: #4CAF50;
                    }
                    p {
                        font-size: 1.2em;
                        margin-bottom: 20px;
                        animation: fadeIn 3s ease-in-out;
                    }
                    .button {
                        display: inline-block;
                        padding: 10px 20px;
                        margin: 20px 0;
                        font-size: 1.2em;
                        color: #fff;
                        background: #4CAF50;
                        border: none;
                        border-radius: 5px;
                        text-decoration: none;
                        transition: background 0.3s ease;
                        animation: slideIn 2s ease-in-out;
                    }
                    .button:hover {
                        background: #388E3C;
                    }
                    input[type="text"], input[type="password"] {
                        padding: 10px;
                        margin: 10px 0;
                        border: none;
                        border-radius: 5px;
                        width: 80%;
                        font-size: 1em;
                    }
                    @keyframes fadeIn {
                        from { opacity: 0; }
                        to { opacity: 1; }
                    }
                    @keyframes glow {
                        from { text-shadow: 0 0 10px #4CAF50, 0 0 20px #4CAF50, 0 0 30px #4CAF50, 0 0 40px #4CAF50; }
                        to { text-shadow: 0 0 20px #388E3C, 0 0 30px #388E3C, 0 0 40px #388E3C, 0 0 50px #388E3C; }
                    }
                    @keyframes slideIn {
                        from { transform: translateY(50px); opacity: 0; }
                        to { transform: translateY(0); opacity: 1; }
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>CTF Login</h1>
                    <form method="post" action="/login">
                        <input type="text" name="username" placeholder="Username"><br>
                        <input type="password" name="password" placeholder="Password"><br>
                        <input type="submit" value="Login" class="button">
                    </form>
                    <p style="color: red;">Invalid username or password.</p>
                </div>
            </body>
            </html>
        ''')

@app.route('/welcome')
def welcome():
    username = request.args.get('username')
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background: #000;
                    color: #fff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    height: 100vh;
                    margin: 0;
                    overflow: hidden;
                }
                .container {
                    text-align: center;
                    animation: fadeIn 2s ease-in-out;
                    max-width: 800px;
                    margin: 20px;
                }
                h1 {
                    font-size: 3em;
                    margin-bottom: 20px;
                    animation: glow 1.5s infinite alternate;
                    color: #4CAF50;
                }
                p {
                    font-size: 1.2em;
                    margin-bottom: 20px;
                    animation: fadeIn 3s ease-in-out;
                }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    margin: 20px 0;
                    font-size: 1.2em;
                    color: #fff;
                    background: #4CAF50;
                    border: none;
                    border-radius: 5px;
                    text-decoration: none;
                    transition: background 0.3s ease;
                    animation: slideIn 2s ease-in-out;
                }
                .button:hover {
                    background: #388E3C;
                }
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                @keyframes glow {
                    from { text-shadow: 0 0 10px #4CAF50, 0 0 20px #4CAF50, 0 0 30px #4CAF50, 0 0 40px #4CAF50; }
                    to { text-shadow: 0 0 20px #388E3C, 0 0 30px #388E3C, 0 0 40px #388E3C, 0 0 50px #388E3C; }
                }
                @keyframes slideIn {
                    from { transform: translateY(50px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome, {{ username }}!</h1>
                <p>You have successfully logged in.</p>
                <p>Flag: bhbureauCTF{b@se64_3nc0d1ng_4v01ds_WAF}</p>
            </div>
        </body>
        </html>
    ''', username=username)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))  # Default to 8000 if PORT is not set
    app.run(debug=False, host='0.0.0.0', port=port)