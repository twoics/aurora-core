import pytest
from httpx import AsyncClient
from models import Matrix
from models import User
from repo.matrix.proto import MatrixRepo


@pytest.mark.parametrize('data', [({'uuid': 'uuid', 'name': 'name'})])
class TestMatrixCRUD:
    @pytest.mark.asyncio
    async def test_create(
        self,
        data: dict,
        admin_access_token: str,
        async_client: AsyncClient,
        matrix_repo: MatrixRepo,
    ):
        response = await async_client.post(
            '/matrix/',
            json=data,
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )
        assert response.status_code == 201
        assert await matrix_repo.get_by_uuid(data['uuid'])

    @pytest.mark.asyncio
    async def test_update(
        self,
        admin_access_token: str,
        data: dict,
        async_client: AsyncClient,
        matrix_repo: MatrixRepo,
        created_matrix: Matrix,
    ):
        response = await async_client.put(
            f'/matrix/{created_matrix.uuid}',
            json=data,
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )
        assert response.status_code == 200
        assert await matrix_repo.get_by_uuid(data['uuid'])


class TestMatrixDuplicate:
    @pytest.mark.asyncio
    async def test_create(
        self,
        admin_access_token: str,
        async_client: AsyncClient,
        matrix_repo: MatrixRepo,
        created_matrix: Matrix,
    ):
        response = await async_client.post(
            '/matrix/',
            json={'uuid': created_matrix.uuid, 'name': 'random'},
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_update(
        self,
        admin_access_token: str,
        async_client: AsyncClient,
        matrix_repo: MatrixRepo,
        created_matrix: Matrix,
    ):
        response = await async_client.put(
            f'/matrix/{created_matrix.uuid}',
            json={'uuid': created_matrix.uuid, 'name': 'random'},
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )
        assert response.status_code == 400


class TestMatrixGroup:
    @pytest.mark.asyncio
    async def test_add_user(
        self,
        admin_access_token: str,
        async_client: AsyncClient,
        created_matrix: Matrix,
        created_user: User,
        matrix_repo: MatrixRepo,
    ):
        assert not await matrix_repo.user_exists(created_matrix.uuid, created_user)
        response = await async_client.post(
            f'/matrix/{created_matrix.uuid}/add/{created_user.username}',
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )
        assert response.status_code == 201
        assert await matrix_repo.user_exists(created_matrix.uuid, created_user)

    @pytest.mark.asyncio
    async def test_remove_user(
        self,
        admin_access_token: str,
        async_client: AsyncClient,
        created_matrix: Matrix,
        created_user: User,
        matrix_repo: MatrixRepo,
    ):
        await matrix_repo.add_user(created_matrix.uuid, created_user)
        response = await async_client.delete(
            f'/matrix/{created_matrix.uuid}/remove/{created_user.username}',
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )
        assert response.status_code == 204
        assert not await matrix_repo.user_exists(created_matrix.uuid, created_user)


class TestMatrixNotFound:
    @pytest.mark.asyncio
    async def test_update(self, admin_access_token: str, async_client: AsyncClient):
        response = await async_client.put(
            '/matrix/not-exists',
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_add_user(self, admin_access_token: str, async_client: AsyncClient):
        response = await async_client.post(
            '/matrix/not-exists/add/not-exists',
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_remove_user(
        self, admin_access_token: str, async_client: AsyncClient
    ):
        response = await async_client.delete(
            '/matrix/not-exists/remove/not-exists',
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )
        assert response.status_code == 404


class TestMatrixPermissions:
    @pytest.mark.asyncio
    async def test_create(self, user_access_token: str, async_client: AsyncClient):
        response = await async_client.post(
            '/matrix/',
            headers={'Authorization': f'Bearer {user_access_token}'},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update(self, user_access_token: str, async_client: AsyncClient):
        response = await async_client.put(
            '/matrix/not-exists',
            headers={'Authorization': f'Bearer {user_access_token}'},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_add_user(self, user_access_token: str, async_client: AsyncClient):
        response = await async_client.post(
            '/matrix/not-exists/add/not-exists',
            headers={'Authorization': f'Bearer {user_access_token}'},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_remove_user(self, user_access_token: str, async_client: AsyncClient):
        response = await async_client.delete(
            '/matrix/not-exists/remove/not-exists',
            headers={'Authorization': f'Bearer {user_access_token}'},
        )
        assert response.status_code == 403
