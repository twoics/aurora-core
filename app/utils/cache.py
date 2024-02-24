from config.redis import get_redis
from deps.config import get_settings


async def clear_cache():
    """Called when app shutdown for clear all application cache"""

    redis = get_redis()
    conf = get_settings()
    async for key in redis.scan_iter(f'{conf.GLOBAL_CASH_KEY_PREFIX}:*'):
        await redis.delete(key)
