import pytest
from unittest.mock import AsyncMock, MagicMock
from io import BytesIO
from fastapi import UploadFile as FastUploadFile
from app.domain.entity import UploadFile
from app.application.use_case import ResizeFile
from app.presentation.api.router.resize import create_upload_file

@pytest.fixture
def mock_file():
    file_mock = MagicMock(spec=FastUploadFile)
    file_mock.filename = "test_image.jpg"
    file_mock.size = 1024
    file_mock.file = BytesIO(b"fake image content")
    return file_mock


@pytest.fixture
def mock_resize_file_use_case():
    use_case = AsyncMock(spec=ResizeFile)
    use_case.execute = AsyncMock()
    return use_case


@pytest.mark.asyncio
async def test_create_upload_file(mock_file, mock_resize_file_use_case):
    mock_resize_file_use_case.execute.return_value = "100x100/test_image.jpg"

    result = await create_upload_file(mock_file, mock_resize_file_use_case, 100, 100)

    assert result == {"file": "100x100/test_image.jpg"}
    mock_resize_file_use_case.execute.assert_called_once()

    called_args = mock_resize_file_use_case.execute.call_args[0][0]
    assert isinstance(called_args, UploadFile)
    assert called_args.name == "test_image.jpg"
    assert called_args.width == 100
    assert called_args.height == 100
    assert called_args.size == 1024
    assert called_args.file == mock_file.file


@pytest.mark.asyncio
async def test_create_upload_file_with_error():
    mock_file = MagicMock(spec=FastUploadFile)
    mock_file.filename = "test_image.jpg"
    mock_file.size = 1024
    mock_file.file = BytesIO(b"fake image content")
    
    mock_resize_file_use_case = AsyncMock(spec=ResizeFile)
    mock_resize_file_use_case.execute.side_effect = Exception("Error processing image")
    
    with pytest.raises(Exception, match="Error processing image"):
        await create_upload_file(mock_file, mock_resize_file_use_case)
