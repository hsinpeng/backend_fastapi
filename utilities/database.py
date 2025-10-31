#from contextlib import asynccontextmanager
import shutil
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker
from sqlalchemy.schema import CreateTable
from setting.config import get_settings
from models.user import DbUser as UserModel
from models.item import DbItem as ItemModel

settings = get_settings()

# create db engine
engine = create_async_engine(
    settings.database_url,
    echo=True,
    pool_pre_ping=True
)
# create async_session
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autocommit=False)

# db and storage resources handling
async def init_db_storage():
    Path(settings.local_storage_path).mkdir(parents=True, exist_ok=True)
    print(f"Directory '{settings.local_storage_path}' created successfully.")
    await init_db()

async def close_db_storage():
    directory_to_remove = Path(settings.local_storage_path)
    if Path(settings.local_storage_path).is_dir():
        try:
            shutil.rmtree(directory_to_remove)
            print(f"Directory '{directory_to_remove}' and its contents removed successfully.")
        except OSError as e:
            print(f"Error: {e.strerror} - Could not remove directory '{directory_to_remove}'.")
    else:
        print(f"Directory '{directory_to_remove}' does not exist.")
    await close_db()

# database
async def init_db():
    async with SessionLocal() as db:
        async with db.begin():
            await db.execute(CreateTable(UserModel.__table__, if_not_exists=True))
            await db.execute(CreateTable(ItemModel.__table__, if_not_exists=True))

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
