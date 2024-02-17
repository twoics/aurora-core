from models import User
from redis.asyncio import Redis as AsyncRedis
from services.pool.proto import MatrixConnectionsPoolProto


class MatrixConnectionsPool(MatrixConnectionsPoolProto):
    def __init__(self, redis: AsyncRedis):
        self._redis = redis

    async def is_connected(self, user: User) -> bool:
        """Check is user still in the pool"""

        key = await self._get_user_key(user)
        return bool(await self._redis.exists(key))

    async def connect(self, user):
        """Add a new matrix-client connection into pool"""

        key = await self._get_user_key(user)
        await self._redis.set(name=key, value=user.id)

    async def disconnect(self, user):
        """Delete user from pool"""

        key = await self._get_user_key(user)
        await self._redis.delete(key)

    @staticmethod
    async def _get_user_key(user: User) -> str:
        """Generate key for user"""

        return f'm-clients:{str(user.pk)}'
