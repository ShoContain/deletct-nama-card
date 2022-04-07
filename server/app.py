import os
from typing import Any, Tuple
from uuid import uuid4
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB

TASK_DIR = os.path.join(os.path.dirname(__file__), 'static', 'task')


def image_path(task_id: str, id: str) -> str:
    return os.path.join(TASK_DIR, task_id, f"{id}.jpg")


def error_res(message: str) -> Tuple[Any, int]:
    return jsonify({'error': message}), 400


@ app.route("/")
def home() -> str:
    return "Hello, Flask!f"


@ app.route('/upload_image', methods=['POST'])
def upload_multipart() -> Any:
    # <input type="file" name="uploadFile">
    if 'uploadFile' not in request.files:
        return jsonify({'error': 'uploadFile is required.'}), 404
    file = request.files['uploadFile']
    file_name = file.filename
    if '' == file_name:
        return jsonify({'error': 'fileName must not be empty.'}), 400

    task_id = str(uuid4())
    id = str(uuid4())
    save_path = image_path(task_id, id)

    os.makedirs(os.path.dirname(save_path))
    # file.save(save_path)
    # 画像をデコード
    img = cv2.imdecode(np.fromstring(
        file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    cv2.imwrite(save_path, img)
    return jsonify({
        "result": {
            "image": {
                "task_id": task_id,
                "id": id
            }
        }
    })


@ app.route('/gray_scale', methods=['POST'])
def grayscale() -> Any:
    data = request.json

    task_id = data.get('task_id', "")
    path = image_path(task_id, data.get('id', ""))
    if not os.path.exists(os):
        return error_res("File Not Exists")

    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    id = str(uuid4())
    write_path = image_path(task_id, id)
    cv2.imwrite(write_path, img_gray)
    return jsonify({
        "result": {
            "image": {
                "task_id": task_id,
                "id": id
            }
        }
    })
