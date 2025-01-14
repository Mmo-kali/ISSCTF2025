from flask import Flask, request, render_template, Response, make_response, redirect, url_for, session
from flask_httpauth import HTTPTokenAuth
import base64
import os
import csv
import re
import json





app = Flask(__name__)
app.secret_key = "OrlandoMagic"

users = {
    "user1": "password1",
    "alice": "password2",
    "bob":"password3"
}

@app.route('/')
def index():
    return render_template('index.html', user='Guest')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with open(r'WEb-Challenge-Overflow\userFile.json', 'r') as file:
            data = json.load(file)
            for user in data['users']:
                if user['username'] == username and user['password'] == password:
                    session['logged_in'] = True
                    session['username'] = username
                    # Assign a session cookie associated with the username
                    response = redirect(url_for('account'))
                    response.set_cookie('username', username)
                    return response
                else: 
                    return render_template('login.html', error='Invalid credentials')
        # If the loop completes without finding a match, invalid credentials
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

#try to assign session cookies to user asoon as they visit the login page so that way we can limit max number of password attempts per user is 10 



@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('create_account.html')

    def check_existing_user(username):
        with open(r'WEb-Challenge-Overflow\userFile.json', 'r') as file:
            data = json.load(file)
            for user in data['users']:
                if user['username'] == username:
                    return True
        return False

    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            if username == 'administrator' or username == 'administrator               ':
                return render_template('create_account.html', error=f'This Username [{username}] is a Invalid account')
            
            if ' ' in username:
                return render_template('create_account.html', error='Username cannot contain spaces')
            
                        

            
            print("ORIGINAL INPUT:  " + username)
            # Clean the username of null character representations
            username = re.sub(r' ', '$', username)
            username = re.sub(r'(\x00|\0|%00|\u0000|\x20|\+|&#0;|&#x0;|0x00|0x0000|0x00000000|0x00000000)', ' ', username)
            print("AFTER subbed:" + username + ";")
        
            # Initialize the circular buffer with a size of 28
            circular_buffer = CircularBuffer(15)

            # Add each character of the username to the circular buffer
            for char in username:
                circular_buffer.add(char)

            # Get the cleaned username from the circular buffer
            cleaned_username = circular_buffer.get()
            print("AFTER STRIPPED:" + cleaned_username + ";")

            if cleaned_username == "administrator  ":
                response = redirect('/admin')
                response.set_cookie('shadow', 'Q29va2llVGVtcDAwMDM=')
                return response

            # Fix it so that it checks for the first character of the username, and that it doesn't accept spaces at the beginning or anywhere else but the end of the username
            # Need help
            # if not username[-1] == '$' or not username[0].isalpha() or username[-2] != ' ':
            #     return render_template('create_account.html', error=f'This Username [{cleaned_username}] is a Invalid account (isAlpha!)')
        
            if check_existing_user(username):
                return render_template('create_account.html', error='User already exists')
            
            else: 
                return render_template('create_account.html', error=f'This Username [{cleaned_username}] is a Invalid account')
        
        except Exception as e: 
            return render_template('create_account.html', error=e) # unexpected error is bad!!!

class CircularBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = [''] * size
        self.index = 0

    def add(self, element):
        self.buffer[self.index] = element
        self.index = (self.index + 1) % self.size

    def get(self):
        return ''.join(self.buffer)



@app.route('/account') #user logged in 
def account():
    if session.get('logged_in'):
        return render_template('account.html', user=session.get('username'))
    else:
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    
    # Set the 'shadow' cookie to 'false'
    response = make_response(redirect(url_for('login')))
    response.set_cookie('shadow', 'PrajwalChuprys4000')
    
    return response


@app.route('/admin')
def admin():
    if request.cookies.get('shadow') == 'Q29va2llVGVtcDAwMDM=':
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)