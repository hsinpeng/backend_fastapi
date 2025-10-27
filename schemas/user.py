from typing import Union, Optional
from datetime import date
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    email: str

class UserInDB(BaseModel):
    id: int
    email: str
    password: str
    username: str
    givenname: str
    surname: str
    birthday: date
    sex: int
    
class UserRead(UserBase):
    id: int
    email: str
    username: str
    givenname: str
    surname: str
    birthday: date
    sex: int

class UserCreate(UserBase):
    email: str
    password: str
    username: str
    givenname: Optional[str] = Field(min_length=2)
    surname: Optional[str] = Field(min_length=2)
    birthday: date
    sex: int

class UserCreateResponse(UserBase):
    id: int
    email: str
    username: str
    givenname: str
    surname: str

class UserUpdate(UserBase):
    email: str
    givenname: str
    surname: str
    birthday: date
    sex: int
    
class UserUpdateResponse(UserBase):
    email: str
    givenname: str
    surname: str
    birthday: date
    sex: int

class UserUpdatePassword(BaseModel):
    email: str
    password:str