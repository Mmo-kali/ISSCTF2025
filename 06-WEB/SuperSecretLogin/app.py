from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    # Add your authentication logic here
    if username == 'jcaesar' and password == 'VeryStrongPassword1@':
        return redirect(url_for('success'))
    else:
        return redirect(url_for('login'))

@app.route('/success')
def success():
    return "Welcome to BlackHat Hacker Login! bhbureauCTF{DontBookMarkThis}"

if __name__ == '__main__':
    app.run(debug=True)