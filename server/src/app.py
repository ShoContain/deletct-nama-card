import os
from typing import Any, Tuple
from uuid import uuid4
from cv2 import Mat
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np

app = Flask(__name__, static_folder='../static')
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1MB

SRC_DIR = os.path.dirname(__file__)

TASK_DIR = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), "static", "task")


def image_path(task_id: str, id: str) -> str:
    return os.path.join(TASK_DIR, task_id, f"{id}.jpg")


def error_res(message: str) -> Tuple[Any, int]:
    return jsonify({"error": message}), 400


@app.route("/upload_image", methods=["POST"])
def upload_multipart() -> Any:
    if "uploadFile" not in request.files:
        return jsonify({"error": "uploadFile is required."}), 400
    file = request.files["uploadFile"]
    file_name = file.filename
    if "" == file_name:
        return jsonify({"error": "fileName must not be empty."}), 400

    task_id = str(uuid4())
    id = str(uuid4())
    save_path = image_path(task_id, id)

    os.makedirs(os.path.dirname(save_path))

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


def filter_api(action):
    data = request.get_json()
    task_id = data.get('task_id', '')
    path = image_path(task_id, data.get('id', ''))

    if not os.path.exists(path):
        return error_res("File Not Exists")

    img = cv2.imread(path)
    img, params = action(data, img)

    id = str(uuid4())
    write_path = image_path(task_id, id)
    cv2.imwrite(write_path, img)

    return jsonify({
        "result": {
            "image": {
                "task_id": task_id,
                "id": id,
                "x": 0,
                "y": 0,
                "width": img.shape[1],
                "height": img.shape[0],
            },
            "params": params
        }
    })


@app.route("/gray_scale", methods=["POST"])
def grayscale() -> Any:
    def gray(data,img: Mat) -> Any:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), None

    return filter_api(gray)


@app.route("/binarize", methods=["POST"])
def binarize() -> Any:
    def thre(data, img: Mat) -> Any:
        threshold = int(data.get('threshold', 0))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if threshold == 0:
            threshold, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
        else:
            _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

        return img, {"threshold": threshold}

    return filter_api(thre)


face_cascade = cv2.CascadeClassifier(os.path.join(
    SRC_DIR, 'haarcascade_frontalface_default.xml'))


@app.route("/face_detection", methods=["POST"])
def face_detection() -> Any:
    def fd(data, img: Mat) -> Any:
        task_id = data.get('task_id', '')
        img_with_rect = img.copy()
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
        face_data = []
        for (x, y, w, h) in faces:
            cv2.rectangle(img_with_rect, (x, y), (x+w, y+h), (255, 0, 0), 2)

            face_img = img[y:y+h, x:x+w]
            id = str(uuid4())
            write_path = image_path(task_id, id)
            cv2.imwrite(write_path, face_img)
            face_data.append({
                "task_id": task_id,
                "id": id,
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h),
            })
        return img_with_rect, {
            "faces": face_data
        }
    return filter_api(fd)
