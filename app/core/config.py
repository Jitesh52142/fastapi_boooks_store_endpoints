import os
from pydantic import BaseModel
from functools import lru_cache
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseModel):
    MONGO_URI: str = os.getenv("MONGO_URI")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "online_bookstore")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )

@lru_cache()
def get_settings():
    return Settings()
