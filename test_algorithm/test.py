# from flask import Flask, render_template, jsonify, request
# import requests
# import cv2
# import numpy as np
# import os
# import base64
# from skimage.metrics import structural_similarity as ssim

# app = Flask(__name__)

# # Route for the home page that renders the table
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Route to fetch image data from the external Spring Boot API
# @app.route('/api/images', methods=['GET'])
# def get_images():
#     try:
#         api_url = 'http://localhost:8082/api/images/list'
#         response = requests.get(api_url)

#         if response.status_code == 200:
#             images = response.json()
#             return jsonify(images)
#         else:
#             return jsonify({"error": "Unable to fetch image data"}), response.status_code
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Route to handle image upload and comparison with API images
# @app.route('/compare', methods=['POST'])
# def compare_image():
#     try:
#         if 'file' not in request.files:
#             return jsonify({"error": "No file part"}), 400
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({"error": "No selected file"}), 400

#         npimg = np.frombuffer(file.read(), np.uint8)
#         uploaded_img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)

#         api_url = 'http://localhost:8082/api/images/list'
#         response = requests.get(api_url)
#         if response.status_code != 200:
#             return jsonify({"error": "Unable to fetch images from API"}), response.status_code

#         images_data = response.json()

#         threshold = 0.05  # 5% match threshold
#         match_results = []  # To store matching results

#         for img_info in images_data:
#             image_path = img_info['path']
#             if not os.path.exists(image_path):
#                 print(f"Image path {image_path} does not exist.")
#                 continue

#             api_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

#             if api_img is None:
#                 print(f"Failed to load image from {image_path}")
#                 continue

#             if uploaded_img.shape != api_img.shape:
#                 api_img_resized = cv2.resize(api_img, (uploaded_img.shape[1], uploaded_img.shape[0]))
#             else:
#                 api_img_resized = api_img

#             score, _ = ssim(uploaded_img, api_img_resized, full=True)
#             print(f"Comparison score with API image {img_info['id']}: {score}")

#             match_status = "Matched" if score >= threshold else "Not Matched"
#             match_results.append({
#                 "image_info": img_info,
#                 "similarity_score": score,
#                 "match_status": match_status
#             })

#         _, uploaded_img_encoded = cv2.imencode('.png', uploaded_img)
#         uploaded_img_base64 = base64.b64encode(uploaded_img_encoded).decode('utf-8')

#         return jsonify({
#             "uploaded_image": uploaded_img_base64,
#             "match_results": match_results
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, jsonify, request
import requests
import cv2
import numpy as np
import os
import base64
from skimage.metrics import structural_similarity as ssim

# Initialize the Flask app
app = Flask(__name__)

# Route for the home page that renders the table
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch image data from the external Spring Boot API
@app.route('/api/images', methods=['GET'])
def get_images():
    try:
        api_url = 'http://localhost:8082/api/images/list'
        response = requests.get(api_url)

        if response.status_code == 200:
            images = response.json()
            return jsonify(images)
        else:
            return jsonify({"error": "Unable to fetch image data"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to handle image upload and comparison with API images
@app.route('/compare', methods=['POST'])
def compare_image():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        npimg = np.frombuffer(file.read(), np.uint8)
        uploaded_img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)

        api_url = 'http://localhost:8082/api/images/list'
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({"error": "Unable to fetch images from API"}), response.status_code

        images_data = response.json()

        threshold = 0.3  # 30% match threshold
        match_results = []  # To store matching results

        for img_info in images_data:
            image_path = img_info['path']
            if not os.path.exists(image_path):
                print(f"Image path {image_path} does not exist.")
                continue

            api_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if api_img is None:
                print(f"Failed to load image from {image_path}")
                continue

            if uploaded_img.shape != api_img.shape:
                api_img_resized = cv2.resize(api_img, (uploaded_img.shape[1], uploaded_img.shape[0]))
            else:
                api_img_resized = api_img

            score, _ = ssim(uploaded_img, api_img_resized, full=True)
            print(f"Comparison score with API image {img_info['id']}: {score}")

            match_status = "Matched" if score >= threshold else "Not Matched"
            match_results.append({
                "image_info": img_info,
                "similarity_score": score,
                "match_status": match_status
            })

            if score >= threshold:
                update_url = f"http://localhost:8082/api/images/{img_info['id']}/present-status"
                update_response = requests.put(update_url)

                if update_response.status_code == 200:
                    print(f"Successfully updated present status for image ID {img_info['id']}.")
                else:
                    print(f"Failed to update present status for image ID {img_info['id']}: {update_response.text}")

        _, uploaded_img_encoded = cv2.imencode('.png', uploaded_img)
        uploaded_img_base64 = base64.b64encode(uploaded_img_encoded).decode('utf-8')

        return jsonify({
            "uploaded_image": uploaded_img_base64,
            "match_results": match_results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
