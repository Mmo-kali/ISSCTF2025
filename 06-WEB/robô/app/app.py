from flask import Flask, render_template_string
import lorem

app = Flask(__name__)

# Add this list near the top of the file
TRANSFORMER_IMAGES = [
    "/static/images/image1.jpg",
    "/static/images/image2.jpg",
    "/static/images/image3.jpg",
    "/static/images/image4.jpg",
    "/static/images/image5.jpg",
    "/static/images/image6.jpg",
    "/static/images/image7.jpg",
    "/static/images/image8.jpg",
    "/static/images/image9.jpg",
    "/static/images/image10.jpg"
]

# Update the HOME_PAGE template to include images
HOME_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Transformers Fan Hub</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }
        .header {
            background: url('/static/images/banner1.jpg') no-repeat center center,
                      linear-gradient(135deg, #1a237e, #0d47a1);
            background-size: cover;
            position: relative;
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            min-height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(26, 35, 126, 0.7);
            z-index: 1;
        }
        .header h1, .header p {
            position: relative;
            z-index: 2;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin: 10px 0;
        }
        .banner-image {
            max-width: 400px;
            height: auto;
            margin: 20px auto;
            display: block;
            position: relative;
            z-index: 2;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .blog-post {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .blog-title {
            color: #1a237e;
            font-size: 1.5em;
        }
        .blog-image {
            width: 100%;
            max-width: 300px;
            height: auto;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Transformers Fan Hub</h1>
        <p>Your Ultimate Source for Cybertron News</p>
    </div>
    <div class="container">
        {% for i in range(10) %}
        <div class="blog-post">
            <h2 class="blog-title">Transformers Blog #{{i+1}}</h2>
            <img src="{{images[i]}}" alt="Transformer" class="blog-image">
            <p>{{blogs[i]}}</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

# Update the home route to pass images
@app.route('/')
def home():
    blogs = [lorem.paragraph() for _ in range(10)]
    return render_template_string(HOME_PAGE, blogs=blogs, images=TRANSFORMER_IMAGES)

# Hidden admin endpoint template
ADMIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
</head>
<body>
    <h1>Congratulations!</h1>
    <p>Flag: bhbureauCTF{r0b0ts_txt_1s_n0t_s3cur3}</p>
</body>
</html>
'''



@app.route('/robots.txt')
def robots():
    return '''
User-agent: *
Disallow: /unprotected-admin-endpoint
'''

@app.route('/unprotected-admin-endpoint')
def admin():
    return ADMIN_PAGE

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))  # Default to 8000 if PORT is not set
    app.run(debug=False, host='0.0.0.0', port=port)