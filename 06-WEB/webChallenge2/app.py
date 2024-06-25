from flask import Flask, request, render_template, Response, make_response, redirect, url_for, session
from flask_httpauth import HTTPTokenAuth
import base64
import os
import csv


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

        with open('userFile.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == password:
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
        with open('userFile.csv', 'a') as file:
            file.write('\n')  # Go down one line in the file
            writer = csv.writer(file)
            writer.writerow([username, password])

    def check_existing_user(username):
        with open('userFile.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2 and row[0] == username:
                    return True
        return False

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the last character of the username is a letter
        if not username[-1].isalpha():
            return render_template('create_account.html', error='Invalid username')

        # Slice the username up to 16 characters and remove null spaces
        username = username[:16].replace('%00', '')

        if username == 'administrator':
            response = redirect('/admin')
            response.set_cookie('shadow', 'true')
            return response
        
        if check_existing_user(username):
            return render_template('create_account.html', error='User already exists')
        write_new_user(username, password)
        session['logged_in'] = True
        session['username'] = username
        response = redirect(url_for('account'))
        response.set_cookie('username', username)
        return response
       
    
    return render_template('create_account.html')




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