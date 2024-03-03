from typing import List

from models import Client
from models import Matrix
from models import User


class MatrixConnectionsPool:
    async def is_connected(self, client: Client, user: User, matrix: Matrix) -> bool:
        """Check is user still in the pool"""

    async def connect(self, client: Client, user: User, matrix: Matrix):
        """Add a new matrix-client connection into pool"""

    async def disconnect(self, client: Client, user: User, matrix: Matrix):
        """Delete user from pool"""

    async def get_user_controlled_matrices(self, user: User) -> List[str]:
        """Get all matrices uuids to which the user is connected"""
