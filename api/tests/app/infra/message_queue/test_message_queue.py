import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.infra.queue.message_queue import RabbitMQ, InputQueue

pytest_plugins = ('pytest_asyncio',)

@pytest.fixture
def mock_settings():
    with patch("app.infra.queue.message_queue.settings") as mock_settings:
        mock_settings.MESSAGE_BROKER_URL = "amqp://test-url"
        yield mock_settings


@pytest.fixture
def mock_aio_pika():
    with patch("app.infra.queue.message_queue.connect", new_callable=AsyncMock) as mock_connect:
        mock_connection = AsyncMock()
        mock_channel = AsyncMock()
        mock_connection.channel.return_value = mock_channel
        mock_connect.return_value = mock_connection
        yield mock_connect, mock_connection, mock_channel


@pytest.mark.asyncio
async def test_rabbitmq_connect(mock_settings, mock_aio_pika):
    mock_connect, mock_connection, mock_channel = mock_aio_pika

    rabbitmq = RabbitMQ()
    await rabbitmq.connect()

    mock_connect.assert_called_once_with(mock_settings.MESSAGE_BROKER_URL)
    mock_connection.channel.assert_called_once()
    assert rabbitmq._RabbitMQ__connection == mock_connection
    assert rabbitmq._RabbitMQ__channel == mock_channel


@pytest.mark.asyncio
async def test_rabbitmq_send(mock_settings, mock_aio_pika):
    mock_connect, mock_connection, mock_channel = mock_aio_pika
    mock_queue = AsyncMock()
    mock_channel.declare_queue.return_value = mock_queue

    rabbitmq = RabbitMQ()
    await rabbitmq.connect()

    input_queue = InputQueue(message_topic="test_topic", message_payload="test_payload")
    await rabbitmq.send(input_queue)

    mock_channel.declare_queue.assert_called_once_with("test_topic")
    mock_channel.default_exchange.publish.assert_called_once()
    published_message = mock_channel.default_exchange.publish.call_args[0][0]
    assert published_message.body == b"test_payload"
    # assert mock_channel.default_exchange.publish.call_args[1]["routing_key"] == "test_topic"


@pytest.mark.asyncio
async def test_rabbitmq_close(mock_settings, mock_aio_pika):
    mock_connect, mock_connection, mock_channel = mock_aio_pika

    rabbitmq = RabbitMQ()
    await rabbitmq.connect()
    await rabbitmq.close()

    mock_channel.close.assert_called_once()
    mock_connection.close.assert_called_once()