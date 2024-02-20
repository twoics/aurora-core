import pytest_asyncio
from beanie import init_beanie
from dto.matrix import MatrixCreate
from dto.user import UserRegister
from models import __all__ as all_models
from models import Matrix
from models import User
from mongomock_motor import AsyncMongoMockClient
from repo.matrix.mongo import MatrixMongoRepository
from repo.matrix.proto import MatrixRepo
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
    """Get user repository"""

    return UserMongoRepository()


@pytest_asyncio.fixture()
async def matrix_repo() -> MatrixRepo:
    """Get matrix repository"""

    return MatrixMongoRepository()


@pytest_asyncio.fixture()
async def created_matrix(matrix_repo: MatrixRepo) -> Matrix:
    await matrix_repo.create(MatrixCreate(uuid='0SN91roa6', name='Aurora'))
    return await matrix_repo.get_by_uuid('0SN91roa6')


@pytest_asyncio.fixture()
async def created_user(user_repo: UserRepo) -> User:
    await user_repo.create_user(UserRegister(username='twoics', password='qwerty'))
    return await user_repo.get_by_name('twoics')
