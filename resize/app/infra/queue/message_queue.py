import json
import asyncio
from abc import ABCMeta, abstractmethod
from app.infra.config.base import settings
from aio_pika import connect, Connection, Channel, IncomingMessage


class Processor(metaclass=ABCMeta):
    
    @abstractmethod
    async def execute(self, message: str) -> None:
        pass


class MessageConsumeQueue(metaclass=ABCMeta):

    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def start_consume(self, queue_name: str) -> str:
        ...

    @abstractmethod
    def set_processor(self, processor: Processor) -> None:
        ...


class RabbitMQConsume(MessageConsumeQueue):
    __connection: Connection = None
    __channel: Channel = None
    __processor: Processor = None

    async def connect(self):
        if not self.__connection:
            self.__connection = await connect(settings.MESSAGE_BROKER_URL)
            self.__channel = await self.__connection.channel()

    async def close(self):
        if self.__channel:
            await self.__channel.close()
        if self.__connection:
            await self.__connection.close()

    def set_processor(self, processor: Processor) -> str:
        self.__processor = processor

    async def on_message(self, message: IncomingMessage) -> None:
        async with message.process():
            if self.__processor:
                data = json.loads(message.body)
                await self.__processor.execute(data)

    async def consume(self, queue_name: str):
        await self.connect()
        channel = await self.__connection.channel()
        queue = await channel.declare_queue(queue_name)
        await queue.consume(self.on_message, no_ack=False)

    async def start_consume(self, queue_name: str):
        self.consume_task = asyncio.create_task(self.consume(queue_name))


class Worker:

    topic: str
    processor: Processor
    message_queue: MessageConsumeQueue

    def __init__(self, topic: str, processor: callable, message_queue: MessageConsumeQueue):
        self.topic = topic
        self.processor = processor
        self.message_queue = message_queue

    async def start(self):
        self.message_queue.set_processor(self.processor)        
        await self.message_queue.consume(self.topic)
