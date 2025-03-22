from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_create_upload_file():
    test_file_content = b"test content"
    test_file_name = "test.txt"
    files = {"file": (test_file_name, test_file_content)}

    response = client.post("/uploadfile/", files=files)
    assert response.status_code == 200
    assert response.json() == {"filename": test_file_name}
