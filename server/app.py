import os
from uuid import uuid4
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB

TASK_DIR = os.path.join(os.path.dirname(__file__), 'static', 'task')


@ app.route("/")
def home() -> str:
    return "Hello, Flask!f"


@ app.route('/upload_image', methods=['POST'])
def upload_multipart():
    # <input type="file" name="uploadFile">
    if 'uploadFile' not in request.files:
        return jsonify({'error': 'uploadFile is required.'}), 404
    file = request.files['uploadFile']
    file_name = file.filename
    if '' == file_name:
        return jsonify({'error': 'fileName must not be empty.'}), 400

    task_id = str(uuid4())
    id = str(uuid4())
    save_path = os.path.join(TASK_DIR, task_id, f"{id}.jpg")

    os.makedirs(os.path.dirname(save_path))
    file.save(save_path)
    return jsonify({
        "result": {
            "image": {
                "task_id": task_id,
                "id": id
            }
        }
    })

# def grayscale():
#     request_path #uuid/original.jpg
