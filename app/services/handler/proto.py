import typing

from models import Matrix
from models import User


@typing.runtime_checkable
class StreamHandler(typing.Protocol):
    async def handle(self, data, matrix: Matrix, user: User) -> typing.List[int] | None:
        ...
