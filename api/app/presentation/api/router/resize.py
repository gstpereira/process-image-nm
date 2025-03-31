import logging
from typing import Annotated
from app.domain.entity import UploadFile
from app.application.use_case import ResizeFile
from app.infra.container.container import Container
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, UploadFile as FastUploadFile, Depends, Query

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/resize",
)

@router.post("/uploadfile/")
@inject
async def create_upload_file(
    file: FastUploadFile,
    resize_file_use_case: Annotated[ResizeFile, Depends(Provide[Container.resize_file_use_case])],
    width: int = Query(gt=0, lt=1201, default=384),
    height: int = Query(gt=0, lt=1201, default=384)):
    logger.info(f"Received file upload request: {file.filename}, width: {width}, height: {height}")
    upload_file = UploadFile(
        name=file.filename,
        width=width,
        height=height,
        size=file.size,
        file=file.file
    )
    output = await resize_file_use_case.execute(upload_file)
    logger.info(f"File processing completed: {upload_file.name}")
    return {"file": output}
