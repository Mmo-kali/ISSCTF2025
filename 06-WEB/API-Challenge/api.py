import json
from flask import Flask, render_template, request, jsonify, send_file
import csv
import os
import requests
from flask import Flask, request, render_template, jsonify

#needs to run on a differnt port than the main app

app = Flask(__name__)

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



@app.route('/apiV1-usr', methods=['GET', 'POST'])
def read_csv():
    script_dir = os.path.dirname(__file__)  # Gets the directory where the script is located
    directory_path = os.path.join(script_dir, 'apiDirectory')  # Correctly builds the path

    if request.method == 'GET':
        debug_pin = request.args.get('debugPin')
        file_name = request.args.get('fileName')

        if not debug_pin:
            if not file_name:
                return jsonify({"error": " 'debugPin' or 'fileName' parameter missing"}), 400
            else:

                files = os.listdir(directory_path)
                if file_name in files:
                    file_path = os.path.join(directory_path, file_name)
                    return send_file(file_path, as_attachment=True)
                else:
                    return jsonify({"error": "File not found"}), 404
                
        elif debug_pin == '123-456-789' or debug_pin == 123-456-789:
            files = os.listdir(directory_path)
            file_name = request.args.get('fileName')        
            
    
            if file_name == '*':
                return jsonify(files)
            elif file_name and file_name in files:
                file_path = os.path.join(directory_path, file_name)
                with open(file_path, 'r') as file:
                    file_contents = file.read()
                    return jsonify({"file_contents": file_contents})
            else:
                return jsonify({"error": "File not found or fileName parameter missing"}), 404
            
        elif debug_pin != '123-456-789' or debug_pin != 123-456-789:
            return jsonify({"error": "Invalid request"}), 403

        else:
            return jsonify({"error": "Invalid request look at  GITHUB FOR DOCUMENTATION "}), 403
        

        
        
    elif request.method == 'POST':
        input_json = request.get_json(force=True)  # force=True ensures JSON format
        print('data from client:', input_json)
        region_id = input_json.get('RegionID')
        file_name = r'apiDirectory\userRegion.json'  # Adjust your JSON file name as necessary

    
        with open(file_name, 'r') as jsonfile:
            json_data = json.load(jsonfile)
            for item in json_data:  # Assuming json_data is a list of dictionaries
                if str(item.get('RegionID')) == str(region_id):
                    return jsonify(item)
        # If the loop completes without finding the region ID, return an error
        return jsonify({"error": "Region ID not found"}), 404
    
if __name__ == '__main__':
    app.run(debug=True, port=8000) # specify the port number here