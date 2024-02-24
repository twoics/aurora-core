import typing

from dto.matrix import MatrixCreate
from dto.matrix import MatrixDetailGet
from dto.matrix import MatrixUpdate
from models import Matrix
from models import User


@typing.runtime_checkable
class MatrixRepo(typing.Protocol):
    async def create(self, matrix: MatrixCreate) -> None:
        """Create a new matrix by passing data"""

    async def add_user(self, matrix_uuid: str, user: User) -> None:
        """Add a user to the matrix group - users who can connect to the matrix"""

    async def remove_user(self, matrix_uuid: str, user: User) -> None:
        """Remove a user from the matrix group"""

    async def update(self, matrix_uuid: str, matrix: MatrixUpdate) -> None:
        """Update the matrix by passing data"""

    async def get_by_uuid(self, matrix_uuid: str) -> Matrix | None:
        """Get a matrix by uuid (not id)"""

    async def get_many(self, matrix_uuids: typing.List[str]) -> typing.List[Matrix]:
        """Get a matrix by list of uuids"""

    async def detail_by_uuid(self, matrix_uuid: str) -> MatrixDetailGet | None:
        """Get a matrix and users who can connect to"""

    async def user_exists(self, matrix_uuid: str, user: User) -> bool:
        """Check is user in matrix group"""

    async def user_matrices(self, user: User) -> typing.List[Matrix]:
        """Get all matrices that the user can connect to"""
