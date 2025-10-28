from fastapi import APIRouter, Depends, status
from typing import List, Optional, Union
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from utilities.database import get_db
from utilities.tools import get_password_hash, get_user_in_db, check_user_in_db
from models.user import User as UserModel
from schemas import user as UserSchema
from schemas.base import GenericResponse

router = APIRouter(
    tags=["user"],
    prefix="/user"
)

### query user ###
@router.get("/all", response_model=GenericResponse[Optional[List[UserSchema.UserRead]]], response_description="Get list of user", )
async def user_read_all(db_session:AsyncSession = Depends(get_db)):
    try :
        stmt = select(UserModel)
        response = await db_session.execute(stmt)
        rows = response.scalars().all()
        result = {"message": "OK", "data":rows}
    except Exception as e:
        result = {"message": f"Error: {e}", "data":None}

    return result

@router.get("/email/{email}", response_model=GenericResponse[Optional[Union[str,UserSchema.UserRead]]], response_description="Get user by email", )
async def user_read_by_email(email:str, db_session:AsyncSession = Depends(get_db)):
    try :
        # stmt = select(UserModel).where(UserModel.email == email)
        # result = await db_session.execute(stmt)
        # row = result.scalars().first()
        user:UserSchema.UserInDB = await get_user_in_db(email=email, username='', db_session=db_session)
        if user:
            result = {"message": "OK", "data":user}
        else:
            result = {"message": "No user", "data":email}
    except Exception as e:
        result = {"message": f"Error: {e}", "data":None}

    return result

### create user ###
@router.post("/create", response_model=GenericResponse[Optional[UserSchema.UserCreateResponse]], status_code=status.HTTP_201_CREATED, response_description="Create new user")
async def create_user(newUser: UserSchema.UserCreate, db_session:AsyncSession = Depends(get_db)):
    try :
        # check if user already exists
        isExist = await check_user_in_db(email=newUser.email, username=newUser.username, db_session=db_session)
        if isExist:
            result = {"message": "User already exists", "data":None}
        else:
            # create user
            user = UserModel(
                email=newUser.email,
                password=get_password_hash(newUser.password), #newUser.password,
                username=newUser.username,
                givenname=newUser.givenname,
                surname=newUser.surname,
                birthday=newUser.birthday,
                sex=newUser.sex
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
            result = {"message": "OK", "data":user}
    except Exception as e:
        print(f'Error: {e}')
        result = {"message": f"Error: {e}", "data":None}

    return result


### update user info###
@router.put("/update/info", status_code=200, response_model=GenericResponse[Optional[UserSchema.UserUpdateResponse]], response_description="Update user info")
async def update_user_info(newUser:UserSchema.UserUpdate, db_session:AsyncSession = Depends(get_db)):
    try :
        # check if user already exists
        isExist = await check_user_in_db(email=newUser.email, username='', db_session=db_session)
        if isExist:
            stmt = update(UserModel).where(UserModel.email == newUser.email).values(
                givenname=newUser.givenname,
                surname=newUser.surname,
                birthday=newUser.birthday,
                sex=newUser.sex
            )
            await db_session.execute(stmt)
            await db_session.commit()
            result = {"message": "User info update OK", "data": newUser}
        else:
            result = {"message": "No such user to update info", "data": newUser}
    except Exception as e:
        result = {"message": f"Error: {e}", "data":None}

    return result

### update password ###
@router.put("/update/password", status_code=200, response_model=GenericResponse[Optional[str]], response_description="Update password")
async def update_user_password(newUser:UserSchema.UserUpdatePassword, db_session:AsyncSession = Depends(get_db)):
    try :
        # check if user already exists
        isExist = await check_user_in_db(email=newUser.email, username='', db_session=db_session)
        if isExist:
            stmt = update(UserModel).where(UserModel.email == newUser.email).values(
                password=get_password_hash(newUser.password), #newUser.password,
            )
            await db_session.execute(stmt)
            await db_session.commit()
            result = {"message": "Passowrd update OK", "data": newUser.email}
        else:
            result = {"message": "No such user to update password", "data": newUser.email}
    except Exception as e:
        result = {"message": f"Error: {e}", "data":None}

    return result

### delete user ###
@router.delete("/email/{email}", response_model=GenericResponse[Optional[str]], response_description="Delete user by email", )
async def user_remove_by_email(email:str, db_session:AsyncSession = Depends(get_db)):
    try :
        # check if user already exists
        isExist = await check_user_in_db(email=email, username='', db_session=db_session)
        if isExist:
            stmt = delete(UserModel).where(UserModel.email == email)
            await db_session.execute(stmt)
            await db_session.commit()
            result = {"message": "Delete OK", "data": email}
        else:
            result = {"message": "No such user to delete", "data": email}
    except Exception as e:
        result = {"message": f"Error: {e}", "data":None}

    return result
