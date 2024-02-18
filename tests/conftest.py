import pytest_asyncio
from beanie import init_beanie
from dto.user import UserRegister
from models import __all__ as all_models
from mongomock_motor import AsyncMongoMockClient
from repo.user.mongo import UserMongoRepository
from repo.user.proto import UserRepo


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    """Initialize mock database"""

    client = AsyncMongoMockClient()
    await init_beanie(
        document_models=all_models, database=client.get_database(name='db')
    )
    yield


@pytest_asyncio.fixture()
async def user_repo() -> UserRepo:
    """Get user_repo repository"""

    return UserMongoRepository()


@pytest_asyncio.fixture()
async def user(user_repo: UserRepo):
    await user_repo.create_user(UserRegister(username='twoics', password='qwerty'))
