from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from utilities.database import get_db
from utilities.tools import check_user_by_id
from models.item import DbItem as ItemModel
from schemas import item as ItemSchema

router = APIRouter(
    tags=["item"],
    prefix="/item"
)

### tools ###
async def get_item_in_db(title:str, db_session:AsyncSession, id:int=None) -> ItemSchema.ItemInDB :
    if(db_session == None):
        print('Error: No db_session in get_item_in_db()')
        return None
    if (id == None):
        stmt = select(ItemModel).where(ItemModel.title == title)
    else:
        stmt = select(ItemModel).where(and_(ItemModel.id == id, ItemModel.title == title))
        
    result = await db_session.execute(stmt)
    item:ItemSchema.ItemInDB = result.scalars().first()
    if item:
        return item
    else:
        return None


async def check_item_in_db(title:str, db_session:AsyncSession) -> bool :
    item:ItemSchema.ItemInDB = await get_item_in_db(title=title, db_session=db_session)
    if item:
        return True
    else:
        return False


### query item ###
@router.get("/all", response_model=List[ItemSchema.ItemRead], response_description="Get list of items", )
async def item_read_all(db_session:AsyncSession = Depends(get_db)):
    try :
        stmt = select(ItemModel)
        response = await db_session.execute(stmt)
        rows = response.scalars().all()
        return rows
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))

@router.get("/id/{id}", response_model=ItemSchema.ItemRead, response_description="Get item by id", )
async def item_read_by_id(id:int, db_session:AsyncSession = Depends(get_db)):
    try :
        stmt = select(ItemModel).where(ItemModel.id == id)
        response = await db_session.execute(stmt)
        item = response.scalars().first()
        if item is not None:
            return item
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item ID({id}) does not exist")
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))

### create item ###
@router.post("/create", response_model=ItemSchema.ItemCreateResponse, status_code=status.HTTP_201_CREATED, response_description="Create a new item")
async def create_item(newItem: ItemSchema.ItemCreate, db_session:AsyncSession = Depends(get_db)):
    try :
        # check if owner_id already exists
        isExist = await check_user_by_id(id=newItem.owner_id, db_session=db_session)
        if (isExist is not True):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User ID({newItem.owner_id}) does not exist")

        # check if item already exists
        isExist = await check_item_in_db(title=newItem.title, db_session=db_session)
        if isExist:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"Item title({newItem.title}) already exists")
        else:
            # create item
            item = ItemModel(
                title=newItem.title,
                content=newItem.content,
                owner_id=newItem.owner_id
            )
            db_session.add(item)
            await db_session.commit()
            await db_session.refresh(item)
            return item
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))
    

### update item ###
@router.put("/update/content", status_code=200, response_model=ItemSchema.ItemUpdateResponse, response_description="Update item content")
async def update_item(newItem:ItemSchema.ItemUpdate, db_session:AsyncSession = Depends(get_db)):
    try :
        # check if item already exists
        isExist = await check_item_in_db(title=newItem.title, db_session=db_session)
        if isExist:
            stmt = update(ItemModel).where(ItemModel.title == newItem.title).values(
                content=newItem.content,
            )
            await db_session.execute(stmt)
            await db_session.commit()
            return newItem
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item.title = {newItem.title} not found")
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))


### delete item ###
@router.delete("/title/{title}", response_model=str, response_description="Delete item by title", )
async def item_remove_by_title(title:str, db_session:AsyncSession = Depends(get_db)):
    try :
        # check if item already exists
        isExist = await check_item_in_db(title=title, db_session=db_session)
        if isExist:
            stmt = delete(ItemModel).where(ItemModel.title == title)
            await db_session.execute(stmt)
            await db_session.commit()
            return f'Item.title = {title} has been deleted'
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item.title = {title} not found")
    except Exception as e:
        raise HTTPException(status_code=499, detail=str(e))