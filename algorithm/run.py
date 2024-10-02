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
        # Fetch data from the Java API
        response = requests.get(java_api_url)
        if response.status_code == 200:
            images = response.json()
            print('images',images)
            return jsonify(images)
        else:
            return jsonify({"error": "Unable to fetch image data"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
