import os
import shutil
from src.app import app, image_path

client = app.test_client()

CURRENT_DIR = os.path.dirname(__file__)


def test_image_path() -> None:
    assert image_path("a", "b") == "/server/static/task/a/b.jpg"


def test_usecase() -> None:
    res = client.post("/upload_image")
    assert res.status_code == 400
    assert res.get_json() == {'error': 'uploadFile is required.'}


def test_face_detection() -> None:
    task_id = "test"
    id = "test_id"
    path = image_path(task_id, id)
    # copy img
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    shutil.copy(f"{CURRENT_DIR}/img/lena.jpg", path)

    res = client.post("/face_detection", json={
        "task_id": task_id, "id": id
    })

    assert res.status_code == 200

    data = res.get_json()

    assert len(data['result']['faces']) == 1

    assert data['result']['image'].pop('id')
    assert data['result']['faces'][0].pop('id')

    assert data == {
        'result': {
            'image': {
                'height': 512,
                # 'id': '0f4195f0-ed87-4816-9de3-cd200f227f25',
                'task_id': 'test',
                'width': 512,
                'x': 0,
                'y': 0
            },
            'faces': [
                {
                    'height': 171,
                    # 'id': '842a58e5-bcc4-4e20-b055-0ae1cbd341bd',
                    'task_id': 'test',
                    'width': 171,
                    'x': 218,
                    'y': 204}
            ]
        }
    }
