from app.domain.entity import UploadFile

def test_initialization():
    name = "image.png"
    width = 1920
    height = 1080
    file_content = b"file content"
    
    upload_file = UploadFile(name, width, height, file_content)
    
    assert upload_file.name == name
    assert upload_file.width == width
    assert upload_file.height == height
    assert upload_file.file == file_content

def test_get_file_path():
    name = "image.png"
    width = 1920
    height = 1080
    file_content = b"file content"
    
    upload_file = UploadFile(name, width, height, file_content)
    expected_path = "1920x1080/image.png"
    
    assert upload_file.get_file_path() == expected_path

