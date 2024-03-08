from typing import List

from models import Matrix
from models import User


class MatrixConnectionsPool:
    async def is_connected(self, user: User) -> bool:
        """Check is user still in the pool"""

    async def connect(self, user: User, matrix: Matrix):
        """Add a new matrix-client connection into pool"""

    async def disconnect(self, user: User):
        """Remove a one specific matrix-client connection from pool"""

    async def get_user_controlled_matrices(self, user: User) -> List[str]:
        """Get all matrices uuids to which the user is connected"""
