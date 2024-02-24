import pytest
from dto.user import UserRegister
from dto.user import UserUpdate
from models import User
from pymongo.errors import DuplicateKeyError
from repo.user.proto import UserRepo


@pytest.mark.parametrize(
    'user_register',
    [
        UserRegister(username='twoics', password='qwerty'),
        UserRegister(username='hello_world', password='some_random'),
    ],
)
class TestUserRepo:
    @pytest.mark.asyncio
    async def test_create_user(self, user_register, user_repo: UserRepo):
        await user_repo.create_user(user_register)
        assert (
            await user_repo.get_by_name(user_register.username)
        ).username == user_register.username

    @pytest.mark.asyncio
    async def test_create_duplicate_user(self, user_register, user_repo: UserRepo):
        await user_repo.create_user(user_register)
        with pytest.raises(DuplicateKeyError):
            await user_repo.create_user(user_register)

    @pytest.mark.asyncio
    async def test_password_hashing(self, user_register, user_repo: UserRepo):
        assert await user_repo.create_user(user_register) != user_register.password

    @pytest.mark.asyncio
    @pytest.mark.parametrize('new_name', ['changed'])
    async def test_update_user(self, user_register, user_repo: UserRepo, new_name: str):
        await user_repo.create_user(user_register)
        user_before = await user_repo.get_by_name(user_register.username)

        await user_repo.update_user(
            user_register.username, UserUpdate(username=new_name)
        )
        user = await user_repo.get_by_name(new_name)

        assert user.id == user_before.id

    @pytest.mark.asyncio
    @pytest.mark.parametrize('new_name', ['changed'])
    async def test_update_user_by_duplicate_name(
        self, user_register, user_repo: UserRepo, new_name: str
    ):
        await user_repo.create_user(user_register)
        await user_repo.create_user(UserRegister(username=new_name, password='random'))

        with pytest.raises(DuplicateKeyError):
            await user_repo.update_user(
                user_register.username, UserUpdate(username=new_name)
            )


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


class TestAccessKey:
    @pytest.mark.asyncio
    async def test_generate_new_access_key(
        self, created_user: User, user_repo: UserRepo
    ):
        await user_repo.renew_access_key(created_user)
        assert (await user_repo.get_by_name(created_user.username)).access_key

    @pytest.mark.asyncio
    async def test_renew_access_key(self, created_user: User, user_repo: UserRepo):
        await user_repo.renew_access_key(created_user)
        hash_before = (await user_repo.get_by_name(created_user.username)).access_key
        await user_repo.renew_access_key(created_user)
        hash_after = (await user_repo.get_by_name(created_user.username)).access_key

        assert hash_before != hash_after

    @pytest.mark.asyncio
    async def test_access_key_not_exist(self, user_repo: UserRepo):
        assert not await user_repo.get_by_access_key('not exists')

    @pytest.mark.asyncio
    async def test_get_by_access_key(self, created_user: User, user_repo: UserRepo):
        key = await user_repo.renew_access_key(created_user)
        user = await user_repo.get_by_access_key(key)
        assert user == created_user
