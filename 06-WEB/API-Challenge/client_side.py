from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        region_id = request.form['RegionID']
        testing  = {'RegionID': region_id}
        print(f"Data being passed to API: {testing}")  # Print the data being passed to the API
        response = requests.post('http://127.0.0.1:8000/apiV1-usr', json=testing)
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({"error": response.status_code}), response.status_code
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run on a different port than the API
