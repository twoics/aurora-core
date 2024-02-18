from config.config import Settings
from config.redis import get_redis
from dependencies.config import get_settings
from fastapi import Depends
from redis.asyncio import Redis as AsyncRedis
from services.pool.clients import MatrixConnectionsPool
from services.pool.proto import MatrixConnectionsPoolProto


async def get_matrix_connections_pool(
    redis: AsyncRedis = Depends(get_redis), conf: Settings = Depends(get_settings)
) -> MatrixConnectionsPoolProto:
    """Get matrix connections pool"""

    return MatrixConnectionsPool(redis, conf)
