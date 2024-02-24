from typing import List

from config.config import Settings
from models import Matrix
from models import User
from redis.asyncio import Redis as AsyncRedis
from services.pool.proto import MatrixConnectionsPool


class RedisConnectionPool(MatrixConnectionsPool):
    def __init__(self, redis: AsyncRedis, conf: Settings):
        self._redis = redis
        self._prefix = f'{conf.GLOBAL_CASH_KEY_PREFIX}:ws:clients'

    async def is_connected(self, user: User, matrix: Matrix) -> bool:
        key = await self._get_user_key(user, matrix)
        return bool(await self._redis.exists(key))

    async def connect(self, user: User, matrix: Matrix):
        key = await self._get_user_key(user, matrix)
        await self._redis.set(name=key, value=matrix.uuid)

    async def disconnect(self, user: User, matrix: Matrix):
        key = await self._get_user_key(user, matrix)
        await self._redis.delete(key)

    async def get_user_controlled_matrices(self, user: User) -> List[str]:
        keys = await self._redis.keys(f'{self._prefix}:{str(user.id)}:*')
        return await self._redis.mget(keys)

    async def _get_user_key(self, user: User, matrix: Matrix) -> str:
        return f'{self._prefix}:{str(user.id)}:{str(matrix.id)}'
