from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import or_, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User as UserModel
from schemas.user import UserInDB
from fastapi.security import OAuth2PasswordBearer

# Auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

### Hash ###
pwd_context = PasswordHash.recommended() #CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

### Others ###
def parse_boolean(value):
    if value is None:
        return False
    return value.lower() in ('true', '1', 'yes', 'on')

async def get_user_in_db(email:str, username:str, db_session:AsyncSession, id:int=None) -> UserInDB :
    if(db_session == None):
        print('Error: No db_session in get_user_in_db()')
        return None
    if (id == None):
        stmt = select(UserModel).where(or_(UserModel.username == username, UserModel.email == email))
    else:
        stmt = select(UserModel).where(and_(UserModel.id == id, UserModel.username == username))
        
    result = await db_session.execute(stmt)
    user:UserInDB = result.scalars().first()
    if user:
        return user
    else:
        return None
    
async def check_user_in_db(email:str, username:str, db_session:AsyncSession) -> bool :
    user:UserInDB = await get_user_in_db(email=email, username=username, db_session=db_session)
    if user:
        return True
    else:
        return False
