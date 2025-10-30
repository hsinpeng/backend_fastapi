from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from utilities.jwt import verify_access_token
from utilities.database import get_db
from utilities.tools import get_password_hash, get_user_in_db, check_user_in_db, oauth2_scheme
from models.user import DbUser as UserModel
from schemas import user as UserSchema

router = APIRouter(
    tags=["user"],
    prefix="/user"
)

### query user ###
@router.get("/me", response_model=UserSchema.UserRead, response_description="Get list of user")
async def user_read_me(token:Annotated[str, Depends(oauth2_scheme)], db_session:Annotated[AsyncSession, Depends(get_db)]):
    try :
        payload : dict = await verify_access_token(token)
        u_id:int = payload.get("id")
        username: str = payload.get("username")
        user:UserSchema.UserInDB = await get_user_in_db(id=u_id, username=username, email='', db_session=db_session)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))


@router.get("/all", response_model=List[UserSchema.UserRead], response_description="Get list of user", )
async def user_read_all(db_session:AsyncSession = Depends(get_db)):
    try :
        stmt = select(UserModel)
        response = await db_session.execute(stmt)
        rows = response.scalars().all()
        return rows
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))


@router.get("/email/{email}", response_model=UserSchema.UserRead, response_description="Get user by email", )
async def user_read_by_email(email:str, db_session:AsyncSession = Depends(get_db)):
    try :
        user:UserSchema.UserInDB = await get_user_in_db(email=email, username='', db_session=db_session)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))


### create user ###
@router.post("/create", response_model=UserSchema.UserCreateResponse, status_code=status.HTTP_201_CREATED, response_description="Create new user")
async def create_user(newUser: UserSchema.UserCreate, db_session:AsyncSession = Depends(get_db)):
    try :
        # check if user already exists
        isExist = await check_user_in_db(email=newUser.email, username=newUser.username, db_session=db_session)
        if isExist:
            raise HTTPException(status_code=405, detail="User already exists")
        else:
            # create user
            user = UserModel(
                email=newUser.email,
                password=get_password_hash(newUser.password), #newUser.password,
                username=newUser.username,
                givenname=newUser.givenname,
                surname=newUser.surname,
                birthday=newUser.birthday,
                gender=newUser.gender,
                active=newUser.active
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
            return user
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))


### update user info###
@router.put("/update/info", status_code=200, response_model=UserSchema.UserUpdateResponse, response_description="Update user info")
async def update_user_info(newUser:UserSchema.UserUpdate, db_session:AsyncSession = Depends(get_db)):
    try :
        # check if user already exists
        isExist = await check_user_in_db(email=newUser.email, username='', db_session=db_session)
        if isExist:
            stmt = update(UserModel).where(UserModel.email == newUser.email).values(
                givenname=newUser.givenname,
                surname=newUser.surname,
                birthday=newUser.birthday,
                gender=newUser.gender,
                active=newUser.active
            )
            await db_session.execute(stmt)
            await db_session.commit()
            return newUser
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))


### update password ###
@router.put("/update/password", status_code=200, response_model=str, response_description="Update password")
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
            return f'password of {newUser.email} has been changed'
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))
    

### delete user ###
@router.delete("/email/{email}", response_model=str, response_description="Delete user by email", )
async def user_remove_by_email(email:str, db_session:AsyncSession = Depends(get_db)):
    try :
        # check if user already exists
        isExist = await check_user_in_db(email=email, username='', db_session=db_session)
        if isExist:
            stmt = delete(UserModel).where(UserModel.email == email)
            await db_session.execute(stmt)
            await db_session.commit()
            return f'account of {email} has been deleted'
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))

