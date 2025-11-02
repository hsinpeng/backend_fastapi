from fastapi import APIRouter, File, UploadFile, HTTPException, status
import shutil, pytesseract
from utilities.config import get_settings
settings = get_settings()

router = APIRouter(
    tags=["ocr"],
    prefix="/ocr"
)

@router.post("/image")
def ocr_image(image:UploadFile = File(...)):
    try: 
        file_store_path = f"{settings.local_storage_path}/{image.filename}"
        with open(file_store_path, "w+b") as buffer:
            shutil.copyfileobj(image.file, buffer)
        return pytesseract.image_to_string(file_store_path, lang="eng")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

