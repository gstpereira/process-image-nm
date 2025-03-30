import json
from app.domain.entity import UploadFile
from app.infra.storage.storage import Storage
from app.infra.queue.message_queue import MessageConsumeQueue, Processor


class ResizeFile(Processor):
    storage: Storage
    message_queue: MessageConsumeQueue
    
    def __init__(self, storage: Storage, message_queue: MessageConsumeQueue):
        self.storage = storage
        self.message_queue = message_queue

    async def execute(self, message: str):
        print(f"Execute message - ResizeFile: {type(message)}")

        # input_queue = InputQueue("file_resized", json.dumps({
        #     "width": upload_file.width,
        #     "height": upload_file.height,
        #     "file_path": upload_file.get_file_path()
        # }))
        # self.storage.save(upload_file)
