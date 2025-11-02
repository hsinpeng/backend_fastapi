import shutil
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from utilities.config import get_settings
settings = get_settings()

router = APIRouter(
    tags=["file"],
    prefix="/file"
)

### upload file ###
@router.post("/file")
async def post_display_file(upload_file:bytes = File(...)):
    try:
        content = upload_file.decode('utf-8')
        lines = content.split('\n')
        return lines
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/upload")
async def post_upload_file(upload_file:UploadFile = File(...)):
    try: 
        file_store_path = f"{settings.local_storage_path}/{upload_file.filename}"
        with open(file_store_path, "w+b") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return {"file": file_store_path, "type": upload_file.content_type}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

### download file ###
@router.get("/download/{filename}")
async def get_download_file(filename:str):
    file_to_download:str = f"{settings.local_storage_path}/{filename}"
    try:
        if Path(file_to_download).is_file():
            return FileResponse(path=file_to_download)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"file {filename} doesn't exist")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))