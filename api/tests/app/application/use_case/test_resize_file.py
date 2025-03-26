import pytest
from unittest.mock import MagicMock, AsyncMock
from app.application.use_case.resize_file import ResizeFile
from app.domain.entity import UploadFile


@pytest.fixture
def mock_storage():
    return MagicMock()


@pytest.fixture
def mock_message_queue():
    return AsyncMock()

@pytest.fixture
def mock_upload_file():
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.get_file_path.return_value = "mock/path/to/file"
    mock_file.file = b"mock file content"
    mock_file.width = 100
    mock_file.height = 200
    return mock_file


@pytest.mark.asyncio
async def test_resize_file_execute_saves_file(mock_storage, mock_message_queue, mock_upload_file):
    resize_file_use_case = ResizeFile(storage=mock_storage, message_queue=mock_message_queue)

    await resize_file_use_case.execute(mock_upload_file)

    mock_storage.save.assert_called_once_with(mock_upload_file)
