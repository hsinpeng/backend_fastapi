from fastapi import APIRouter, Depends
from datetime import date
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from utilities.database import get_db
from models.user import User as UserModel

router = APIRouter(
    tags=["infor"],
    prefix="/info"
)

@router.get("/")
def hello_world():
    return "Hello FastAPI!"

@router.get("/infor")
async def get_infor(db_session:AsyncSession = Depends(get_db)):
    databases = None
    
    try :
        databases = await db_session.execute(text("SELECT * FROM User;"))
    except Exception as e:
        print(e)

    if databases is None:
        try :
            databases = await db_session.execute(text("SHOW DATABASES;"))
        except Exception as e:
            print(e)

    return {
        "database": str(databases.fetchall())
    }

@router.get("/test/create")
async def test_create(db_session:AsyncSession = Depends(get_db)):
    try :
        test_user = UserModel(email="user01@email.com", password="123456", username="user01", 
                              givenname="John", surname="Doe", birthday=date(1973, 7, 4), sex=0)
        db_session.add(test_user)
        await db_session.commit()
        await db_session.refresh(test_user)
        result = "OK"
    except Exception as e:
        print(f'Error: {e}')
        result = e

    return result

@router.get("/test/read")
async def test_read(db_session:AsyncSession = Depends(get_db)):
    try :
        stmt = select(UserModel.id, UserModel.username, UserModel.password).where(UserModel.email == 'user01@email.com')
        result = await db_session.execute(stmt)
        test_user = result.first()
    except Exception as e:
        print(e)

    return f'{test_user.id}, {test_user.username}, {test_user.password}'   
