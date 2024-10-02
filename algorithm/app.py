from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Define route for the home page that renders the table
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to fetch image data from the external Spring Boot API
@app.route('/api/images', methods=['GET'])
def get_images():
    try:
        # Replace with the actual URL of your Spring Boot API
        api_url = 'http://localhost:8082/api/images/list'
        response = requests.get(api_url)

        # If the API request is successful
        if response.status_code == 200:
            images = response.json()
            return jsonify(images)
        else:
            return jsonify({"error": "Unable to fetch image data"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
