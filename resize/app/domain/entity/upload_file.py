class UploadFile:
    name: str
    width: int
    height: int
    size: int
    file: bytes
    
    def __init__(self, name: str, width: int, height: int, size: int, file: bytes):
        self.name = name
        self.width = width
        self.height = height
        self.size = size
        self.file = file
        
    def get_file_path(self):
        return f'{self.width}x{self.height}/{self.name}'
