import typing

from app.dto.user import UserRegister
from app.models import User


@typing.runtime_checkable
class UserRepo(typing.Protocol):
    async def get_by_name(self, username: str) -> User | None:
        ...

    async def create_user(self, user: UserRegister) -> None:
        ...

    async def get_by_id(self, user_id: str) -> User | None:
        ...
