#from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker
from sqlalchemy.schema import CreateTable
from setting.config import get_settings
from models.user import User

settings = get_settings()

# Create db engine
engine = create_async_engine(
    settings.database_url,
    echo=True,
    pool_pre_ping=True
)

# Create async_session
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autocommit=False)

async def init_db():
    async with SessionLocal() as db:
        async with db.begin():
            await db.execute(CreateTable(User.__table__, if_not_exists=True))

async def close_db():
    async with engine.begin() as conn:
        await conn.close()

#@asynccontextmanager # convert async_session into async_context_manager?
async def get_db():
    """Dependency that provides a database session for a single request."""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
