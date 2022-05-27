import os
import shutil
from typing import Any, Union
from src.app import app, image_path
import pytest

client = app.test_client()

task_id = "test"
id = "test_id"

CURRENT_DIR = os.path.dirname(__file__)

TEST_DIR = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), "static", "task", "test")


@pytest.fixture(scope='module', autouse=True)
def scope_class() -> None:
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    yield

def copy_image(threshold: Union[int, None] = None) -> Any:
    path = image_path(task_id, id)

    # copy img if img doesn't exist
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
        shutil.copy(f"{CURRENT_DIR}/img/lena.jpg", path)

    if threshold is not None:
        return {'task_id': task_id, 'id': id, 'threshold': threshold}
    else:
        return {'task_id': task_id, 'id': id}


def test_image_path() -> None:
    assert image_path("a", "b") == "/server/static/task/a/b.jpg"


def test_usecase() -> None:
    res = client.post("/upload_image")
    assert res.status_code == 400
    assert res.get_json() == {'error': 'uploadFile is required.'}


def test_gray_scale() -> None:
    res = client.post("/gray_scale", json=copy_image())

    assert res.status_code == 200

    data = res.get_json()

    assert data['result']['image'].pop('id')
    assert data == {
        'result': {
            "image": {
                "task_id": task_id,
                'x': 0,
                'y': 0,
                'width': 512,
                'height': 512
            },
            "params": None
        },
    }


def test_binarize() -> None:
    res = client.post("/binarize", json=copy_image())

    assert res.status_code == 200

    data = res.get_json()

    assert data['result']['image'].pop('id')
    assert data == {
        'result': {
            "image": {
                "task_id": task_id,
                'x': 0,
                'y': 0,
                'width': 512,
                'height': 512
            },
            "params": {
                "threshold": 117
            }
        }
    }


def test_binarize_setting_threshold() -> None:
    threshold = 200
    res = client.post("/binarize", json=copy_image(threshold))

    assert res.status_code == 200

    data = res.get_json()

    assert data['result']['image'].pop('id')
    assert data == {
        'result': {
            "image": {
                "task_id": task_id,
                'x': 0,
                'y': 0,
                'width': 512,
                'height': 512
            },
            "params": {
                "threshold": threshold
            }
        }
    }


def test_face_detection() -> None:
    res = client.post("/face_detection", json=copy_image())

    assert res.status_code == 200

    data = res.get_json()

    assert len(data['result']['params']['faces']) == 1

    assert data['result']['image'].pop('id')
    assert data['result']['params']['faces'][0].pop('id')

    assert data == {
        'result': {
            'image': {
                # 'id': '0f4195f0-ed87-4816-9de3-cd200f227f25',
                'task_id': 'test',
                'x': 0,
                'y': 0,
                'width': 512,
                'height': 512
            },
            'params': {
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
    }
