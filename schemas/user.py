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
    gender: int
    active: bool
    
class UserRead(UserBase):
    id: int
    email: str
    username: str
    givenname: str
    surname: str
    birthday: date
    gender: int
    active: bool

class UserCreate(UserBase):
    email: str
    password: str
    username: str
    givenname: Optional[str] = Field('John', min_length=2)
    surname: Optional[str] = Field('Doe', min_length=2)
    birthday: date
    gender: int = 1
    active: bool = True

class UserCreateResponse(UserBase):
    id: int
    email: str
    username: str
    givenname: str
    surname: str
    active: bool

class UserUpdate(UserBase):
    email: str
    givenname: str
    surname: str
    birthday: date
    gender: int
    active: bool
    
class UserUpdateResponse(UserBase):
    email: str
    givenname: str
    surname: str
    birthday: date
    gender: int
    active: bool

class UserUpdatePassword(BaseModel):
    email: str
    password:str