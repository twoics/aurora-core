import typing

from app.dto.matrix import MatrixCreate
from app.models import User


@typing.runtime_checkable
class MatrixRepo(typing.Protocol):
    async def create(self, matrix: MatrixCreate) -> None:
        ...

    async def add_user(self, matrix_uuid: str, user: User) -> None:
        ...
