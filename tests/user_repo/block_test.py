import pytest
from models import User
from repo.user.proto import UserRepo


class TestBlockUser:
    @pytest.mark.asyncio
    async def test_block_user(self, user: User, user_repo: UserRepo):
        await user_repo.block_user(user)
        blocked_user = await user_repo.get_by_name(user.username)

        assert not blocked_user.is_matrices_access

    @pytest.mark.asyncio
    async def test_unblock_user(self, user: User, user_repo: UserRepo):
        await user_repo.block_user(user)
        await user_repo.unblock_user(user)

        unblocked_user = await user_repo.get_by_name(user.username)

        assert unblocked_user.is_matrices_access
