from utilities.database import init_db, close_db
from api.infor import router as infor_router
from api.auth import router as auth_router
from api.user import router as user_router
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # replacement of @app.on_event("startup")
    print("ASYNC startup: Initializing resources...")
    await init_db()
    yield
    # replacement of @app.on_event("shutdown")
    print("ASYNC shutdown: Releasing resources...")
    await close_db()

app = FastAPI(lifespan=lifespan)
app.include_router(infor_router)
app.include_router(auth_router)
app.include_router(user_router)