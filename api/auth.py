from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
#from typing import Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.auth import login_form_schema, Token, RefreshRequest
from schemas.user import UserInDB
from utilities.tools import verify_password, get_user_in_db, oauth2_scheme
from utilities.jwt import create_token_pair, verify_refresh_token, verify_access_token
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

@router.post("/login", response_model=Token)
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
            raise exception_invalid_login
        elif not verify_password(form_data.password, user_in_db.password):
            raise exception_invalid_login
        else:
            result = await create_token_pair(
                {"username": user_in_db.username, "id": user_in_db.id},
                {"username": user_in_db.username, "id": user_in_db.id},
            )
            return result
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))
    
    
@router.post("/refresh", response_model=Token)
async def refresh(refersh_data: RefreshRequest, token: Annotated[str, Depends(oauth2_scheme)]): # refersh_data: RefreshRequest): #, token: oauth2_token_scheme):
    """
    Refresh token with the following information:

    - **token** in `Authorization` header

    """
    try:
        accessPayload : dict = await verify_access_token(token)
        print(f'token={token}, accessPayload={accessPayload}')
        #######################
        payload : dict = await verify_refresh_token(refersh_data.refresh_token)
        username: str = payload.get("username")
        u_id:int = payload.get("id")
        if username is None or u_id is None:
            raise  exception_invalid_token
        else:
            result = await create_token_pair(
                {"username": username , "id": u_id},
                {"username": username , "id": u_id}
            )
            return result
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))
