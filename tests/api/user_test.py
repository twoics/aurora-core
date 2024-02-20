import pytest
from httpx import AsyncClient
from models import User
from repo.user.proto import UserRepo


class TestUserAPI:
    @pytest.mark.parametrize(
        'request_data', [({'username': 'New user', 'password': 'qwerty'})]
    )
    @pytest.mark.asyncio
    async def test_user_register(
        self,
        admin_access_token: str,
        async_client: AsyncClient,
        user_repo: UserRepo,
        request_data: dict,
    ):
        response = await async_client.post(
            '/user/register',
            json=request_data,
            headers={
                'Authorization': f'Bearer {admin_access_token}',
            },
        )

        assert response.status_code == 201
        assert bool(await user_repo.get_by_name(request_data['username']))

    @pytest.mark.parametrize('request_data', [({'username': 'Admin 2'})])
    @pytest.mark.asyncio
    async def test_user_update(
        self,
        admin_user: User,
        admin_access_token: str,
        async_client: AsyncClient,
        user_repo: UserRepo,
        request_data: dict,
    ):
        response = await async_client.put(
            f'/user/{admin_user.username}',
            json=request_data,
            headers={
                'Authorization': f'Bearer {admin_access_token}',
            },
        )
        assert response.status_code == 200
        assert bool(await user_repo.get_by_name(request_data['username']))

    @pytest.mark.asyncio
    async def test_user_update_duplicate(
        self,
        admin_user: User,
        admin_access_token: str,
        async_client: AsyncClient,
        created_user: User,
    ):
        response = await async_client.put(
            f'/user/{admin_user.username}',
            json={'username': created_user.username},
            headers={
                'Authorization': f'Bearer {admin_access_token}',
            },
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_user_create_duplicate(
        self,
        admin_user: User,
        admin_access_token: str,
        async_client: AsyncClient,
        created_user: User,
    ):
        response = await async_client.post(
            '/user/register',
            json={'username': created_user.username, 'password': "doesn't matter"},
            headers={
                'Authorization': f'Bearer {admin_access_token}',
            },
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_user_block(
        self,
        admin_access_token: str,
        created_user: User,
        async_client: AsyncClient,
        user_repo: UserRepo,
    ):
        assert created_user.is_matrices_access
        response = await async_client.post(
            f'/user/{created_user.username}/block',
            headers={
                'Authorization': f'Bearer {admin_access_token}',
            },
        )
        assert response.status_code == 204

        user = await user_repo.get_by_name(created_user.username)
        assert not user.is_matrices_access

    @pytest.mark.asyncio
    async def test_user_unblock(
        self,
        admin_access_token: str,
        created_user: User,
        async_client: AsyncClient,
        user_repo: UserRepo,
    ):
        created_user.is_matrices_access = False
        await created_user.save()
        response = await async_client.post(
            f'/user/{created_user.username}/unblock',
            headers={
                'Authorization': f'Bearer {admin_access_token}',
            },
        )

        assert response.status_code == 204

        user = await user_repo.get_by_name(created_user.username)
        assert user.is_matrices_access


class TestUserAPIPermissions:
    @pytest.mark.asyncio
    async def test_create_permissions(
        self, user_access_token: str, async_client: AsyncClient
    ):
        response = await async_client.post(
            '/user/register',
            headers={
                'Authorization': f'Bearer {user_access_token}',
            },
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_permissions(
        self, user_access_token: str, created_user: User, async_client: AsyncClient
    ):
        response = await async_client.put(
            f'/user/{created_user.username}',
            headers={
                'Authorization': f'Bearer {user_access_token}',
            },
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_block_permissions(
        self, user_access_token: str, created_user: User, async_client: AsyncClient
    ):
        response = await async_client.post(
            f'/user/{created_user.username}/block',
            headers={
                'Authorization': f'Bearer {user_access_token}',
            },
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_unblock_permissions(
        self, user_access_token: str, created_user: User, async_client: AsyncClient
    ):
        response = await async_client.post(
            f'/user/{created_user.username}/unblock',
            headers={
                'Authorization': f'Bearer {user_access_token}',
            },
        )
        assert response.status_code == 403


class TestUserAPINotFound:
    @pytest.mark.asyncio
    async def test_update_permissions(
        self, admin_access_token: str, async_client: AsyncClient
    ):
        response = await async_client.post(
            '/user/not-exists',
            headers={
                'Authorization': f'Bearer {admin_access_token}',
            },
        )
        assert response.status_code == 405

    @pytest.mark.asyncio
    async def test_block_permissions(
        self, admin_access_token: str, async_client: AsyncClient
    ):
        response = await async_client.post(
            '/user/not-exists',
            headers={
                'Authorization': f'Bearer {admin_access_token}',
            },
        )
        assert response.status_code == 405

    @pytest.mark.asyncio
    async def test_unblock_permissions(
        self, admin_access_token: str, async_client: AsyncClient
    ):
        response = await async_client.post(
            '/user/not-exists',
            headers={
                'Authorization': f'Bearer {admin_access_token}',
            },
        )
        assert response.status_code == 405
