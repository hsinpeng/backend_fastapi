from typing import Union, Optional
from datetime import date
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    email: str
    username: str

class UserInDB(BaseModel):
    id: int
    email: str
    password: str
    username: str
    birthday: date
    sex: bool
    
class UserRead(UserBase):
    id: int
    email: str
    username: str
    birthday: date
    sex: bool

class UserCreate(UserBase):
    id: int
    email: str
    password: str
    username: str
    birthday: date
    sex: bool

class UserCreateResponse(UserBase):
    username: str
    email: str

class UserUpdate(UserBase):
    username: Optional[str] = Field(min_length=6)
    birthday: Optional[date] = Field()

class UserUpdatePassword(BaseModel):
    password:str
    
class UserUpdateResponse(UserBase):
    username: Optional[str] = Field(min_length=6)
    birthday: Optional[date] = Field()