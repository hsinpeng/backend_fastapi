from pydantic import BaseModel

# class User(BaseModel):
#     id: int
#     username: str
#     email: str

class ItemBase(BaseModel):
    title: str

class ItemInDB(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    
class ItemRead(ItemBase):
    id: int
    title: str
    content: str
    owner_id: int
    # owner: User
    # class Config:
    #     orm_mode = True

class ItemCreate(ItemBase):
    title: str = "Title 000"
    content: str = "Content 000"
    owner_id: int = 1

class ItemCreateResponse(ItemBase):
    title: str
    content: str
    owner_id: int

class ItemUpdate(ItemBase):
    title: str
    content: str
    
class ItemUpdateResponse(ItemBase):
    title: str
    content: str