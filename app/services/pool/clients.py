from typing import List

from config.config import Settings
from models import Client
from models import Matrix
from models import User
from redis.asyncio import Redis as AsyncRedis
from services.pool.proto import MatrixConnectionsPool


class RedisConnectionPool(MatrixConnectionsPool):
    def __init__(self, redis: AsyncRedis, conf: Settings):
        self._redis = redis
        self._prefix = f'{conf.GLOBAL_CASH_KEY_PREFIX}:ws:clients'

    async def is_connected(self, client: Client, user: User, matrix: Matrix) -> bool:
        key = await self._get_user_key(client, user)
        val = self._get_matrix_value(matrix)
        return (await self._redis.get(key)) == val

    async def connect(self, client: Client, user: User, matrix: Matrix):
        if self.is_connected(client, user, matrix):
            raise ConnectionError('Client already connected')

        key = await self._get_user_key(client, user)
        val = self._get_matrix_value(matrix)
        await self._redis.set(name=key, value=val)

    async def get_user_controlled_matrices(self, user: User) -> List[str]:
        keys = await self._redis.keys(f'{self._prefix}:{str(user.id)}:*')
        return await self._redis.mget(keys)

    async def _get_user_key(self, client: Client, user: User) -> str:
        return f'{self._prefix}:{str(user.id)}:{str(client.id)}'

    @staticmethod
    def _get_matrix_value(matrix: Matrix) -> str:
        return matrix.uuid
