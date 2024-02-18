from typing import List

from models import Matrix
from models import User


class MatrixConnectionsPoolProto:
    async def is_connected(self, user: User, matrix: Matrix) -> bool:
        """Check is user still in the pool"""

    async def connect(self, user: User, matrix: Matrix):
        """Add a new matrix-client connection into pool"""

    async def disconnect(self, user: User, matrix: Matrix):
        """Delete user from pool"""

    async def get_connected_matrices_uuid_by(self, user: User) -> List[str]:
        """Get all matrices uuids to which the user is connected"""
