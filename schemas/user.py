from typing import Union, Optional
from datetime import date
from pydantic import BaseModel, Field

# class Item(BaseModel):
#     title: str
#     content: str

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
    email: str = 'user@email.com'
    username: str
    givenname: str
    surname: str
    birthday: date
    gender: int
    active: bool
    # items: list[Item] = []
    # class Config:
    #     orm_mode = True

class UserCreate(UserBase):
    email: str = 'user@email.com'
    password: str = '123456'
    username: str = 'user'
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
    email: str = 'user@email.com'
    givenname: Optional[str] = Field('John', min_length=2)
    surname: Optional[str] = Field('Doe', min_length=2)
    birthday: date
    gender: int = 1
    active: bool = True
    
class UserUpdateResponse(UserBase):
    email: str
    givenname: str
    surname: str
    birthday: date
    gender: int
    active: bool

class UserUpdatePassword(BaseModel):
    email: str = 'user@email.com'
    password:str = '123456'