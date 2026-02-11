from pydantic import BaseModel
from functools import lru_cache


class Settings(BaseModel):
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "online_bookstore"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


@lru_cache()
def get_settings():
    return Settings()
