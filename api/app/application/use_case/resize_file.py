import json
import logging
from app.domain.entity import UploadFile
from app.infra.storage.storage import Storage
from app.infra.queue.message_queue import MessageQueue, InputQueue

logger = logging.getLogger(__name__)

class ResizeFile:
    storage: Storage
    message_queue: MessageQueue
    
    def __init__(self, storage: Storage, message_queue: MessageQueue):
        self.storage = storage
        self.message_queue = message_queue

    async def execute(self, upload_file: UploadFile):
        logger.info(f"Starting ResizeFile execution for file: {upload_file.name}")
        self.storage.save(upload_file)
        logger.info(f"File saved to storage: {upload_file.get_file_path()}")

        input_queue = InputQueue("file_resized", json.dumps({
            "width": upload_file.width,
            "height": upload_file.height,
            "file_path": upload_file.get_file_path()
        }))
        await self.message_queue.send(input_queue)
        logger.info(f"Message sent to queue: {input_queue.message_topic}")
        return upload_file.get_file_path_risized(self.storage.get_uri())
