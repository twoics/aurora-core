import pytest
from httpx import AsyncClient
from repo.client.proto import ClientRepo


@pytest.mark.parametrize(
    'data',
    [
        ({'name': 'tg-bot', 'description': 'Some description'}),
        ({'name': 'client without description'}),
    ],
)
class TestCreateClient:
    @pytest.mark.asyncio
    async def test_create(
        self,
        data: dict,
        async_client: AsyncClient,
        admin_access_token: str,
    ):
        response = await async_client.post(
            '/client/',
            json=data,
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )

        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_count_after_create(
        self,
        data: dict,
        async_client: AsyncClient,
        admin_access_token: str,
        client_repo: ClientRepo,
    ):
        await async_client.post(
            '/client/',
            json=data,
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )

        assert len(await client_repo.get_all()) == 1

    @pytest.mark.asyncio
    async def test_body_response_after_create(
        self,
        data: dict,
        async_client: AsyncClient,
        admin_access_token: str,
        client_repo: ClientRepo,
    ):
        response = await async_client.post(
            '/client/',
            json=data,
            headers={'Authorization': f'Bearer {admin_access_token}'},
        )

        assert 'access_key' in response.json()
