import json
import logging
from abc import ABCMeta, abstractmethod
from app.infra.config.base import settings
from aio_pika import connect, Connection, Channel, Message

logger = logging.getLogger(__name__)

class InputQueue:
    message_topic: str
    message_payload: str
    
    def __init__(self, message_topic: str, message_payload: json):
        self.message_topic = message_topic
        self.message_payload = message_payload


class MessageQueue(metaclass=ABCMeta):

    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def send(self, input: InputQueue) -> None:
        ...

    @abstractmethod
    def receive(self) -> str:
        ...


class RabbitMQ(MessageQueue):
    __connection: Connection = None
    __channel: Channel = None
    
    async def connect(self):
        logger.info(f"Connecting to RabbitMQ at {settings.MESSAGE_BROKER_URL}")
        if not self.__connection:
            self.__connection = await connect(settings.MESSAGE_BROKER_URL)
            self.__channel = await self.__connection.channel()
        logger.info("Connected to RabbitMQ")

    async def send(self, input: InputQueue) -> None:
        logger.info(f"Sending message to queue: {input.message_topic}")
        queue = await self.__channel.declare_queue(input.message_topic)
        await self.__channel.default_exchange.publish(
            Message(input.message_payload.encode()),
            routing_key=queue.name,
        )
        logger.info(f"Message sent to queue: {input.message_topic}")
        
    async def close(self):
        logger.info("Closing RabbitMQ connection")
        if self.__channel:
            await self.__channel.close()
        if self.__connection:
            await self.__connection.close()
        logger.info("RabbitMQ connection closed")

    def receive(self) -> str:
        pass
