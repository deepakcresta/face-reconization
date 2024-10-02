from flask import Flask, jsonify, send_from_directory, request
import os
import requests

app = Flask(__name__)

# Serve index.html from the root route
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Fetch student data from the external API
@app.route('/get-students', methods=['GET'])
def get_students():
    java_api_url = 'http://localhost:8082/api/students/ids-and-images'  # Change to your API URL

    try:
        # Fetch data from the Java API
        response = requests.get(java_api_url)
        print('rspo')
        if response.status_code == 200:
            students_data = response.json()

            # Filter students with valid image paths
            students_with_images = [
                {'id': student['id'], 'imagePath': student.get('imagePath')}
                for student in students_data if student.get('imagePath')
            ]
            return jsonify(students_with_images)
        else:
            return jsonify({'error': 'Failed to retrieve data'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
