from typing import List

from models import Matrix
from models import User
from redis.asyncio import Redis as AsyncRedis
from services.pool.proto import MatrixConnectionsPoolProto


class MatrixConnectionsPool(MatrixConnectionsPoolProto):
    def __init__(self, redis: AsyncRedis):
        self._redis = redis

    async def is_connected(self, user: User, matrix: Matrix) -> bool:
        """Check is user still in the pool"""

        key = await self._get_user_key(user, matrix)
        return bool(await self._redis.exists(key))

    async def connect(self, user: User, matrix: Matrix):
        """Add a new matrix-client connection into pool"""

        key = await self._get_user_key(user, matrix)
        await self._redis.set(name=key, value=str(matrix.id))

    async def disconnect(self, user: User, matrix: Matrix):
        """Delete user from pool"""

        key = await self._get_user_key(user, matrix)
        await self._redis.delete(key)

    async def get_user_matrices(self, user: User) -> List[str]:
        """Get all matrices ids to which the user is connected"""

        keys = await self._redis.keys(f'm-clients:{str(user.id)}:*')
        return await self._redis.mget(keys)

    @staticmethod
    async def _get_user_key(user: User, matrix: Matrix) -> str:
        """Generate key for user"""

        return f'aurora:clients:{str(user.id)}:{str(matrix.id)}'
