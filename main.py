from flask import Flask, render_template, request, send_file, send_from_directory
import cv2
import os

# Init the flask app
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
  # Check if an image is uploaded
  if 'image' not in request.files:
      return "No file uploaded", 400

  file = request.files['image']
  if file.filename == '':
      return "No selected file", 400

  # Save the uploaded image
  filepath = os.path.join(UPLOAD_FOLDER, file.filename)
  file.save(filepath)

  # Load the image
  img = cv2.imread(filepath)

  # Convert the image to grayscale
  grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Invert the grayscale image
  invert = cv2.bitwise_not(grey_img)

  # Add a Gaussian blur to the inverted image
  blur = cv2.GaussianBlur(invert, (21, 21), 0)

  # Invert the blurred image
  invertedblur = cv2.bitwise_not(blur)

  # Create the pencil sketch effect
  sketch = cv2.divide(grey_img, invertedblur, scale=256.0)

  # Save the processed image
  processed_path = os.path.join(PROCESSED_FOLDER, f"processed_{file.filename}")
  cv2.imwrite(processed_path, sketch)

  return send_file(processed_path, mimetype='image/png')

if __name__ == '__main__':
  app.run(debug=True)
