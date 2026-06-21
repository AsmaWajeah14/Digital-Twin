from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
from pathlib import Path
import shutil

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {"message": "Digital Twin API is running"}


@app.post("/upload-media")
async def upload_media(file: UploadFile = File(...)):
    allowed_types = [
        "image/jpeg",
        "image/png",
        "video/mp4",
        "audio/mpeg",
        "audio/wav"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} is not allowed"
        )

    safe_filename = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Media uploaded successfully",
        "filename": safe_filename,
        "content_type": file.content_type,
        "saved_path": str(file_path)
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)