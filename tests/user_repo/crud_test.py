import pytest
from dto.user import UserRegister
from dto.user import UserUpdate
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
