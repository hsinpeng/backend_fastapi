from fastapi import APIRouter
from utilities.config import get_settings
settings = get_settings()

router = APIRouter(
    tags=["infor"],
    prefix="/info"
)

@router.get("/")
def hello_world():
    return {"App Name": settings.app_name, "Author": settings.author}
