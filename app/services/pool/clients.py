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

    async def is_connected(self, user: User) -> bool:
        key = self._get_key(user)
        return bool(await self._redis.get(key))

    async def connect(self, user: User, matrix: Matrix):
        if await self.is_connected(user):
            raise ConnectionError('Client already connected')

        key = self._get_key(user)
        val = self._get_val(matrix)
        await self._redis.set(name=key, value=val)

    async def disconnect(self, user: User):
        key = self._get_key(user)
        await self._redis.delete(key)

    async def get_user_controlled_matrices(self, user: User) -> List[str]:
        key = self._get_key(user)
        raw_values = await self._redis.get(key)
        return [value.decode() for value in [raw_values]] if raw_values else []

    def _get_key(self, user: User) -> str:
        return f'{self._prefix}:{str(user.id)}'

    @staticmethod
    def _get_val(matrix: Matrix) -> str:
        return matrix.uuid
