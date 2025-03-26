from app.infra.config.base import Config
from app.infra.storage.storage import MinioStorage
from app.infra.queue.message_queue import RabbitMQ
from dependency_injector import containers, providers
from app.application.use_case.resize_file import ResizeFile


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Config()])
    config.load()

    storate = providers.Factory(MinioStorage)

    message_queue = providers.Singleton(RabbitMQ)

    resize_file_use_case = providers.Factory(
        ResizeFile,
        storage=storate,
        message_queue=message_queue
    )


