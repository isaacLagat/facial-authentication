from flask import Flask, request, jsonify
import base64
import face_recognition
from io import BytesIO
from PIL import Image
import numpy as np

app = Flask(__name__)

# Load a known image (for demonstration purposes, replace with your own logic)
known_image = face_recognition.load_image_file("known_image.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    image_data = data['image'].split(",")[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image_np = np.array(image)

    unknown_face_encodings = face_recognition.face_encodings(image_np)
    if len(unknown_face_encodings) == 0:
        return jsonify({"message": "No face detected."})

    matches = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
    if matches[0]:
        return jsonify({"message": "Authentication successful!"})
    else:
        return jsonify({"message": "Authentication failed."})

if __name__ == '__main__':
    app.run(debug=True)
