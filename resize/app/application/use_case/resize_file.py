import io
import logging
from PIL import Image
from app.domain.entity import UploadFile
from app.infra.storage.storage import Storage
from app.infra.queue.message_queue import Processor

logger = logging.getLogger(__name__)

class ResizeFile(Processor):
    storage: Storage
    
    def __init__(self, storage: Storage):
        self.storage = storage

    async def execute(self, message: str):
        logger.info(f"Processing resize for file: {message.get("file_path")}")
        image_name = message.get("file_path").split("/")[-1]
        image_format = image_name.split(".")[-1]

        image_object = self.storage.get_object(message.get("file_path"))
        image = Image.open(io.BytesIO(image_object))

        resized = image.resize((message.get('width'), message.get('height')))
        logger.info(f"Image {message.get("file_path")} resized to: {message.get('width')}x{message.get('height')}")

        image_memory = io.BytesIO()
        resized.save(image_memory, format=image_format)
        image_memory.seek(0)

        upload_file = UploadFile(
            name=image_name,
            width=message.get('width'),
            height=message.get('height'),
            size=image_memory.getbuffer().nbytes,
            file=image_memory,
        )

        self.storage.save(upload_file)
        logger.info(f"Resized image saved: {upload_file.get_file_path()}")
