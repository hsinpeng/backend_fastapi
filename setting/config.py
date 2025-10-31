import os
from functools import lru_cache
from utilities.tools import parse_boolean

@lru_cache()
def get_settings():
    #load_dotenv(f".env.{os.getenv('APP_MODE')}") # useless?
    return Settings()

class Settings():
    # app info
    app_name:str = "A General FastAPI Server"
    author:str = "Sheldon Lin"

    # run setup
    app_mode:str = os.getenv("APP_MODE")
    port_tmp = os.getenv("PORT")
    if port_tmp is not None:
        port:int = int(port_tmp)
    reload:bool = parse_boolean(os.getenv("RELOAD"))

    # storage
    local_storage_path: str = os.getenv("LOCAL_STORAGE_PATH")
    static_storage_path: str = os.getenv("STATIC_STORAGE_PATH")
    # database
    database_url:str = os.getenv("DATABASE_URL") 

    # jwt
    access_token_secret:str = os.getenv("ACCESS_TOKEN_SECRET")
    access_token_expire_minutes_tmp = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    if access_token_expire_minutes_tmp is not None:
        access_token_expire_minutes:int = int(access_token_expire_minutes_tmp)
    refresh_token_secret:str = os.getenv("REFRESH_TOKEN_SECRET")
    refresh_token_expire_minutes_tmp = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
    if refresh_token_expire_minutes_tmp is not None:
        refresh_token_expire_minutes:int = int(refresh_token_expire_minutes_tmp)