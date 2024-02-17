from functools import lru_cache

from config.config import Settings
from dependencies.config import get_settings
from fastapi import Depends
from redis.asyncio import Redis as redis


@lru_cache
async def get_redis(conf: Settings = Depends(get_settings)) -> redis:
    """Get cached redis connection"""

    return redis.from_url(conf.REDIS_URL, encoding='utf8')
