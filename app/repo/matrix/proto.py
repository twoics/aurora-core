import typing

from app.dto.matrix import MatrixCreate
from app.dto.matrix import MatrixGet
from app.dto.matrix import MatrixUpdate
from app.models import Matrix
from app.models import User


@typing.runtime_checkable
class MatrixRepo(typing.Protocol):
    async def create(self, matrix: MatrixCreate) -> None:
        ...

    async def add_user(self, matrix_uuid: str, user: User) -> None:
        ...

    async def update_matrix(self, matrix_uuid: str, matrix: MatrixUpdate) -> None:
        ...

    async def get_by_uuid(self, matrix_uuid: str) -> Matrix | None:
        ...

    async def detail_by_uuid(self, matrix_uuid: str) -> MatrixGet | None:
        ...

    async def user_exists(self, matrix_uuid: str, user: User) -> bool:
        ...
