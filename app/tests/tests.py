from fastapi.testclient import TestClient
from app.main import app
import shutil
import tempfile
import pytest

TEMP_DIR = tempfile.mkdtemp()


def cleanup_temp_dir():
    shutil.rmtree(TEMP_DIR)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    yield
    cleanup_temp_dir()


def test_register_patient_success():
    client = TestClient(app)

    response = client.post(
        "/register/",
        data={
            "name": "John Doe",
            "email": "johndoe@example.com",
            "phone": "+1234567890",
        },
        files={"document": ("test.txt", b"Test content")},
    )

    assert response.status_code == 201
    assert response.json() == {"message": "Patient registered successfully."}


def test_register_patient_missing_name():
    client = TestClient(app)

    response = client.post(
        "/register/",
        data={
            "email": "john.doe@example.com",
            "phone": "+1234567890",
        },
        files={"document": ("test.txt", b"Test content")},
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_register_patient_invalid_email():
    client = TestClient(app)

    response = client.post(
        "/register/",
        data={
            "name": "John Doe",
            "email": "invalid-email",
            "phone": "+1234567890",
        },
        files={"document": ("test_file.txt", b"Test content")},
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_register_patient_invalid_phone():
    client = TestClient(app)

    response = client.post(
        "/register/",
        data={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "invalid-phone",
        },
        files={"document": ("test_file.txt", b"Test content")},
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_register_patient_missing_document():
    client = TestClient(app)

    response = client.post(
        "/register/",
        data={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
        },
    )

    assert response.status_code == 422
    assert "detail" in response.json()
