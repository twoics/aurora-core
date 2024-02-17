from functools import lru_cache

from config.config import Settings
from dependencies.config import get_settings
from fastapi import Depends
from redis.asyncio import Redis as AsyncRedis


@lru_cache
async def get_redis(conf: Settings = Depends(get_settings)) -> AsyncRedis:
    """Get cached redis connection"""

    return AsyncRedis.from_url(conf.REDIS_URL, decode_responses=True)
