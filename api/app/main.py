from fastapi import FastAPI, UploadFile as FastUploadFile
from app.domain.entity import UploadFile

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}


@app.post("/uploadfile/")
async def create_upload_file(file: FastUploadFile):
    upload_file = UploadFile(
        name=file.filename,
        width=100,
        height=100,
        file=await file.read()
    )
    return {"filename": upload_file.name}
