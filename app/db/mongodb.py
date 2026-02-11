from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

settings = get_settings()

client = AsyncIOMotorClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client[settings.DATABASE_NAME]
