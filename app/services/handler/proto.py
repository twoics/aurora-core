import typing

from app.models import User


@typing.runtime_checkable
class StreamHandler(typing.Protocol):
    async def handle(self, data, uuid: str, user: User) -> typing.List[int] | None:
        ...
