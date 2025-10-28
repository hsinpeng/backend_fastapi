#from passlib.context import CryptContext
from pwdlib import PasswordHash
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User as UserModel
from schemas.user import UserInDB

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

async def get_user_in_db(email:str, username:str, db_session:AsyncSession) -> UserInDB :
    stmt = select(UserModel).where(or_(UserModel.username == username, UserModel.email == email))
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