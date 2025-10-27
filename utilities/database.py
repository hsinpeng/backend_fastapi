from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker
from sqlalchemy.orm import DeclarativeBase 
from sqlalchemy.schema import CreateTable

from setting.config import get_settings
from models.user import User

settings = get_settings()

# Create engine
engine = create_async_engine(
    settings.database_url,
    echo=True,
    pool_pre_ping=True
)

# Create session
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autocommit=False)

class Base(DeclarativeBase):
    pass

#@asynccontextmanager # 透過 @contextlib.asynccontextmanager 將 async_generator 轉換成 async 的 context manager
async def get_db():
    """Dependency that provides a database session for a single request."""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with SessionLocal() as db:
        async with db.begin():
            await db.execute(CreateTable(User.__table__, if_not_exists=True))

async def close_db():
    async with engine.begin() as conn:
        await conn.close()

