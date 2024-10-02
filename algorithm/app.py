# import requests
# from flask import Flask, render_template, jsonify

# app = Flask(__name__)

# # API endpoint to get images from your Spring Boot API
# API_URL = "http://localhost:8080/api/images/list"  # Change this to your Spring Boot API URL

# @app.route('/')
# def index():
#     try:
#         # Make a GET request to the Spring Boot API
#         response = requests.get(API_URL)
#         print
#         images = response.json()  # Convert the response to JSON
#         return render_template('index.html', images=images)
#     except Exception as e:
#         print(f"Error fetching images: {e}")
#         return "Error fetching images", 500

# if __name__ == '__main__':
#     app.run(debug=True)
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# API endpoint to get images from your Spring Boot API
API_URL = "http://localhost:8080/api/images/list"

@app.route('/')
def index():
    try:
        # Make a GET request to the Spring Boot API
        response = requests.get(API_URL)
        images = response.json()  # Convert the response to JSON
        return render_template('index.html', images=images)
    except Exception as e:
        print(f"Error fetching images: {e}")
        return "Error fetching images", 500

if __name__ == '__main__':
    app.run(debug=True)
