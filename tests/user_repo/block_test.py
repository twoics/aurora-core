import pytest
from models import User
from repo.user.proto import UserRepo


class TestBlockUser:
    @pytest.mark.asyncio
    async def test_block_user(self, created_user: User, user_repo: UserRepo):
        await user_repo.block_user(created_user)
        blocked_user = await user_repo.get_by_name(created_user.username)

        assert not blocked_user.is_matrices_access

    @pytest.mark.asyncio
    async def test_unblock_user(self, created_user: User, user_repo: UserRepo):
        await user_repo.block_user(created_user)
        await user_repo.unblock_user(created_user)

        unblocked_user = await user_repo.get_by_name(created_user.username)

        assert unblocked_user.is_matrices_access
