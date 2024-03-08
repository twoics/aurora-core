import pytest
from models import Client
from models import Matrix
from models import User
from services.pool.proto import MatrixConnectionsPool


class TestSimpleConnectionPool:
    @pytest.mark.asyncio
    async def test_not_connected(
        self,
        connection_pool: MatrixConnectionsPool,
        created_user: User,
        external_client: Client,
        created_matrix: Matrix,
    ):
        assert not await connection_pool.is_connected(created_user)

    @pytest.mark.asyncio
    async def test_connect(
        self,
        connection_pool: MatrixConnectionsPool,
        created_user: User,
        external_client: Client,
        created_matrix: Matrix,
    ):
        await connection_pool.connect(created_user, created_matrix)
        assert await connection_pool.is_connected(created_user)

    @pytest.mark.asyncio
    async def test_error_connect(
        self,
        connection_pool: MatrixConnectionsPool,
        created_user: User,
        external_client: Client,
        created_matrix: Matrix,
    ):
        await connection_pool.connect(created_user, created_matrix)
        with pytest.raises(ConnectionError):
            await connection_pool.connect(created_user, created_matrix)

    @pytest.mark.asyncio
    async def test_disconnect(
        self,
        connection_pool: MatrixConnectionsPool,
        created_user: User,
        external_client: Client,
        created_matrix: Matrix,
    ):
        await connection_pool.connect(created_user, created_matrix)
        await connection_pool.disconnect(created_user)
        assert not await connection_pool.is_connected(created_user)

    @pytest.mark.asyncio
    async def test_get_empty_controlled_matrices(
        self,
        connection_pool: MatrixConnectionsPool,
        created_user: User,
    ):
        matrices = await connection_pool.get_user_controlled_matrices(created_user)
        assert not len(matrices)

    @pytest.mark.asyncio
    async def test_get_controlled_matrices(
        self,
        connection_pool: MatrixConnectionsPool,
        created_user: User,
        external_client: Client,
        created_matrix: Matrix,
    ):
        await connection_pool.connect(created_user, created_matrix)
        matrices = await connection_pool.get_user_controlled_matrices(created_user)
        assert matrices[0] == created_matrix.uuid
