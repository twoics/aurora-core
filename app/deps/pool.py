from config.config import Settings
from config.redis import get_redis
from deps.config import get_settings
from fastapi import Depends
from redis.asyncio import Redis as AsyncRedis
from services.pool.clients import RedisConnectionPool
from services.pool.proto import MatrixConnectionsPool


async def get_matrix_connections_pool(
    redis: AsyncRedis = Depends(get_redis), conf: Settings = Depends(get_settings)
) -> MatrixConnectionsPool:
    """Get matrix connections pool"""

    return RedisConnectionPool(redis, conf)
