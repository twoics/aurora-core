import pytest
from dto.client import ClientCreate
from repo.client.proto import ClientRepo


class TestClient:
    @pytest.mark.parametrize(
        'client_data',
        [
            ClientCreate(name='tg-bot', description='Some description'),
            ClientCreate(name='client without description'),
        ],
    )
    @pytest.mark.asyncio
    async def test_create(self, client_data: ClientCreate, client_repo: ClientRepo):
        access_key = await client_repo.create(client_data)
        assert isinstance(access_key, str)

    @pytest.mark.asyncio
    async def test_empty_exist(self, client_repo: ClientRepo):
        assert not await client_repo.exists('something')

    @pytest.mark.asyncio
    async def test_client_exist(self, client_repo: ClientRepo, created_client_key: str):
        assert await client_repo.exists(created_client_key)
