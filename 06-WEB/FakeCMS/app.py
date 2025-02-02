from flask import Flask, request, render_template_string, redirect, url_for, make_response, jsonify
import random

app = Flask(__name__)

# Flag for the CTF challenge
FLAG = "bhbureauCTF{C00K13_M4N1PUL4T10N_1S_FUN}"

# HTML Templates as strings
HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>FakeCMS - WordPress Site</title>
    <style>
        body { 
            font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif;
            margin: 0;
            background: #f0f0f1;
            line-height: 1.6;
        }
        header {
            background: #23282d;
            padding: 1rem;
            color: white;
        }
        .site-title {
            margin: 0;
            font-size: 1.8rem;
        }
        nav {
            background: #32373c;
            padding: 0.5rem;
        }
        nav a {
            color: #eee;
            text-decoration: none;
            margin-right: 1rem;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            display: grid;
            grid-template-columns: 7fr 3fr;
            gap: 2rem;
        }
        .main-content {
            background: white;
            padding: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .sidebar {
            background: white;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .post {
            margin-bottom: 2rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid #eee;
        }
        .post-title {
            color: #23282d;
            margin: 0 0 1rem 0;
        }
        .post-meta {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        .admin-button { 
            background-color: #0073aa; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 3px; 
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 1rem 0;
        }
        .widget {
            margin-bottom: 2rem;
        }
        .widget-title {
            color: #23282d;
            border-bottom: 2px solid #eee;
            padding-bottom: 0.5rem;
        }
        footer {
            background: #23282d;
            color: #eee;
            padding: 2rem;
            text-align: center;
            margin-top: 2rem;
        }
    </style>
</head>
<body>
    <header>
        <h1 class="site-title">FakeCMS</h1>
    </header>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/blog">Blog</a>
        <a href="/contact">Contact</a>
        <a href="/login" style="float:right">Login</a>
    </nav>
    <div class="container">
        <main class="main-content">
            {% if show_admin_button %}
            <form action="/admin" method="GET">
                <button class="admin-button">Admin Panel</button>
            </form>
            {% endif %}
            <article class="post">
                <h2 class="post-title">Welcome to Our WordPress Site</h2>
                <div class="post-meta">Posted by John Doe | January 1, 2024</div>
                <p>Welcome to FakeCMS, a modern content management system. This is your first post. Edit or delete it, then start writing!</p>
            </article>
            <article class="post">
                <h2 class="post-title">Getting Started with FakeCMS</h2>
                <div class="post-meta">Posted by Jane Smith | January 2, 2024</div>
                <p>Learn how to customize your site, add new posts, and manage your content effectively with our comprehensive guide.</p>
            </article>
        </main>
        <aside class="sidebar">
            <div class="widget">
                <h3 class="widget-title">Recent Posts</h3>
                <ul>
                    <li><a href="#">Welcome to Our WordPress Site</a></li>
                    <li><a href="#">Getting Started with FakeCMS</a></li>
                    <li><a href="#">Customizing Your Theme</a></li>
                </ul>
            </div>
            <div class="widget">
                <h3 class="widget-title">Categories</h3>
                <ul>
                    <li><a href="#">News</a></li>
                    <li><a href="#">Updates</a></li>
                    <li><a href="#">Tutorials</a></li>
                </ul>
            </div>
        </aside>
    </div>
    <footer>
        <p>Powered by FakeCMS | Theme: Twenty Twenty-Four</p>
    </footer>
</body>
</html>
"""

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Log In - FakeCMS</title>
    <style>
        body { background: #f1f1f1; font-family: Arial, sans-serif; }
        .login-form {
            background: white;
            width: 320px;
            margin: 100px auto;
            padding: 26px 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,.13);
        }
        .login-form h1 {
            margin: 0 0 24px 0;
            font-size: 20px;
            text-align: center;
        }
        .input-field {
            margin: 8px 0;
            width: 100%;
            padding: 3px;
            border: 1px solid #ddd;
        }
        .submit-button {
            background: #0073aa;
            border: none;
            color: white;
            padding: 10px;
            width: 100%;
            margin-top: 20px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <!-- Default user listing.. ?  -->
    <div class="login-form">
        <h1>FakeCMS</h1>
        {% if error %}
        <p style="color: red;">{{ error }}</p>
        {% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="Username" class="input-field">
            <input type="password" name="password" placeholder="Password" class="input-field">
            <button type="submit" class="submit-button">Log In</button>
        </form>
    </div>
</body>
</html>
"""

ADMIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel - FakeCMS</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
    </style>
</head>
<body>
    <h1>Admin Panel</h1>
    <p>Congratulations! Here's your flag: {{ flag }}</p>
    <p><a href="/logout">Logout</a></p>
</body>
</html>
"""

# Add these templates after existing templates
UNDER_DEVELOPMENT_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ page_title }} - FakeCMS</title>
    <style>
        body { 
            font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif;
            margin: 0;
            background: #f0f0f1;
            line-height: 1.6;
        }
        header { background: #23282d; padding: 1rem; color: white; }
        .site-title { margin: 0; font-size: 1.8rem; }
        nav { background: #32373c; padding: 0.5rem; }
        nav a { color: #eee; text-decoration: none; margin-right: 1rem; }
        .container { max-width: 800px; margin: 2rem auto; padding: 2rem; background: white; }
    </style>
</head>
<body>
    <header><h1 class="site-title">FakeCMS</h1></header>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/blog">Blog</a>
        <a href="/contact">Contact</a>
        <a href="/login" style="float:right">Login</a>
    </nav>
    <div class="container">
        <h1>{{ page_title }}</h1>
        <p>🚧 This page is currently under development. Please check back later! 🚧</p>
    </div>
</body>
</html>
"""

ABOUT_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>About - FakeCMS</title>
    <style>
        body { 
            font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif;
            margin: 0;
            background: #f0f0f1;
            line-height: 1.6;
        }
        header { background: #23282d; padding: 1rem; color: white; }
        .site-title { margin: 0; font-size: 1.8rem; }
        nav { background: #32373c; padding: 0.5rem; }
        nav a { color: #eee; text-decoration: none; margin-right: 1rem; }
        .container { max-width: 800px; margin: 2rem auto; padding: 2rem; background: white; }
    </style>
</head>
<body>
    <header><h1 class="site-title">FakeCMS</h1></header>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/blog">Blog</a>
        <a href="/contact">Contact</a>
        <a href="/login" style="float:right">Login</a>
    </nav>
    <div class="container">
        <h1>About Us</h1>
        <p>Welcome to FakeCMS, established in 2024. We are a leading provider of content management solutions.</p>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.</p>
        <p>Our mission is to provide the best content management experience for our users. We believe in simplicity, security, and efficiency.</p>
    </div>
</body>
</html>
"""

CONTACT_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Contact - FakeCMS</title>
    <style>
        body { 
            font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif;
            margin: 0;
            background: #f0f0f1;
            line-height: 1.6;
        }
        header { background: #23282d; padding: 1rem; color: white; }
        .site-title { margin: 0; font-size: 1.8rem; }
        nav { background: #32373c; padding: 0.5rem; }
        nav a { color: #eee; text-decoration: none; margin-right: 1rem; }
        .container { max-width: 800px; margin: 2rem auto; padding: 2rem; background: white; }
    </style>
</head>
<body>
    <header><h1 class="site-title">FakeCMS</h1></header>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/blog">Blog</a>
        <a href="/contact">Contact</a>
        <a href="/login" style="float:right">Login</a>
    </nav>
    <div class="container">
        <h1>Contact Us</h1>
        <p>Get in touch with our team:</p>
        <ul>
            <li>Email: info@fakecms.local</li>
            <li>Phone: (555) 123-4567</li>
            <li>Address: 123 CMS Street, Web City, IN 12345</li>
        </ul>
        <p>Office Hours: Monday - Friday, 9:00 AM - 5:00 PM EST</p>
    </div>
</body>
</html>
"""

# Add these routes before if __name__ == '__main__':
@app.route('/about')
def about():
    return render_template_string(ABOUT_PAGE)

@app.route('/contact')
def contact():
    return render_template_string(CONTACT_PAGE)

@app.route('/blog')
def blog():
    return render_template_string(UNDER_DEVELOPMENT_PAGE, page_title="Blog")


@app.route('/') #IMPORTANT ***
def home():
    loggedin = request.cookies.get('loggedin', 'false')
    username = request.cookies.get('username', '')
    
    if loggedin == 'true' and username == 'admin':
        return render_template_string(HOME_PAGE, show_admin_button=True)
    else:
        response = make_response(render_template_string(HOME_PAGE, show_admin_button=False))
        if not request.cookies.get('loggedin'):
            response.set_cookie('loggedin', 'false')
            response.set_cookie('username', '')
        return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'dGVzdEFkbWluVGVzdDIwMjFARmFrZUNNU0AyMDIxdGVzdEFkbWluVGVzdDIwMjFARmFrZUNNU0AyMDIxdGVzdEFkbWluVGVzdDIwMjFARmFrZUNNU0AyMDIxdGVzdEFkbWluVGVzdDIwMjFARmFrZUNNU0AyMDIx' or username == 'umbra' and password == 'P@ssw0rd':
            response = make_response(redirect(url_for('home')))
            response.set_cookie('loggedin', 'true')
            response.set_cookie('username', username)
            return response
        else:
            return render_template_string(LOGIN_PAGE, error='Invalid credentials')
    
    return render_template_string(LOGIN_PAGE)


# Add at top of file after imports
FIRST_NAMES = ['John', 'Jane', 'Mike', 'Sarah', 'Tom', 'Lisa', 'David', 'Emma', 'Chris', 'Amy']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Wilson', 'Taylor']

# Add new endpoint before if __name__ == '__main__':
@app.route('/wp/v2/users')
def users():
    users_list = [{
        "id": 1,
        "name": "Administrator",
        "username": "admin",
        "roles": ["administrator"],
        "_links": {
            "self": [{"href": "/wp/v2/users/admin"}]
        }
    },
    {
        "id": 6,
        "name": "Umbra",
        "username": "umbra",
        "roles": ["editor"],
        "_links": {
            "self": [{"href": "/wp/v2/users/umbra"}]
        }
    }]
    
    for i in range(4):
        username = f"{random.choice(FIRST_NAMES).lower()}.{random.choice(LAST_NAMES).lower()}"
        users_list.append({
            "id": i + 2,
            "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "username": username,
            "roles": ["author"],
            "_links": {
                "self": [{"href": f"/wp/v2/users/{username}"}]
            }
        })
    return jsonify(users_list)


@app.route('/admin')
def admin():
    loggedin = request.cookies.get('loggedin', 'false')
    username = request.cookies.get('username', '')
    
    if loggedin == 'true' and username == 'admin':
        return render_template_string(ADMIN_PAGE, flag=FLAG)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home')))
    response.delete_cookie('loggedin')
    response.delete_cookie('username')
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))  # Default to 8000 if PORT is not set
    app.run(debug=True, host='0.0.0.0', port=port)