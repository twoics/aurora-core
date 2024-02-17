from config.redis import get_redis
from fastapi import Depends
from redis.asyncio import Redis as AsyncRedis
from services.pool.clients import MatrixConnectionsPool
from services.pool.proto import MatrixConnectionsPoolProto


async def get_matrix_connections_pool(
    redis: AsyncRedis = Depends(get_redis),
) -> MatrixConnectionsPoolProto:
    """Get matrix connections pool"""

    return MatrixConnectionsPool(redis)
