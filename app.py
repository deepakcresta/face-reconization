import os
import base64
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.static_folder, 'captured_images')

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    # List all images in the captured_images folder
    images = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload_image():
    # Get the image data from the request (base64 format)
    image_data = request.form.get('image')
    
    if image_data:
        # Extract image data from base64
        image_data = image_data.split(',')[1]  # Remove the prefix (e.g., "data:image/jpeg;base64,")
        image_bytes = base64.b64decode(image_data)

        # Generate a unique filename based on current time
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'image_{timestamp}.jpg'

        # Save the image in the UPLOAD_FOLDER
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(image_path, 'wb') as f:
            f.write(image_bytes)

        return redirect(url_for('index'))

@app.route('/delete/<int:image_index>', methods=['POST'])
def delete_image(image_index):
    # Get the list of images
    images = os.listdir(UPLOAD_FOLDER)
    
    try:
        # Get the image to be deleted
        image_to_delete = images[image_index]
        image_path = os.path.join(UPLOAD_FOLDER, image_to_delete)
        
        # Delete the image file
        if os.path.exists(image_path):
            os.remove(image_path)
        
        return redirect(url_for('index'))
    except IndexError:
        return "Image not found", 404

if __name__ == '__main__':
    app.run(debug=True)
