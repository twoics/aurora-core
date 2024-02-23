import typing

from dto.user import UserRegister
from dto.user import UserUpdate
from models import User


@typing.runtime_checkable
class UserRepo(typing.Protocol):
    async def get_by_name(self, username: str) -> User | None:
        """Find user with this username and return it"""

    async def create_user(self, user: UserRegister) -> None:
        """Create user and hash his password"""

    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by user_id as str"""

    async def update_user(self, username: str, user: UserUpdate) -> None:
        """Update user with given username and set UserUpdate data"""

    async def block_user(self, user: User) -> None:
        """Block the user so that he cannot connect to matrices"""

    async def unblock_user(self, user: User) -> None:
        """Return user access to connect to matrices"""

    async def renew_access_key(self, user: User) -> str:
        """Return user access key to connect to matrices"""
