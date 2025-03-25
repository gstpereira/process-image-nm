from typing import Annotated
from fastapi import Depends
from app.infra.storage.storage import Storage
from app.domain.entity import UploadFile

class ResizeFile:
    storage: Storage
    
    def __init__(self, storage: Storage):
        self.storage = storage

    async def execute(self, upload_file: UploadFile):
        self.storage.save(upload_file)
