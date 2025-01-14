import json
from flask import Flask, render_template, request, jsonify, send_file
import csv
import os
import requests
from flask import Flask, request, render_template, jsonify

#needs to run on a differnt port than the main app

app = Flask(__name__)



# Function to fetch data from the API
def fetch_data_from_api(region_id):
    # Example logic to process the data
    file_name = os.path.join(os.getcwd(), 'apiDirectory', 'userRegion.json')
    with open(file_name, 'r') as jsonfile:
        json_data = json.load(jsonfile)
        for item in json_data:  # Assuming json_data is a list of dictionaries
            if isinstance(item, dict) and str(item.get('RegionID')) == str(region_id):
                return item
    # If no matching item is found, return all data
    return json_data




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
        print(f'fileName={file_name}')

        if not debug_pin:
            if not file_name:
                return jsonify({"error": " 'debugPin' or 'fileName' parameter missing"}), 400
            else:
                return jsonify({"error": "Look At Docs"}), 404
                
        elif debug_pin == '335-818-834' or debug_pin == 335-818-834:
            files = os.listdir(directory_path)
            file_name = request.args.get('fileName')        
            
    
            if file_name == '*':
                return jsonify(files)   
            elif file_name and file_name in files:
                file_path = os.path.join(directory_path, file_name)
                with open(file_path, 'r') as file:
                    file_contents = file.read()
                    return jsonify({"file_contents": file_contents})
            
            elif file_name != '*':
                files = os.listdir(directory_path)
                if file_name in files:
                        file_path = os.path.join(directory_path, file_name)
                        return send_file(file_path, as_attachment=True)
                else:
                        return jsonify({"error": "File not found"}), 404
                
            else:
                return jsonify({"error": "File not found or fileName parameter missing"}), 404
            
        elif debug_pin != '335-818-834' or debug_pin != 335-818-834:
            return jsonify({"error": "Invalid request"}), 403

        else:
            return jsonify({"error": "Invalid request look at  GITHUB FOR DOCUMENTATION "}), 403
        

        
        
    if request.method == 'POST':
        input_json = request.get_json(force=True)  # force=True ensures JSON format
        print('data from client:', input_json)
        region_id = input_json.get('RegionID')
        result = fetch_data_from_api(region_id)
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Region ID not found"}), 404

    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))  # Default to 8000 if PORT is not set
    app.run(debug=False, host='0.0.0.0', port=port)