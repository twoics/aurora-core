import typing

from models import Matrix
from models import User


@typing.runtime_checkable
class Preprocess(typing.Protocol):
    async def handle(self, data, matrix: Matrix, user: User) -> typing.List[int] | None:
        """Process an incoming message and prepare it for sending to the matrix"""
