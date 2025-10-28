from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Union
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.auth import login_form_schema, Token, RefreshRequest
from schemas.user import UserInDB
from models.user import User as UserModel
from utilities.tools import verify_password
from utilities.jwt import create_token_pair, verify_refresh_token
from utilities.database import get_db


router = APIRouter(
    tags=["auth"],
    prefix="/auth",
)


exception_invalid_token = HTTPException(
    status_code=401,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"}
)

exception_invalid_login = HTTPException(
    status_code=401,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"}
)

@router.post("/login", response_model=Optional[Union[str, Token]])
async def login(form_data:login_form_schema, db_session:AsyncSession = Depends(get_db)):
    """
    Login with the following information:

    - **username**
    - **password**

    """
    try:
        user_in_db:UserInDB = await get_user_in_db(email='', username=form_data.username, db_session=db_session)
        print()
        if user_in_db is None:
            #raise exception_invalid_login
            result = "Incorrect username or password"
        elif not verify_password(form_data.password, user_in_db.password):
            #raise exception_invalid_login
            result = "Incorrect username or password"
        else:
            result = await create_token_pair(
                {"username": user_in_db.username, "id": user_in_db.id},
                {"username": user_in_db.username, "id": user_in_db.id},
            )
    except Exception as e:
        result = e
    
    return result
    

@router.post("/refresh", response_model=Optional[Union[str, Token]])
async def refresh(refersh_data: RefreshRequest):
    """
    Refresh token with the following information:

    - **token** in `Authorization` header

    """
    try:
        payload : dict = await verify_refresh_token(refersh_data.refresh_token)
        username: str = payload.get("username")
        u_id:int = payload.get("id")
        if username is None or u_id is None:
            #raise  exception_invalid_token
            result = "Invalid token"
        else:
            result = await create_token_pair(
                {"username": username , "id": u_id},
                {"username": username , "id": u_id}
            )
    except Exception as e:
        result = e
    
    return result

### tools ###
async def get_user_in_db(email:str, username:str, db_session:AsyncSession) -> UserInDB :
    stmt = select(UserModel).where(or_(UserModel.username == username, UserModel.email == email))
    result = await db_session.execute(stmt)
    user = result.scalars().first()
    if user:
        return user
    else:
        return None