import json
from abc import ABCMeta, abstractmethod
from app.infra.config.base import settings
from aio_pika import connect, Connection, Channel, Message

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
        if not self.__connection:
            self.__connection = await connect(settings.MESSAGE_BROKER_URL)
            self.__channel = await self.__connection.channel()

    async def send(self, input: InputQueue) -> None:
        queue = await self.__channel.declare_queue(input.message_topic)
        await self.__channel.default_exchange.publish(
            Message(input.message_payload.encode()),
            routing_key=queue.name,
        )
        
    async def close(self):
        if self.__channel:
            await self.__channel.close()
        if self.__connection:
            await self.__connection.close()

    def receive(self) -> str:
        pass
