import requests
from flask import Flask, request, render_template, jsonify

def fetch_data_from_api(region_id):
    # URL of the api.py application endpoint
    url = 'http://localhost:8000/apiV1-usr'
    
    # Example of sending a POST request with JSON data
    headers = {'Content-Type': 'application/json'}
    data = {'RegionID': region_id}
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        # Process the successful response
        return response.json()
    else:
        # Handle errors or unsuccessful responses
        return None


app = Flask(__name__)

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