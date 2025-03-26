import pytest
from app.domain.entity.upload_file import UploadFile

name = "image.png"
width = 1920
height = 1080
size = 12
file_content = b"file content"


@pytest.fixture
def upload_file():
    return UploadFile(name, width, height, size, file_content)


def test_initialization(upload_file):
    assert upload_file.name == name
    assert upload_file.width == width
    assert upload_file.height == height
    assert upload_file.file == file_content


def test_get_file_path(upload_file):
    expected_path = "raw/image.png"

    assert upload_file.get_file_path() == expected_path

