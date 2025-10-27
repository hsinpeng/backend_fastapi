import json
from fastapi import APIRouter, Depends
from datetime import date
from sqlalchemy import text, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from utilities.database import get_db
from models.user import User as UserModel
from schemas import user as UserSchema
from typing import List

router = APIRouter(
    tags=["user"],
    prefix="/user"
)

@router.get("/all", response_model=List[UserSchema.UserRead], response_description="Get list of user", )
async def user_read_all(db_session:AsyncSession = Depends(get_db)):
    try :
        stmt = select(UserModel)
        result = await db_session.execute(stmt)
        rows = result.scalars().all()
    except Exception as e:
        print(e)

    return rows

@router.get("/email/{email}", response_model=UserSchema.UserRead, response_description="Get user by email", )
async def user_read_by_email(email:str, db_session:AsyncSession = Depends(get_db)):
    try :
        stmt = select(UserModel).where(UserModel.email == email)
        result = await db_session.execute(stmt)
        row = result.scalars().first()
    except Exception as e:
        print(e)

    return row