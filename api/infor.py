from fastapi import APIRouter, Depends
from datetime import date
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from utilities.database import get_db
from models.user import User as UserModel

router = APIRouter(
    tags=["infor"],
    prefix="/info"
)

@router.get("/")
def hello_world():
    return "Hello FastAPI!"
