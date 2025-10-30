from fastapi import APIRouter

router = APIRouter(
    tags=["infor"],
    prefix="/info"
)

@router.get("/")
def hello_world():
    return "Hello FastAPI!"
