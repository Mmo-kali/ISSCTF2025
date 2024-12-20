from flask import Flask, request, jsonify
import http.client
import json
import requests
from flask import Flask, request, render_template, jsonify


app = Flask(__name__)

def fetch_data_from_api(region_id):
    host = 'localhost'
    port = 8000
    endpoint = '/apiV1-usr'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'RegionID': region_id})

    connection = http.client.HTTPConnection(host, port)
    connection.request('POST', endpoint, body=data, headers=headers)

    response = connection.getresponse()

    if response.status == 200:
        response_data = response.read()
        connection.close()
        return json.loads(response_data)
    else:
        connection.close()
        return None

@app.route('/get-data', methods=['POST'])
def get_data():
    content = request.json
    region_id = content['RegionID']
    result = fetch_data_from_api(region_id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract data from the form submission
        region_id = request.form.get('regionID')
        # Fetch data from the api.py application
        result = fetch_data_from_api(region_id)
        if result:
            # Return the result to the user
            return jsonify(result)
        else:
            # Return an error message if the API call was unsuccessful
            return jsonify({'error': 'Failed to fetch data from the API'}), 500 #here
    else:
        # For a GET request, just render the index page
        return render_template('index.html')

# Ensure the fetch_data_from_api function is defined as shown previously



if __name__ == '__main__':
    app.run(debug=True)