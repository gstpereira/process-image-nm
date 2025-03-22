from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
