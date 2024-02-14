import typing

from dto.matrix import MatrixCreate
from dto.matrix import MatrixDetailGet
from dto.matrix import MatrixUpdate
from models import Matrix
from models import User


@typing.runtime_checkable
class MatrixRepo(typing.Protocol):
    async def create(self, matrix: MatrixCreate) -> None:
        ...

    async def add_user(self, matrix_uuid: str, user: User) -> None:
        ...

    async def remove_user(self, matrix_uuid: str, user: User) -> None:
        ...

    async def update_matrix(self, matrix_uuid: str, matrix: MatrixUpdate) -> None:
        ...

    async def get_by_uuid(self, matrix_uuid: str) -> Matrix | None:
        ...

    async def detail_by_uuid(self, matrix_uuid: str) -> MatrixDetailGet | None:
        ...

    async def user_exists(self, matrix_uuid: str, user: User) -> bool:
        ...

    async def user_matrices(self, user: User) -> typing.List[Matrix]:
        ...
