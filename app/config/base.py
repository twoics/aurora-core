from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app import models
from app.config.config import Settings


async def init_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(), document_models=models.__all__
    )
