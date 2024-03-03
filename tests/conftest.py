import pytest_asyncio
from beanie import init_beanie
from deps.auth import get_auth_service
from deps.config import get_settings
from dto.client import ClientCreate
from dto.matrix import MatrixCreate
from dto.user import UserRegister
from httpx import AsyncClient
from main import app
from models import __all__ as all_models
from models import Matrix
from models import User
from mongomock_motor import AsyncMongoMockClient
from repo.client.mongo import ClientMongoRepository
from repo.client.proto import ClientRepo
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
async def client_repo() -> ClientRepo:
    """Get client repository"""

    return ClientMongoRepository()


@pytest_asyncio.fixture()
async def created_matrix(matrix_repo: MatrixRepo) -> Matrix:
    """Get created matrix"""

    await matrix_repo.create(MatrixCreate(uuid='0SN91roa6', name='Aurora'))
    return await matrix_repo.get_by_uuid('0SN91roa6')


@pytest_asyncio.fixture()
async def created_user(user_repo: UserRepo) -> User:
    """Get simple client"""

    await user_repo.create(UserRegister(username='twoics', password='qwerty'))
    return await user_repo.get_by_name('twoics')


@pytest_asyncio.fixture()
async def created_client_key(client_repo: ClientRepo) -> str:
    """Get created client access key"""

    return await client_repo.create(
        ClientCreate(name='tg-bot', description='Some description')
    )


@pytest_asyncio.fixture()
async def admin_user(user_repo: UserRepo) -> User:
    """Get admin"""

    admin = User(username='admin', password='admin', is_admin=True)
    await admin.insert()
    return await user_repo.get_by_name('admin')


@pytest_asyncio.fixture()
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://localhost') as client:
        yield client


@pytest_asyncio.fixture()
async def user_access_token(created_user) -> str:
    auth_serv = get_auth_service(get_settings())
    return (await auth_serv.generate(created_user))['access_token']  # noqa


@pytest_asyncio.fixture()
async def admin_access_token(admin_user) -> str:
    auth_serv = get_auth_service(get_settings())
    return (await auth_serv.generate(admin_user))['access_token']  # noqa
