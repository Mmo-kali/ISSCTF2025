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

        with open(r'web\webChallenge2\userFile.json', 'r') as file:
            data = json.load(file)
            for user in data['users']:
                if user['username'] == username and user['password'] == password:
                    session['logged_in'] = True
                    session['username'] = username
                    # Assign a session cookie associated with the username
                    response = redirect(url_for('account'))
                    response.set_cookie('username', username)
                    return response

        # If the loop completes without finding a match, invalid credentials
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

#try to assign session cookies to user asoon as they visit the login page so that way we can limit max number of password attempts per user is 10 




@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('create_account.html')
    
    def write_new_user(username, password):
        user = {"username": username, "password": password}
        with open(r'web\webChallenge2\userFile.json', 'r+') as file:
            data = json.load(file)
            data["users"].append(user)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

 

    def check_existing_user(username):
        with open(r'web\webChallenge2\userFile.json', 'r') as file:
            data = json.load(file)
            for user in data['users']:
                if user['username'] == username:
                    return True
        return False

    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
        
            
            print("ORIGINAL INPUT:  "+username)
            # Check if the last character of the username is a letter
            
        
            # Clean the username of null character representations
            username = re.sub(r'(\x00|\0|%00|\u0000|\x20|\+|&#0;|&#x0;|0x00|0x0000|0x00000000)', ' ', username)
            print("AFTER subbed:  "+username)
        
           
            

            # Further clean the username if needed and slice up to 16 characters
            cleaned_username = username[:15].strip()
            print("AFTER STRIPPED:  "+cleaned_username)

            if cleaned_username == 'administrator':
                response = redirect('/admin')
                response.set_cookie('shadow', 'true')
                return response

            #fix it so that it checks for the first character of the username, and that it doesnt accepts spaces at begging or anywhere else but end of user name ****
            
            if not username[-1].isalpha() or not username[0].isalpha() or username[-2] != ' ':
                return render_template('create_account.html', error='Invalid account')
        
            
        
            if check_existing_user(username):
                return render_template('create_account.html', error='User already exists')
            write_new_user(username, password)
            session['logged_in'] = True
            session['username'] = username
            response = redirect(url_for('account'))
            response.set_cookie('username', username)
            return response
        
        except Exception as e: 
            return render_template('create_account.html', error=e) # unexpected error is bad!!!





@app.route('/account') #user logged in 
def account():
    if session.get('logged_in'):
        return render_template('account.html', user=session.get('username'))
    else:
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if request.cookies.get('shadow') == 'true':
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)