from beanie import init_beanie
from config.config import Settings
from models import __all__ as all_models
from motor.motor_asyncio import AsyncIOMotorClient


async def init_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(), document_models=all_models
    )
