from typing import Annotated
from app.domain.entity import UploadFile
from app.application.use_case import ResizeFile
from app.infra.container.container import Container
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, UploadFile as FastUploadFile, Depends

router = APIRouter(
    prefix="/resize",
)

@router.post("/uploadfile/")
@inject
async def create_upload_file(
    file: FastUploadFile,
    resize_file_use_case: Annotated[ResizeFile, Depends(Provide[Container.resize_file_use_case])],
    width: int = 384,
    height: int = 384):
    upload_file = UploadFile(
        name=file.filename,
        width=width,
        height=height,
        size=file.size,
        file=file.file
    )
    await resize_file_use_case.execute(upload_file)
    return {"filename": upload_file.name}
