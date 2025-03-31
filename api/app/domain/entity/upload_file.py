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
        return f'raw/{self.name}'

    def get_file_path_risized(self, uri: str = ''):
        return f'{uri}{self.width}x{self.height}/{self.name}'
