from models import User


class MatrixConnectionsPoolProto:
    async def is_connected(self, user: User) -> bool:
        """Check is user still in the pool"""

    async def connect(self, user):
        """Add a new matrix-client connection into pool"""

    async def disconnect(self, user):
        """Delete user from pool"""
