import typing

from dto.user import UserRegister
from dto.user import UserUpdate
from models import User


@typing.runtime_checkable
class UserRepo(typing.Protocol):
    async def get_by_name(self, username: str) -> User | None:
        ...

    async def create_user(self, user: UserRegister) -> None:
        ...

    async def get_by_id(self, user_id: str) -> User | None:
        ...

    async def update_user(self, username: str, user: UserUpdate) -> None:
        ...

    async def block_user(self, user: User) -> None:
        ...

    async def unblock_user(self, user: User) -> None:
        ...
